from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, cast, String
from app.models.items import Item
from app.services.base_service import BaseService
from app.utils import response


class ItemsService(BaseService):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Item)

    def get_all_items(self):
        items = self.db.query(Item).all()
        return response(200, "Success", [item.to_dict() for item in items])

    def get_item_by_id(self, item_id):
        item = self._get_by_id(item_id)
        if not item:
            return response(404, "Item not found", None)
        return response(200, "Success", item.to_dict())

    def generate_item_code(self, name, item_type):
        prefix = "".join((name or "ITM").split())[:3].upper() or "ITM"
        type_key = str(item_type).upper()
        type_code = "SVC" if type_key == "SERVICE" else "GDS"

        code_prefix = f"{prefix}-{type_code}-"
        latest = (
            self.db.query(Item)
            .filter(Item.code.like(f"{code_prefix}%"))
            .order_by(desc(Item.id))
            .first()
        )

        next_seq = 1
        if latest and latest.code and latest.code.startswith(code_prefix):
            last_part = latest.code[len(code_prefix):]
            if last_part.isdigit():
                next_seq = int(last_part) + 1

        return f"{code_prefix}{next_seq:03d}"

    def create(self, data):
        item_data = dict(data)
        if not item_data.get("code"):
            item_data["code"] = self.generate_item_code(
                name=item_data.get("name"),
                item_type=item_data.get("type"),
            )

        payload, status = super().create(item_data)
        if payload.get("data") is not None:
            payload["data"] = payload["data"].to_dict()
        return payload, status

    def update_item_by_id(self, item_id, updated_data):
        item = self._get_by_id(item_id)
        if not item:
            return response(404, "Item not found", None)

        payload, status = super().update(item_id, updated_data)
        if payload.get("data") is not None:
            payload["data"] = payload["data"].to_dict()
        return payload, status

    def get_item_list_filter(self, payload):
        """Search, filter, and pagination for items."""
        try:
            page_size = payload.get("page_size", 25)
            page_number = payload.get("page_number", 1)
            sort_by = payload.get("sort_by", "id")
            sort_order = payload.get("sort_order", "DESC")
            search_query = payload.get("search", "")

            expense_ids = payload.get("expense_ids", [])
            quotation_ids = payload.get("quotation_ids", [])

            query = self.db.query(Item)

            if search_query:
                query = query.filter(
                    or_(
                        Item.name.ilike(f"%{search_query}%"),
                        cast(Item.type, String).ilike(f"%{search_query}%"),
                    )
                )

            if expense_ids:
                query = query.filter(Item.expense_id.in_(expense_ids))
            if quotation_ids:
                query = query.filter(Item.quotation_id.in_(quotation_ids))

            sort_column = getattr(Item, sort_by) if hasattr(Item, sort_by) else Item.id
            query = query.order_by(
                desc(sort_column) if sort_order.upper() == "DESC" else asc(sort_column)
            )

            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size

            raw_data = query.offset(offset).limit(page_size).all()
            data_list = [item.to_dict() for item in raw_data]

            result = {
                "list": data_list,
                "pagination": {
                    "current_page": page_number,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items,
                },
            }
            return response(200, "Success", result)

        except Exception as e:
            return response(500, f"Error processing item filter: {str(e)}")
