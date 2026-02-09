from sqlalchemy.orm import Session
from app.models.employees import Employee
from app.services.base_service import BaseService
from app.utils import response


class EmployeeService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Employee)

    def get_all_employees(self):
        return super().get_all()

    def get_employee_by_id(self, employee_id):
        return super().get_by_id(employee_id)

    def create_employee(self, data):
        data['user_id'] = self.get_user_id_login()
        return super().create(data)

    def update_employee_by_id(self, employee_id, data):
        return super().update(employee_id, data)

    def delete_employee_by_id(self, employee_id):
        return super().delete(employee_id)

    # def filter_employees(self, payload: dict):
    #     page_size = payload.get("page_size", 25)
    #     page_number = payload.get("page_number", 1)
    #     sort_by = payload.get("sort_by", "id")
    #     sort_order = payload.get("sort_order", "DESC")

    #     search = payload.get("search")
    #     religions = payload.get("religions")
    #     blood_types = payload.get("blood_types")
    #     marital_statuses = payload.get("marital_statuses")

    #     query = self.db.query(Employee)

    #     # ===============================
    #     # SEARCH (name, nickname, code)
    #     # ===============================
    #     if search:
    #         query = query.filter(
    #             or_(
    #                 Employee.full_name.ilike(f"%{search}%"),
    #                 Employee.nickname.ilike(f"%{search}%"),
    #                 Employee.employee_code.ilike(f"%{search}%")
    #             )
    #         )

    #     # ===============================
    #     # FILTER BY RELIGION
    #     # ===============================
    #     if religions:
    #         query = query.filter(Employee.religion.in_(religions))

    #     # ===============================
    #     # FILTER BY BLOOD TYPE
    #     # ===============================
    #     if blood_types:
    #         query = query.filter(Employee.blood_type.in_(blood_types))

    #     # ===============================
    #     # FILTER BY MARITAL STATUS
    #     # ===============================
    #     if marital_statuses:
    #         query = query.filter(Employee.marital_status.in_(marital_statuses))

    #     # ===============================
    #     # SORTING
    #     # ===============================
    #     sort_column = getattr(Employee, sort_by, Employee.id)
    #     if sort_order.upper() == "ASC":
    #         query = query.order_by(asc(sort_column))
    #     else:
    #         query = query.order_by(desc(sort_column))

    #     # ===============================
    #     # PAGINATION
    #     # ===============================
    #     total_items = query.count()
    #     total_pages = (total_items + page_size - 1) // page_size

    #     items = query.offset(
    #         (page_number - 1) * page_size
    #     ).limit(page_size).all()

    #     return {
    #         "list": items,
    #         "pagination": {
    #             "current_page": page_number,
    #             "page_size": page_size,
    #             "total_pages": total_pages,
    #             "total_items": total_items
    #         }
    #     }