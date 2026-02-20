from sqlalchemy import or_, desc, asc
from app.services.base_service import BaseService
from app.models.partners import Partner, PartnerType, CompanyType
from app.utils import response
import json

class VendorService(BaseService):
    def __init__(self, db):
        super().__init__(db, Partner)

    def get_vendor_list_filter(self, payload):
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            company_types_filter = payload.get('company_types', [])
            industries_filter = payload.get('industries', [])
            query = self.db.query(Partner).filter(Partner.partner_type == PartnerType.VENDOR)

            if search_query:
                query = query.filter(
                    or_(
                        Partner.name.ilike(f"%{search_query}%"),
                        Partner.initials.ilike(f"%{search_query}%"),
                        Partner.industry.ilike(f"%{search_query}%")
                    )
                )

            if company_types_filter:
                valid_enums = []
                for ct in company_types_filter:
                    key = ct.upper().replace(" ", "_")
                    if key in CompanyType.__members__:
                        valid_enums.append(CompanyType[key])
                if valid_enums:
                    query = query.filter(Partner.company_type.in_(valid_enums))

            if industries_filter:
                conditions = [Partner.industry.ilike(f"%{i}%") for i in industries_filter if i]
                if conditions:
                    query = query.filter(or_(*conditions))

            sort_column = getattr(Partner, sort_by) if hasattr(Partner, sort_by) else Partner.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            raw_data = query.offset(offset).limit(page_size).all()
            
            result = {
                "list": [v.to_dict() for v in raw_data],
                "pagination": {
                    "current_page": page_number,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items
                }
            }
            return response(200, "Success", result)

        except Exception as e:
            return response(500, f"Error processing vendor filter: {str(e)}")

    def create_vendor(self, data):
        data["partner_type"] = PartnerType.VENDOR
        return self.create(data)