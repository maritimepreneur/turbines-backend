from app.services.base_service import BaseService
from app.models.partners import Partner, PartnerType
from app.utils import response

class VendorService(BaseService):

    def __init__(self, db):
        super().__init__(db, Partner)

    def get_all(self):
        vendors = (
            self.db.query(self.model)
            .filter(self.model.partner_type == PartnerType.VENDOR)
            .order_by(self.model.created_at.desc())
            .all()
        )

        return response(200, "Action Success", vendors)

    def get_by_id(self, vendor_id: int):
        vendor = (
            self.db.query(self.model)
            .filter(
                self.model.id == vendor_id,
                self.model.partner_type == PartnerType.VENDOR
            )
            .first()
        )

        if not vendor:
            return response(404, "Vendor not found")

        return response(200, "Action Success", vendor)

    def create(self, data):
        data["partner_type"] = PartnerType.VENDOR
        return super().create(data)
