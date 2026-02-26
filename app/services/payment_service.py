from sqlalchemy import desc
from app.models.payments import Payment
from app.models.invoices import Invoice
from datetime import datetime
from flask import abort


class PaymentService:
    def __init__(self, db_session):
        self.db = db_session

    def get_all(self, page=1, per_page=10):
        pagination = Payment.query.order_by(
            desc(Payment.id)
        ).paginate(page=page, per_page=per_page, error_out=False)

        return {
            "message": "Success",
            "code": 200,
            "status": "success",
            "data": {
                "list": [{
                    "id": p.id,
                    "code": p.code,
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

        invoice_id = data.get("invoice_id")
        if not invoice_id:
            raise ValueError("invoice_id is required")

        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")

        code = self.generate_payment_code(invoice)

        new_payment = Payment(
            code=code,
            date=payment_date,
            nominal=data.get("nominal"),
            notes=data.get("notes"),
            attachments=data.get("attachments"),
            invoice_id=invoice_id,
        )

        self.db.add(new_payment)
        self.db.commit()

        return {
            "message": "Payment created successfully",
            "code": 201,
            "status": "success",
            "data": new_payment
        }

    def generate_payment_code(self, invoice):
        invoice_number = invoice.number  # INV-STA-SVC-000001

        prefix = f"PAY-{invoice_number}-"

        last_payment = (
            self.db.query(Payment)
            .filter(Payment.code.ilike(f"{prefix}%"))
            .order_by(desc(Payment.code))
            .first()
        )

        if not last_payment:
            payment_increment = 1
        else:
            last_number = last_payment.code.split("-")[-1]
            payment_increment = int(last_number) + 1

        return f"{prefix}{payment_increment:03d}"

    def update_payment(self, payment_id, data):
        payment = Payment.query.get(payment_id)
        if not payment:
            abort(404, f"Payment ID {payment_id} not found")

        for key, value in data.items():
            if hasattr(payment, key):
                if key == "date" and isinstance(value, str):
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