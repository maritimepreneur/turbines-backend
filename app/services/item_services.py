from app.database import db
from app.models.items import Item
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.services.base_service import BaseService
from app.utils import response

class ItemsService(BaseService):

    def __init__(self, db_session: Session):
        super().__init__(db_session, Item)

    def get_item_list_filter(self, payload):
        """NEW: Search, Filter, and Pagination for Items (BaseService Standard)"""
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            
            expense_ids = payload.get('expense_ids', [])
            quotation_ids = payload.get('quotation_ids', [])

            query = self.db.query(Item)

            if search_query:
                query = query.filter(
                    or_(
                        Item.name.ilike(f"%{search_query}%"),
                        Item.type.ilike(f"%{search_query}%")
                    )
                )

            if expense_ids:
                query = query.filter(Item.expense_id.in_(expense_ids))
            if quotation_ids:
                query = query.filter(Item.quotation_id.in_(quotation_ids))

            sort_column = getattr(Item, sort_by) if hasattr(Item, sort_by) else Item.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))

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
                    "total_items": total_items
                }
            }
            return response(200, "Success", result)

        except Exception as e:
            return response(500, f"Error processing item filter: {str(e)}")

    @staticmethod
    def get_all():
        items = Item.query.all()
        return [item.to_dict() for item in items]

    @staticmethod
    def get_by_id(item_id):
        item = Item.query.get(item_id)
        if not item:
            return None
        return item.to_dict()

    @staticmethod
    def create(data):
        try:
            item = Item(
                name=data["name"],
                cost=data["cost"],
                amount=data["amount"],
                billed_amount=data["billed_amount"],
                type=data["type"],
                amount_type=data["amount_type"],
                attachments=data.get("attachments", []),
                expense_id=data.get("expense_id"),
                quotation_id=data.get("quotation_id")
            )

            db.session.add(item)
            db.session.commit()

            return item.to_dict()

        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update(item_id, data):
        item = Item.query.get(item_id)
        if not item:
            return None

        try:
            item.name = data.get("name", item.name)
            item.cost = data.get("cost", item.cost)
            item.amount = data.get("amount", item.amount)
            item.billed_amount = data.get("billed_amount", item.billed_amount)
            item.type = data.get("type", item.type)
            item.amount_type = data.get("amount_type", item.amount_type)
            item.attachments = data.get("attachments", item.attachments)
            item.expense_id = data.get("expense_id", item.expense_id)
            item.quotation_id = data.get("quotation_id", item.quotation_id)

            db.session.commit()
            return item.to_dict()

        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(item_id):
        item = Item.query.get(item_id)
        if not item:
            return False

        try:
            db.session.delete(item)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            raise