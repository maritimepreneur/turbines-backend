from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.services.base_service import BaseService
from app.models.payments import Payment 
from datetime import datetime
from flask import abort 

class PaymentService:
    def __init__(self, db_session):
        self.db = db_session

    def get_all(self, page=1, per_page=10):
        pagination = Payment.query.order_by(desc(Payment.id)).paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            "message": "Success",
            "code": 200,
            "status": "success",
            "data": {
                "list": [{
                    "id": p.id,
                    "date": p.date.isoformat() if p.date else None,
                    "nominal": float(p.nominal),
                    "notes": p.notes,
                    "invoice_number": p.invoice.number if p.invoice else None,                    
                } for p in pagination.items],
                "pagination": {
                    "current_page": pagination.page,
                    "page_size": pagination.per_page,
                    "total_pages": pagination.pages,
                    "total_items": pagination.total
                }
            }
        }

    def get_by_id(self, payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            abort(404, f"Payment ID {payment_id} not found")
        
        return {
            "message": "Success",
            "code": 200,
            "status": "success",
            "data": payment
        }

    def create_payment(self, data):
        payment_date = data.get("date")
        if isinstance(payment_date, str):
            payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()

        new_payment = Payment(
            date=payment_date,
            nominal=data.get("nominal"),
            notes=data.get("notes"),
            attachments=data.get("attachments"),
            invoice_id=data.get("invoice_id"),    
        )
        self.db.add(new_payment)
        self.db.commit()
        
        return {
            "message": "Payment created successfully",
            "code": 201,
            "status": "success",
            "data": new_payment
        }

    def update_payment(self, payment_id, data):
        payment = Payment.query.get(payment_id)
        if not payment:
            abort(404, f"Payment ID {payment_id} not found")

        for key, value in data.items():
            if hasattr(payment, key):
                if key == 'date' and isinstance(value, str):
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                setattr(payment, key, value)
        
        self.db.commit()
        return {
            "message": "Payment updated successfully",
            "code": 200,
            "status": "success",
            "data": payment
        }

    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            abort(404, f"Payment ID {payment_id} not found")
        
        self.db.delete(payment)
        self.db.commit()
        return {
            "message": "Payment deleted successfully", 
            "code": 200, 
            "status": "success"
        }