from sqlalchemy import desc, asc, or_
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from flask import abort

from app.models.scholarship import Scholarship, ScholarshipStatus
from app.models.users import User


class ScholarshipService:

    CATEGORY_MAPPING = {
    "Training Course": "TRN",
    "Certification": "CRT"
    }

    def __init__(self, db_session):
        self.db = db_session

    def generate_code(self, category):

        if category not in self.CATEGORY_MAPPING:
            raise ValueError("Invalid scholarship category")

        category_code = self.CATEGORY_MAPPING[category]

        today = datetime.now()
        date_str = today.strftime("%y%m%d")

        prefix = f"SCH-{category_code}-{date_str}-"

        last_scholarship = (
            self.db.query(Scholarship)
            .filter(Scholarship.code.ilike(f"{prefix}%"))
            .order_by(desc(Scholarship.code))
            .first()
        )

        if not last_scholarship:
            increment = 1
        else:
            last_number = last_scholarship.code.split("-")[-1]
            increment = int(last_number) + 1

        return f"{prefix}{increment:05d}"

    def calculate_price(self, original_price, discount):

        return original_price - (original_price * discount / 100)

    def create(self, data):

        current_user_id = get_jwt_identity()

        code = self.generate_code(data.get("category"))

        price = self.calculate_price(
            data.get("original_price"),
            data.get("discount")
        )

        new_scholarship = Scholarship(
            name=data.get("name"),
            status=ScholarshipStatus(data.get("status")),
            date=data.get("date"),
            type=data.get("type"),
            category=data.get("category"),
            original_price=data.get("original_price"),
            discount=data.get("discount"),
            price=price,
            code=code,
            created_by=current_user_id
        )

        self.db.add(new_scholarship)
        self.db.commit()

        return {
            "message": "Scholarship created successfully",
            "code": 201,
            "status": "success",
            "data": new_scholarship.to_dict()
        }

    def update(self, scholarship_id, data):

        scholarship = self.db.query(Scholarship).get(scholarship_id)

        if not scholarship:
            abort(404, f"Scholarship ID {scholarship_id} not found")

        current_user_id = get_jwt_identity()

        for key, value in data.items():

            if hasattr(scholarship, key):

                if key == "status":
                    value = ScholarshipStatus(value)

                setattr(scholarship, key, value)

        scholarship.price = self.calculate_price(
            scholarship.original_price,
            scholarship.discount
        )

        scholarship.updated_by = current_user_id

        self.db.commit()

        return {
            "message": "Scholarship updated successfully",
            "code": 200,
            "status": "success",
            "data": scholarship.to_dict()
        }

    def update_expired_scholarships(self):

        today = datetime.today()

        expired = (
            self.db.query(Scholarship)
            .filter(
                Scholarship.date < today,
                Scholarship.status == ScholarshipStatus.ACTIVE
            )
            .all()
        )

        for scholarship in expired:
            scholarship.status = ScholarshipStatus.DEACTIVE

        if expired:
            self.db.commit()

    def get_all(self, payload):

        self.update_expired_scholarships()
        page_size = payload.get("page_size", 25)
        page_number = payload.get("page_number", 1)
        search = payload.get("search", "")
        status = payload.get("status")
        category = payload.get("category")
        sort_by = payload.get("sort_by", "id")
        sort_order = payload.get("sort_order", "DESC")

        query = self.db.query(Scholarship)

        if search:
            query = query.filter(
                or_(
                    Scholarship.name.ilike(f"%{search}%"),
                    Scholarship.code.ilike(f"%{search}%"),
                )
            )

        if status:
            query = query.filter(Scholarship.status == status)

        if category:
            query = query.filter(Scholarship.category == category)

        sort_column = getattr(Scholarship, sort_by) if hasattr(Scholarship, sort_by) else Scholarship.id

        if sort_order.upper() == "DESC":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        total_items = query.count()
        total_pages = (total_items + page_size - 1) // page_size
        offset = (page_number - 1) * page_size

        scholarships = query.offset(offset).limit(page_size).all()

        return {
            "message": "Success",
            "code": 200,
            "status": "success",
            "data": {
                "list": [s.to_dict() for s in scholarships],
                "pagination": {
                    "current_page": page_number,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items
                }
            }
        }

    def get_by_id(self, scholarship_id):

        self.update_expired_scholarships()

        scholarship = self.db.query(Scholarship).get(scholarship_id)

        if not scholarship:
            abort(404, f"Scholarship ID {scholarship_id} not found")

        return {
            "message": "Success",
            "code": 200,
            "status": "success",
            "data": scholarship.to_dict()
        }

    def delete(self, scholarship_id):

        scholarship = self.db.query(Scholarship).get(scholarship_id)

        if not scholarship:
            abort(404, f"Scholarship ID {scholarship_id} not found")

        self.db.delete(scholarship)
        self.db.commit()

        return {
            "message": "Scholarship deleted successfully",
            "code": 200,
            "status": "success"
        }