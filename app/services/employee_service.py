from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.employees import Employee
from app.services.base_service import BaseService
from app.utils import response

class EmployeeService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Employee)

    def get_all_employees(self):
        """ Get all employees dengan serialisasi manual """
        raw_data = self.db.query(Employee).all()
        data = [emp.to_dict() for emp in raw_data]
        return response(200, "Success", data)

    def get_employee_by_id(self, employee_id):
        """ Get employee by ID dengan serialisasi manual """
        employee = self._get_by_id(employee_id)
        if not employee:
            return response(404, "Employee not found", None)
        return response(200, "Success", employee.to_dict())

    def create_employee(self, data):
        """ Create employee """
        if 'nickname' in data:
            existing = self.db.query(Employee).filter(Employee.nickname == data['nickname']).first()
            if existing:
                return response(400, "Nickname already exists")
        
        return super().create(data)

    def update(self, employee_id, updated_data):
        """ Update employee """
        employee = self._get_by_id(employee_id)
        if not employee:
            return response(404, "Employee not found", None)
        return super().update(employee_id, updated_data)

    def delete(self, employee_id):
        """ Delete employee """
        employee = self._get_by_id(employee_id)
        if not employee:
            return response(404, "Employee not found", None)
        return super().delete(employee_id)

    def get_employee_list_filter(self, payload):
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')

            religions = payload.get('religions', [])
            blood_types = payload.get('blood_types', [])
            marital_statuses = payload.get('marital_statuses', [])

            query = self.db.query(Employee)

            if search_query:
                search_term = f"%{search_query}%"
                query = query.filter(
                    or_(
                        Employee.full_name.ilike(search_term),
                        Employee.nickname.ilike(search_term),
                        Employee.employee_code.ilike(search_term)
                    )
                )

            if religions:
                query = query.filter(Employee.religion.in_(religions))
            
            if blood_types:
                query = query.filter(Employee.blood_type.in_(blood_types))
            
            if marital_statuses:
                query = query.filter(Employee.marital_status.in_(marital_statuses))

            if hasattr(Employee, sort_by):
                sort_column = getattr(Employee, sort_by)
            else:
                sort_column = Employee.id

            if sort_order.upper() == 'ASC':
                query = query.order_by(asc(sort_column))
            else:
                query = query.order_by(desc(sort_column))

            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            
            raw_data = query.offset(offset).limit(page_size).all()

            data_list = [emp.to_dict() for emp in raw_data]

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
            return response(500, f"Error filtering employees: {str(e)}")