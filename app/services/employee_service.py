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
        return super().create(data)

    def update_employee_by_id(self, employee_id, data):
        return super().update(employee_id, data)

    def delete_employee_by_id(self, employee_id):
        return super().delete(employee_id)
