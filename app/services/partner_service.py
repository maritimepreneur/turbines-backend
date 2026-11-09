from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.partners import Partner, CompanyType, PartnerType
from app.models.contacts import Contact
from app.models.contact_partners import ContactPartner
from app.services.base_service import BaseService
from app.utils import response

class PartnerService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Partner)

    def get_all_partners(self):
        """ Get all Partner """
        partners = self.db.query(Partner).all()
        return response(200, "Success", partners or [])

    def _normalize_partner_data(self, data):
        if not isinstance(data, dict):
            return data
        
        # Normalize company_type
        if "company_type" in data and isinstance(data["company_type"], str):
            clean = data["company_type"].upper().replace(" ", "").replace("_", "").replace("-", "")
            if clean in ["GOVERNMENT", "GOVERMENT"]:
                data["company_type"] = "GOVERMENT"
            elif clean in ["STATEOWNED", "STATE_OWNED"]:
                data["company_type"] = "STATEOWNED"
            elif clean in ["NONPROFIT", "NON_PROFIT"]:
                data["company_type"] = "NONPROFIT"
            elif clean in ["PRIVATE", "PUBLIC", "OTHER"]:
                data["company_type"] = clean

        # Normalize partner_type
        if "partner_type" in data and isinstance(data["partner_type"], str):
            clean = data["partner_type"].upper().strip()
            if clean in ["VENDOR", "CLIENT", "BOTH", "UNCATEGORIZED", "UNCATEGORIED"]:
                data["partner_type"] = clean

        return data

    def create(self, partner_data):
        """ Register a new Partner """
        partner_data = self._normalize_partner_data(partner_data)
        return super().create(partner_data)

    def update(self, obj_id, data: dict):
        """ Update Partner """
        data = self._normalize_partner_data(data)
        return super().update(obj_id, data)

    def get_partner_by_id(self, partner_id):
        """ Get Partner details """
        partner = self._get_by_id(partner_id)
        if not partner:
            return response(404, "Partner not found", None)
        return super().get_by_id(partner_id)

    def update_partner_by_id(self, partner_id, updated_data):
        """ Update Partner """
        partner = self._get_by_id(partner_id)
        if not partner:
            return response(404, partner_id)
        return super().update(partner_id, updated_data)

    def get_partner_contacts(self, partner_id):
        """ Get all contacts belonging to a specific partner """
        partner = self._get_by_id(partner_id)
        if not partner:
            return response(404, "Partner not found")

        contacts = (
            self.db.query(Contact)
            .join(ContactPartner)
            .filter(ContactPartner.partner_id == partner_id)
            .all()
        )
        return response(200, "Success", contacts)

    def get_partner_list_filter(self, payload):
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')

            industries_filter = payload.get('industries', [])
            company_types_filter = payload.get('company_types', [])
            partner_types_filter = payload.get('partner_types', [])
            services_filter = payload.get('services', [])
            goods_filter = payload.get('goods', [])

            query = self.db.query(Partner)

            if search_query:
                query = query.filter(
                    or_(
                        Partner.name.ilike(f"%{search_query}%"),
                        Partner.initials.ilike(f"%{search_query}%")
                    )
                )

            if industries_filter:
                conditions = [Partner.industry.ilike(f"%{x}%") for x in industries_filter if x]
                if conditions:
                    query = query.filter(or_(*conditions))

            if services_filter:
                conditions = [Partner.service.ilike(f"%{x}%") for x in services_filter if x]
                if conditions:
                    query = query.filter(or_(*conditions))

            if goods_filter:
                conditions = [Partner.goods.ilike(f"%{x}%") for x in goods_filter if x]
                if conditions:
                    query = query.filter(or_(*conditions))

            if company_types_filter:
                enum_values = []
                for item in company_types_filter:
                    for member in CompanyType:
                        if member.value == item:
                            enum_values.append(member)
                if enum_values:
                    query = query.filter(Partner.company_type.in_(enum_values))

            if partner_types_filter:
                enum_values = []
                for item in partner_types_filter:
                    for member in PartnerType:
                        if member.value == item:
                            enum_values.append(member)
                if enum_values:
                    query = query.filter(Partner.partner_type.in_(enum_values))

            if hasattr(Partner, sort_by):
                sort_column = getattr(Partner, sort_by)
            else:
                sort_column = Partner.id

            if sort_order.upper() == 'DESC':
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size

            raw_data = query.offset(offset).limit(page_size).all()
            data = [partner.to_dict() for partner in raw_data]

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
            print(f"Error filtering partners: {e}")
            return response(500, f"Error processing partner filter: {str(e)}")