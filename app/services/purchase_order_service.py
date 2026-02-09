from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.services.base_service import BaseService
from app.models.purchase_orders import Purchase_Order
from datetime import datetime

class PurchaseOrderService(BaseService):
    def __init__(self, db: Session):
        """
        Inisialisasi service dengan session database dan model Purchase_Order.
        Mengikuti pola LeadService agar konsisten dengan BaseService.
        """
        super().__init__(db, Purchase_Order)

    def create_purchase(self, data):
        """
        TASK: Create Purchase Order
        Menghasilkan nomor purchase otomatis sebelum menyimpan ke database.
        """
        # 1. Generate nomor purchase otomatis (PURCHASE-2026-0001)
        data['number'] = self.generate_purchase_number()
        
        # 2. Simpan menggunakan method create dari BaseService
        return self.create(data)

    def generate_purchase_number(self):
        """
        Logika untuk membuat nomor purchase yang unik berdasarkan tahun dan ID terakhir.
        """
        
        # Menggunakan self.db (Session) untuk query data terakhir
        last_purchase = self.db.query(Purchase_Order).order_by(desc(Purchase_Order.id)).first()
        
        if not last_purchase:
            new_number = 1
        else:
            new_number = last_purchase.id + 1
            
        return f"PO-{new_number:04d}"

    def update_purchase(self, id, data):
        """
        TASK: Edit Purchase Order
        Memastikan nomor purchase tidak ikut diubah saat update data lain.
        """
        # Hapus 'number' dari data agar tidak terjadi perubahan nomor manual
        data.pop('number', None)
            
        return self.update(id, data)