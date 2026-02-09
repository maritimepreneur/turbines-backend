from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, not_
from flask_jwt_extended import get_jwt_identity
from app.models.employees import Employee
from app.services.base_service import BaseService
from app.utils import response

class EmployeeService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Employee)

    def _generate_code(self):
        """Helper: Auto Generate EMP-XXXX"""
        last = self.db.query(Employee).order_by(desc(Employee.id)).first()
        if not last or not last.employee_code: return "EMP-0001"
        try:
            return f"EMP-{int(last.employee_code.split('-')[1]) + 1:04d}"
        except: return "EMP-0001"

    def get_current_employee_profile(self):
        """Get Profile by Token"""
        emp = self.db.query(Employee).filter(Employee.user_id == get_jwt_identity()).first()
        return response(200, "Success", emp.to_dict()) if emp else response(404, "Profile not found", None)

    def get_all_employees(self):
        """Get All dengan Serialisasi (Menggunakan Super tapi di-convert)"""
        data = [x.to_dict() for x in self.db.query(Employee).all()]
        return response(200, "Success", data)

    def get_employee_by_id(self, id):
        """Get One dengan Serialisasi"""
        emp = self._get_by_id(id)
        return response(200, "Success", emp.to_dict()) if emp else response(404, "Not Found", None)

    def create_employee(self, data):
        """Create dengan Validasi & Auto Code"""
        uid = get_jwt_identity()
        if self.db.query(Employee).filter(Employee.user_id == uid).first():
            return response(400, "User already linked")
        if 'nickname' in data and self.db.query(Employee).filter(Employee.nickname == data['nickname']).first():
            return response(400, "Nickname exists")
        
        data.update({"user_id": uid, "employee_code": self._generate_code()})
        return super().create(data)

    def update(self, id, data):
        """Update dengan proteksi employee_code"""
        data.pop('employee_code', None)
        return super().update(id, data)

    def delete(self, id):
        """Delete standard"""
        return super().delete(id)

    def get_employee_list_filter(self, payload):
        """Search & Filter Compact Version"""
        try:
            q = self.db.query(Employee)
            
            if s := payload.get('search'):
                term = f"%{s}%"
                q = q.filter(or_(Employee.full_name.ilike(term), Employee.nickname.ilike(term), Employee.employee_code.ilike(term)))

            for key, col in [('religions', Employee.religion), ('blood_types', Employee.blood_type), ('marital_statuses', Employee.marital_status)]:
                if val := payload.get(key): q = q.filter(col.in_(val))

            sort_col = getattr(Employee, payload.get('sort_by', 'id'), Employee.id)
            q = q.order_by(asc(sort_col) if payload.get('sort_order', 'DESC') == 'ASC' else desc(sort_col))
            
            page, size = payload.get('page_number', 1), payload.get('page_size', 25)
            total = q.count()
            data = [x.to_dict() for x in q.offset((page - 1) * size).limit(size).all()]

            return response(200, "Success", {
                "list": data,
                "pagination": {"current_page": page, "page_size": size, "total_pages": (total + size - 1) // size, "total_items": total}
            })
        except Exception as e:
            return response(500, f"Error: {str(e)}")
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