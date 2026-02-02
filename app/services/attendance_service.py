from sqlalchemy.orm import Session
from datetime import date, datetime
from app.services.base_service import BaseService
from app.models.attendances import Attendance
from app.utils import response

class AttendanceService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Attendance)
    
    def get_attendance_by_id(self, attendance_id: int):
        return self.get_by_id(attendance_id)
    
    def delete_attendance(self, attendance_id: int):
        return self.delete(attendance_id)

    def clock_in(self, employee_id: int, payload: dict):
        """
        Clock in for employee
        payload: {
            "timestamp": "2025-02-02T08:00:00",
            "status": "On Time" / "Late",
            "desc": "Arrived at office",
            "latitude": -6.200000,
            "longitude": 106.816666
        }
        """
        try:
            today = date.today()
            
            # Check if already clocked in today
            existing = self.db.query(Attendance).filter(
                Attendance.employee_id == employee_id,
                Attendance.date == today
            ).first()
            
            if existing:
                return response(400, "Already clocked in today")
            
            # Create clock in data
            clock_in_data = {
                "timestamp": payload.get('timestamp', datetime.now().isoformat()),
                "status": payload.get('status', 'On Time'),
                "desc": payload.get('desc', ''),
                "latitude": payload.get('latitude'),
                "longitude": payload.get('longitude')
            }
            
            # Create new attendance record
            new_attendance = Attendance(
                date=today,
                employee_id=employee_id,
                clock_in=clock_in_data,
                clock_out={},  # Empty for now
                checked=False  # Default belum di-check
            )
            
            self.db.add(new_attendance)
            self.db.commit()
            self.db.refresh(new_attendance)
            
            return response(201, "Clock in successful", new_attendance)
            
        except Exception as e:
            self.db.rollback()
            return response(500, f"Error clock in: {str(e)}")

    def clock_out(self, employee_id: int, payload: dict):
        """
        Clock out for employee
        payload: {
            "timestamp": "2025-02-02T17:00:00",
            "status": "On Time" / "Early",
            "desc": "Finished work",
            "latitude": -6.200000,
            "longitude": 106.816666
        }
        """
        try:
            today = date.today()
            
            # Find today's attendance
            attendance = self.db.query(Attendance).filter(
                Attendance.employee_id == employee_id,
                Attendance.date == today
            ).first()
            
            if not attendance:
                return response(404, "Please clock in first")
            
            if attendance.clock_out and attendance.clock_out != {}:
                return response(400, "Already clocked out today")
            
            # Create clock out data
            clock_out_data = {
                "timestamp": payload.get('timestamp', datetime.now().isoformat()),
                "status": payload.get('status', 'On Time'),
                "desc": payload.get('desc', ''),
                "latitude": payload.get('latitude'),
                "longitude": payload.get('longitude')
            }
            
            # Update attendance
            attendance.clock_out = clock_out_data
            self.db.commit()
            self.db.refresh(attendance)
            
            return response(200, "Clock out successful", attendance)
            
        except Exception as e:
            self.db.rollback()
            return response(500, f"Error clock out: {str(e)}")

    def get_today_status(self, employee_id: int):
        """Check if employee has clocked in/out today"""
        try:
            today = date.today()
            attendance = self.db.query(Attendance).filter(
                Attendance.employee_id == employee_id,
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
        """Toggle checked status (for admin/HR)"""
        try:
            attendance = self._get_by_id(attendance_id)
            if not attendance:
                return response(404, "Attendance not found")
            
            # Toggle: jika True jadi False, jika False jadi True
            attendance.checked = not attendance.checked
            self.db.commit()
            self.db.refresh(attendance)
            
            status = "checked" if attendance.checked else "unchecked"
            return response(200, f"Attendance marked as {status}", attendance)
            
        except Exception as e:
            self.db.rollback()
            return response(500, f"Error toggling checked status: {str(e)}")