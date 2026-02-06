from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, not_ # <-- PENTING: Tambahkan not_
from datetime import date, datetime
from app.services.base_service import BaseService
from app.models.attendances import Attendance
from app.models.employees import Employee
from app.utils import response

class AttendanceService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Attendance)

    def _get_employee_from_user(self, user_id: int):
        return self.db.query(Employee).filter(Employee.user_id == user_id).first()
    
    def get_attendance_by_id(self, attendance_id: int):
        return self.get_by_id(attendance_id)
    
    def delete_attendance(self, attendance_id: int):
        return self.delete(attendance_id)

    def clock_in(self, payload: dict):
        try:
            user_id = self.get_user_id_login()
            employee = self._get_employee_from_user(user_id)
            if not employee:
                return response(404, "Employee not found for this user")

            today = date.today()

            existing = self.db.query(Attendance).filter(
                Attendance.employee_id == employee.id,
                Attendance.date == today
            ).first()

            if existing:
                return response(400, "Already clocked in today")
            
            timenow = datetime.now().isoformat()
            ontime = "09:00"
            status = "On Time" if timenow <= f"{today}T{ontime}:00" else "Late"
            
            clock_in_data = {
                "timestamp": timenow,
                "status": status,
                "latitude": payload.get('latitude'),
                "longitude": payload.get('longitude')
            }

            new_attendance = Attendance(
                date=today,
                employee_id=employee.id,
                clock_in=clock_in_data,
                clock_out={},
                checked=False
            )

            self.db.add(new_attendance)
            self.db.commit()
            self.db.refresh(new_attendance)

            return response(201, "Clock in successful", new_attendance)

        except Exception as e:
            self.db.rollback()
            return response(500, f"Error clock in: {str(e)}")

    def clock_out(self, user_id: int, payload: dict):
        try:
            employee = self._get_employee_from_user(user_id)
            if not employee:
                return response(404, "Employee not found for this user")

            today = date.today()

            attendance = self.db.query(Attendance).filter(
                Attendance.employee_id == employee.id,
                Attendance.date == today
            ).first()

            if not attendance:
                return response(404, "Please clock in first")

            if attendance.clock_out and attendance.clock_out != {}:
                return response(400, "Already clocked out today")

            clock_out_data = {
                "timestamp": datetime.now().isoformat(),
                "status": payload.get('status', 'On Time'),
                "desc": payload.get('desc', ''), 
                "latitude": payload.get('latitude'),
                "longitude": payload.get('longitude')
            }

            attendance.clock_out = clock_out_data
            self.db.commit()
            self.db.refresh(attendance)

            return response(200, "Clock out successful", attendance)

        except Exception as e:
            self.db.rollback()
            return response(500, f"Error clock out: {str(e)}")

    def get_today_status(self, user_id: int):
        try:
            employee = self._get_employee_from_user(user_id)
            if not employee:
                return response(404, "Employee not found for this user")

            today = date.today()
            attendance = self.db.query(Attendance).filter(
                Attendance.employee_id == employee.id,
                Attendance.date == today
            ).first()

            if not attendance:
                return response(200, "Success", {
                    "clocked_in": False,
                    "clocked_out": False,
                    "attendance": None
                })

            has_clock_out = attendance.clock_out and attendance.clock_out != {}

            return response(200, "Success", {
                "clocked_in": True,
                "clocked_out": has_clock_out,
                "attendance": attendance.to_dict()
            })

        except Exception as e:
            return response(500, f"Error getting status: {str(e)}")

    def toggle_checked(self, attendance_id: int):
        try:
            attendance = self._get_by_id(attendance_id)
            if not attendance:
                return response(404, "Attendance not found")

            attendance.checked = not attendance.checked
            self.db.commit()
            self.db.refresh(attendance)

            status = "checked" if attendance.checked else "unchecked"
            return response(200, f"Attendance marked as {status}", attendance)

        except Exception as e:
            self.db.rollback()
            return response(500, f"Error toggling checked status: {str(e)}")

    def get_attendance_list_filter(self, payload):
        try:
            page_size = payload.get('page_size', 10)
            page_number = payload.get('page_number', 1)
            search_query = payload.get('search', '')
            checked_filter = payload.get('checked') 
            start_date = payload.get('start_date')
            end_date = payload.get('end_date')
            sort_order = payload.get('sort_order', 'DESC')

            query = self.db.query(Attendance).join(Employee, Attendance.employee_id == Employee.id)

            if search_query:
                query = query.filter(Employee.full_name.ilike(f"%{search_query}%"))

            if checked_filter is not None:
                query = query.filter(Attendance.checked == checked_filter)

            if start_date and end_date:
                query = query.filter(Attendance.date.between(start_date, end_date))
            elif start_date:
                 query = query.filter(Attendance.date >= start_date)

            if sort_order.upper() == 'ASC':
                query = query.order_by(asc(Attendance.date))
            else:
                query = query.order_by(desc(Attendance.date))

            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            
            raw_data = query.offset(offset).limit(page_size).all()

            data_list = []
            for item in raw_data:
                att_dict = item.to_dict()
                att_dict['employee_name'] = item.employee.full_name if item.employee else "Unknown"
                data_list.append(att_dict)

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
            return response(500, f"Error filtering attendance: {str(e)}")

    def get_absent_list(self):
        try:
            today = date.today()

            present_ids_query = self.db.query(Attendance.employee_id).filter(
                Attendance.date == today
            ).all()
            
            present_employee_ids = [x[0] for x in present_ids_query]

            if present_employee_ids:
                absent_query = self.db.query(Employee).filter(
                    not_(Employee.id.in_(present_employee_ids))
                ).all()
            else:
                absent_query = self.db.query(Employee).all()

            data_list = []
            for emp in absent_query:
                data_list.append({
                    "id": emp.id,
                    "employee_name": emp.full_name,
                    "employee_code": emp.employee_code,
                    "nickname": emp.nickname, 
                    "img_url": emp.img_url,
                    "phone": emp.phone
                })

            return response(200, "Success retrieving absent list", data_list)

        except Exception as e:
            return response(500, f"Error getting absent list: {str(e)}")