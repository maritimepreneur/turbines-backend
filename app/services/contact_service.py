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

    def create(self, contact_data):
        """ Register a new contact """
        partner_ids = contact_data.pop("partner_ids", [])
        legacy_partner_id = contact_data.pop("partner_id", None)
        if legacy_partner_id not in (None, 0, "0"):
            partner_ids = [*partner_ids, legacy_partner_id] if isinstance(partner_ids, list) else [partner_ids, legacy_partner_id]

        if partner_ids is None:
            partner_ids = []
        elif isinstance(partner_ids, int):
            partner_ids = [partner_ids]
        elif not isinstance(partner_ids, list):
            return response(400, "Partner ids must be integer or list of integers")

        normalized_partner_ids = []
        for partner_id in partner_ids:
            if partner_id in (None, 0, "0"):
                continue
            try:
                parsed_partner_id = int(partner_id)
            except (TypeError, ValueError):
                return response(400, "Each partner id must be an integer")
            if parsed_partner_id not in normalized_partner_ids:
                normalized_partner_ids.append(parsed_partner_id)

        emails = contact_data.get("emails")
        phones = contact_data.get("phone_numbers")
        company = contact_data.get("company")

        if not company:
            return response(400, "company is required")

        if not isinstance(emails, list) or not isinstance(phones, list):
            return response(400, "emails and phone_numbers must be list")

        email_conditions = [Contact.emails.contains([e]) for e in emails]
        phone_conditions = [Contact.phone_numbers.contains([p]) for p in phones]

        existing = self.db.query(Contact).filter(
            or_(*email_conditions, *phone_conditions)
        ).first()

        if existing:
            return response(409, "Contact with the same email or phone number already exists")

        if normalized_partner_ids:
            existing_partner_ids = {
                row[0]
                for row in self.db.query(Partner.id).filter(Partner.id.in_(normalized_partner_ids)).all()
            }
            missing_partner_ids = sorted(set(normalized_partner_ids) - existing_partner_ids)
            if missing_partner_ids:
                return response(404, f"Partner not found: {missing_partner_ids}")

        contact_data["partner_id"] = normalized_partner_ids[0] if normalized_partner_ids else None

        data = self._inject_create_meta(contact_data)
        new_contact = Contact(**data)
        self.db.add(new_contact)
        self.db.flush()

        for partner_id in normalized_partner_ids:
            self.db.add(
                ContactPartner(
                    contact_id=new_contact.id,
                    partner_id=partner_id,
                    created_by=data.get("created_by"),
                    updated_by=data.get("updated_by"),
                )
            )

        self.db.commit()
        self.db.refresh(new_contact)
        return response(201, "Action Success", new_contact)

    def get_contact_by_id(self, contact_id):
        """ Get Contact details """
        contact = (
            self.db.query(Contact)
            .options(joinedload(Contact.contact_partners).joinedload(ContactPartner.partner))
            .filter(Contact.id == contact_id)
            .first()
        )
        if not contact:
            return response(404, "Contact not found")
        return response(200, "Success", contact)

    def update_contact_by_id(self, contact_id, updated_data):
        """ Update Contact """
        contact = self._get_by_id(contact_id)
        if not contact:
            return response(404, contact_id)

        if "emails" in updated_data:
            contact.emails = list(set(contact.emails + updated_data["emails"]))

        if "phone_numbers" in updated_data:
            contact.phone_numbers = list(set(contact.phone_numbers + updated_data["phone_numbers"]))

        self.db.commit()
        self.db.refresh(contact)
        return response(200, "Action Success", contact)

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
