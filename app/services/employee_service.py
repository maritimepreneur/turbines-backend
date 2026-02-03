from sqlalchemy.orm import Session
from app.models.employees import Employee
from app.services.base_service import BaseService
from app.utils import response


class EmployeeService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Employee)

    def create(self, employee_data):
        """ Create employee """
        return super().create(employee_data)

    def get_employee_by_id(self, employee_id):
        """ Get employee by ID """
        employee = self._get_by_id(employee_id)
        if not employee:
            return response(404, "employee not found", None)
        return response(200, "Success", employee)

    def update_employee_by_id(self, employee_id, updated_data):
        """ Update employee """
        employee = self._get_by_id(employee_id)
        if not employee:
            return response(404, "employee not found", None)
        return super().update(employee_id, updated_data)

    def delete_employee_by_id(self, employee_id):
        """ Delete employee """
        employee = self._get_by_id(employee_id)
        if not employee:
            return response(404, "employee not found", None)
        return super().delete(employee_id)