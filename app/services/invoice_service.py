from sqlalchemy.orm import Session
from app.models.invoices import Invoice
from app.models.contacts import Contact
from app.models.partners import Partner
from app.models.purchase_orders import Purchase_Order
from app.services.base_service import BaseService
from app.utils import response

class InvoiceService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Invoice)

    def get_all_invoices(self):
        """ Get all Invoices """
        invoices = self.db.query(Invoice).all()
        data = [inv.to_dict() for inv in invoices]
        return response(200, "Success", data)

    def create_invoice(self, data):
        """ Create a new Invoice """
        validation = self.validate_fk(data)
        if validation:
            return validation
            
        existing = self.db.query(Invoice).filter(Invoice.number == data.get('number')).first()
        if existing:
            return response(400, "Invoice number already exists")

        return super().create(data)

    def get_invoice_by_id(self, invoice_id):
        """ Get Invoice details """
        invoice = self._get_by_id(invoice_id)
        if not invoice:
            return response(404, "Invoice not found", None)
        return response(200, "Success", invoice.to_dict())

    def update_invoice(self, invoice_id, updated_data):
        """ Update Invoice """
        invoice = self._get_by_id(invoice_id)
        if not invoice:
            return response(404, "Invoice not found", None)

        validation = self.validate_fk(updated_data)
        if validation:
            return validation

        if 'number' in updated_data and updated_data['number'] != invoice.number:
                existing = self.db.query(Invoice).filter(Invoice.number == updated_data['number']).first()
        if existing:
                return response(400, "Invoice number already exists")

        return super().update(invoice_id, updated_data)

    def delete_invoice(self, invoice_id):
        """ Delete Invoice """
        return super().delete(invoice_id)

    def validate_fk(self, data):
        """ Helper untuk validasi Foreign Keys """
        if data.get("contact_id") and not self.db.query(Contact).get(data["contact_id"]):
            return response(404, "Invalid contact_id")
        
        if data.get("partner_id") and not self.db.query(Partner).get(data["partner_id"]):
            return response(404, "Invalid partner_id")
            
        if data.get("purchase_order_id") and not self.db.query(Purchase_Order).get(data["purchase_order_id"]):
            return response(404, "Invalid purchase_order_id")
        
        return None