import json
from sqlalchemy.orm import Session, joinedload 
from sqlalchemy import or_, desc, asc, cast, String
from sqlalchemy.dialects.postgresql import JSONB
from app.models.contacts import Contact
from app.services.base_service import BaseService
from app.utils import response
from app.models.partners import Partner
from app.models.contact_partners import ContactPartner

class ContactService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Contact)

    def get_all_contacts(self):
        """ Get All Contact """
        contacts = (
            self.db.query(Contact)
            .options(joinedload(Contact.contact_partners).joinedload(ContactPartner.partner))
            .all()
        )
        return response(200, "Success", contacts)

    def _parse_partner_ids(self, data):
        """Extract and normalize partner_id / partner_ids from payload."""
        has_partner_field = ("partner_ids" in data) or ("partner_id" in data)
        raw_partner_ids = data.pop("partner_ids", None)
        legacy_partner_id = data.pop("partner_id", None)

        if not has_partner_field:
            return None, None

        combined = []
        if raw_partner_ids is not None:
            if isinstance(raw_partner_ids, int):
                combined.append(raw_partner_ids)
            elif isinstance(raw_partner_ids, list):
                combined.extend(raw_partner_ids)
            else:
                return None, response(400, "Partner ids must be integer or list of integers")

        if legacy_partner_id not in (None, 0, "0", ""):
            combined.append(legacy_partner_id)

        normalized_ids = []
        for pid in combined:
            if pid in (None, 0, "0", ""):
                continue
            try:
                parsed_id = int(pid)
            except (TypeError, ValueError):
                return None, response(400, "Each partner id must be an integer")
            if parsed_id not in normalized_ids:
                normalized_ids.append(parsed_id)

        if normalized_ids:
            existing_partner_ids = {
                row[0]
                for row in self.db.query(Partner.id).filter(Partner.id.in_(normalized_ids)).all()
            }
            missing_ids = sorted(set(normalized_ids) - existing_partner_ids)
            if missing_ids:
                return None, response(404, f"Partner not found: {missing_ids}")

        return normalized_ids, None

    def _sync_contact_partners(self, contact, partner_ids, user_id):
        """Synchronize contact.partner_id and contact_partners junction rows."""
        contact.partner_id = partner_ids[0] if partner_ids else None
        self.db.query(ContactPartner).filter(ContactPartner.contact_id == contact.id).delete()
        for partner_id in partner_ids:
            cp = ContactPartner()
            cp.contact_id = contact.id
            cp.partner_id = partner_id
            cp.created_by = user_id
            cp.updated_by = user_id
            self.db.add(cp)

    def _check_duplicate_contact(self, emails, phone_numbers, exclude_contact_id=None):
        """Return conflict response if email or phone already exists on another contact."""
        email_conditions = [Contact.emails.contains([e]) for e in emails if e]
        phone_conditions = [Contact.phone_numbers.contains([p]) for p in phone_numbers if p]
        all_conditions = email_conditions + phone_conditions
        if not all_conditions:
            return None

        query = self.db.query(Contact).filter(or_(*all_conditions))
        if exclude_contact_id is not None:
            query = query.filter(Contact.id != exclude_contact_id)

        if query.first():
            msg = (
                "Email or phone number already used by another contact"
                if exclude_contact_id is not None
                else "Contact with the same email or phone number already exists"
            )
            return response(409, msg)
        return None

    def _load_contact_with_partners(self, contact_id):
        """Fetch contact with joined contact_partners and partner details."""
        return (
            self.db.query(Contact)
            .options(joinedload(Contact.contact_partners).joinedload(ContactPartner.partner))
            .filter(Contact.id == contact_id)
            .first()
        )

    def create(self, contact_data):
        """ Register a new contact """
        payload = dict(contact_data or {})
        normalized_partner_ids, err_resp = self._parse_partner_ids(payload)
        if err_resp:
            return err_resp
        normalized_partner_ids = normalized_partner_ids or []

        emails = payload.get("emails")
        phones = payload.get("phone_numbers")
        if not isinstance(emails, list) or not isinstance(phones, list):
            return response(400, "emails and phone_numbers must be list")

        company = (payload.get("company") or "").strip()
        if not company:
            if normalized_partner_ids:
                first_partner = self.db.query(Partner).filter(Partner.id == normalized_partner_ids[0]).first()
                company = first_partner.name if first_partner else "-"
            else:
                company = "-"
        payload["company"] = company

        dup_resp = self._check_duplicate_contact(emails, phones)
        if dup_resp:
            return dup_resp

        payload["partner_id"] = normalized_partner_ids[0] if normalized_partner_ids else None

        data = self._inject_create_meta(payload)
        new_contact = Contact(**data)
        self.db.add(new_contact)
        self.db.flush()

        self._sync_contact_partners(new_contact, normalized_partner_ids, data.get("created_by"))

        self.db.commit()
        created_contact = self._load_contact_with_partners(new_contact.id)
        return response(201, "Action Success", created_contact)

    def get_contact_by_id(self, contact_id):
        """ Get Contact details """
        contact = self._load_contact_with_partners(contact_id)
        if not contact:
            return response(404, "Contact not found")
        return response(200, "Success", contact)

    def update_contact_by_id(self, contact_id, updated_data):
        """ Update Contact """
        contact = self._get_by_id(contact_id)
        if not contact:
            return response(404, "Contact not found")

        payload = dict(updated_data or {})
        normalized_partner_ids, err_resp = self._parse_partner_ids(payload)
        if err_resp:
            return err_resp

        has_emails = "emails" in payload
        has_phones = "phone_numbers" in payload
        new_emails = payload.get("emails", []) if has_emails else []
        new_phones = payload.get("phone_numbers", []) if has_phones else []

        if has_emails and not isinstance(new_emails, list):
            return response(400, "emails must be list")
        if has_phones and not isinstance(new_phones, list):
            return response(400, "phone_numbers must be list")

        dup_resp = self._check_duplicate_contact(new_emails, new_phones, exclude_contact_id=contact_id)
        if dup_resp:
            return dup_resp

        if "name" in payload:
            contact.name = payload["name"]
        if "company" in payload:
            contact.company = (payload["company"] or "").strip() or "-"
        if "nasionality" in payload:
            contact.nasionality = payload["nasionality"]
        if "role" in payload:
            contact.role = payload["role"]
        if "position" in payload:
            contact.position = payload["position"]
        if has_emails:
            contact.emails = new_emails
        if has_phones:
            contact.phone_numbers = new_phones

        user_id = self.get_user_id_login()
        if normalized_partner_ids is not None:
            self._sync_contact_partners(contact, normalized_partner_ids, user_id)

        contact.updated_by = user_id

        self.db.commit()
        self.db.expire(contact)
        updated_contact = self._load_contact_with_partners(contact_id)
        return response(200, "Action Success", updated_contact)

    def get_contact_list_filter(self, payload):
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')

            names_filter = payload.get('names', [])
            emails_filter = payload.get('emails', [])
            phones_filter = payload.get('phone_numbers', [])
            companies_filter = payload.get('companies', [])

            start_date = payload.get('start_date')
            end_date = payload.get('end_date')

            query = (
                self.db.query(Contact)
                .options(joinedload(Contact.contact_partners).joinedload(ContactPartner.partner))
            )

            if search_query:
                query = query.filter(
                    or_(
                        Contact.name.ilike(f"%{search_query}%"),
                        cast(Contact.emails, String).ilike(f"%{search_query}%")
                    )
                )

            if start_date and end_date:
                query = query.filter(Contact.created_at.between(start_date, end_date))
            else:
                if names_filter:
                    conditions = [Contact.name.ilike(f"%{n}%") for n in names_filter if n]
                    if conditions:
                        query = query.filter(or_(*conditions))

                if companies_filter:
                    conditions = [Contact.company.ilike(f"%{c}%") for c in companies_filter if c]
                    if conditions:
                        query = query.filter(or_(*conditions))

                if emails_filter:
                    email_conditions = [Contact.emails.contains([e]) for e in emails_filter]
                    query = query.filter(or_(*email_conditions))

                if phones_filter:
                    phone_conditions = [Contact.phone_numbers.contains([p]) for p in phones_filter]
                    query = query.filter(or_(*phone_conditions))

            if hasattr(Contact, sort_by):
                sort_column = getattr(Contact, sort_by)
            else:
                sort_column = Contact.id

            if sort_order.upper() == 'DESC':
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size

            raw_data = query.offset(offset).limit(page_size).all()
            data = [contact.to_dict() for contact in raw_data]

            result = {
                "list": data,
                "pagination": {
                    "current_page": page_number,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items
                }
            }

            return response(200, "Success", result)

        except Exception as e:
            print(f"Error filtering contacts: {e}")
            return response(500, f"Error processing contact filter: {str(e)}")
