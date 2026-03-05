from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from datetime import datetime
from app.services.base_service import BaseService
from app.models.schedules import Schedule
from app.models.employees import Employee
from app.utils import response

class ScheduleService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Schedule)
    
    def _enrich_schedule_with_tagged(self, schedule_dict):
        """Add tagged_employees detail to schedule dict"""
        tagged_employees = []
        if schedule_dict.get('tagged_ids') and len(schedule_dict['tagged_ids']) > 0:
            tagged_employees = self.db.query(Employee).filter(
                Employee.id.in_(schedule_dict['tagged_ids'])
            ).all()
            
            tagged_employees = [
                {
                    "id": emp.id,
                    "full_name": emp.full_name,
                    "employee_code": emp.employee_code
                } for emp in tagged_employees
            ]
        
        schedule_dict['tagged_employees'] = tagged_employees
        return schedule_dict
    
    def get_all_schedules(self):
        try:
            schedules = self.db.query(Schedule).all()
            data = [self._enrich_schedule_with_tagged(schedule.to_dict()) for schedule in schedules]
            return response(200, "Action Success", data)
        except Exception as e:
            return response(500, f"Error fetching schedules: {str(e)}")
    
    def get_schedule_by_id(self, schedule_id: int):
        try:
            schedule = self._get_by_id(schedule_id)
            if not schedule:
                return response(404, "Schedule not found")
            
            data = self._enrich_schedule_with_tagged(schedule.to_dict())
            return response(200, "Action Success", data)
        except Exception as e:
            return response(500, f"Error fetching schedule: {str(e)}")
    
    def create_schedule(self, user_id: int, user_role: str, data: dict):
        try:
            # Cari employee berdasarkan user_id yang sedang login
            employee = self.db.query(Employee).filter(Employee.user_id == user_id).first()
            if not employee:
                return response(404, "Employee not found for this user")
                
            # Tetapkan employee_id berdasarkan employee yang ditemukan
            data["employee_id"] = employee.id
                
            # Buat schedule baru
            return self.create(data)
        except Exception as e:
            return response(500, str(e))

    
    def update_schedule(self, schedule_id: int, data):
        return self.update(schedule_id, data)
    
    def delete_schedule(self, schedule_id: int):
        return self.delete(schedule_id)

    def get_schedule_list_filter(self, payload):
        """Get schedules with filter and pagination"""
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'date')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            
            date_start = payload.get('date_start')
            date_end = payload.get('date_end')
            employees_filter = payload.get('employees', [])
            
            query = self.db.query(Schedule)\
                .outerjoin(Employee, Schedule.employee_id == Employee.id)
            
            if search_query:
                query = query.filter(
                    or_(
                        Schedule.title.ilike(f"%{search_query}%"),
                        Schedule.description.ilike(f"%{search_query}%"),
                        Employee.full_name.ilike(f"%{search_query}%")
                    )
                )
            
            if date_start and date_end:
                query = query.filter(Schedule.date.between(date_start, date_end))
            
            if employees_filter:
                conditions = [Employee.full_name.ilike(f"%{e}%") for e in employees_filter if e]
                if conditions:
                    query = query.filter(or_(*conditions))
            
            if hasattr(Schedule, sort_by):
                sort_column = getattr(Schedule, sort_by)
            elif sort_by == 'employee_name':
                sort_column = Employee.full_name
            else:
                sort_column = Schedule.date
            
            if sort_order.upper() == 'DESC':
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
            
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            raw_data = query.offset(offset).limit(page_size).all()
            data = [self._enrich_schedule_with_tagged(schedule.to_dict()) for schedule in raw_data]
            
            result = {
                "list": data,
                "pagination": {
                    "current_page": page_number,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items
                }
            }
            
            return response(200, "Success", result)
            
        except Exception as e:
            return response(500, f"Error filtering schedules: {str(e)}")

    def get_my_schedules(self, user_id: int):
        """Get schedules for logged-in user (employee) — including tagged schedules"""
        try:
            employee = self.db.query(Employee).filter(Employee.user_id == user_id).first()
            if not employee:
                return response(404, "Employee not found for this user")
            
            schedules = self.db.query(Schedule)\
                .filter(
                    or_(
                        Schedule.employee_id == employee.id,
                        Schedule.tagged_ids.contains([employee.id])  # JSONB contains
                    )
                )\
                .order_by(desc(Schedule.date))\
                .all()
            
            data = [self._enrich_schedule_with_tagged(schedule.to_dict()) for schedule in schedules]
            return response(200, "Success", data)
            
        except Exception as e:
            return response(500, f"Error fetching schedules: {str(e)}")

    def get_employee_list_dropdown(self):
        """Get lightweight employee list for dropdowns"""
        try:
            employees = self.db.query(Employee.id, Employee.full_name, Employee.employee_code).all()
            result = [{"id": e.id, "name": e.full_name, "code": e.employee_code} for e in employees]
            return response(200, "Success", result)
        except Exception as e:
            return response(500, f"Error fetching employee list: {str(e)}")