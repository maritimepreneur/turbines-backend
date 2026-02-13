from app.database import db
from app.models.items import Item
from sqlalchemy.exc import SQLAlchemyError


class ItemsService:

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
