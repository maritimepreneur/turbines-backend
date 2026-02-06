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

        if not data.get('employee_code') or data.get('employee_code') == "string":
            data['employee_code'] = self.generate_employee_code()

        return super().create(data)
    
    from datetime import datetime

    def generate_employee_code(self):
        
        count = self.db.query(Employee).count()
        new_number = count + 1
        
        new_code = f"EMP{new_number:03d}"
        
        return new_code

    def update_employee_by_id(self, employee_id, data):
        return super().update(employee_id, data)

    def delete_employee_by_id(self, employee_id):
        return super().delete(employee_id)
