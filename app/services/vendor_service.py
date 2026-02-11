from app.services.base_service import BaseService
from app.models.partners import Partner, PartnerType, CompanyType
from app.utils import response
import json

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

        # GUNAKAN to_dict() yang sudah ada di model
        vendors_list = [vendor.to_dict() for vendor in vendors]

        return response(200, "Action Success", vendors_list)

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

        # GUNAKAN to_dict()
        return response(200, "Action Success", vendor.to_dict())

    def create(self, data):
        # Validasi dan konversi company_type
        company_type_str = data.get("company_type", "").upper().replace(" ", "_")
        
        # Mapping untuk company_type (sesuaikan dengan enum di model)
        company_type_mapping = {
            "OTHER": CompanyType.OTHER,
            "GOVERMENT": CompanyType.GOVERMENT,
            "PRIVATE": CompanyType.PRIVATE,
            "STATEOWNED": CompanyType.STATEOWNED,
            "STATE_OWNED": CompanyType.STATEOWNED,
            "PUBLIC": CompanyType.PUBLIC,
            "NONPROFIT": CompanyType.NONPROFIT,
            "NON_PROFIT": CompanyType.NONPROFIT,
        }
        
        try:
            if company_type_str in company_type_mapping:
                data["company_type"] = company_type_mapping[company_type_str]
            else:
                # Coba langsung pakai value dari string
                data["company_type"] = CompanyType[company_type_str]
        except (KeyError, AttributeError):
            # Kembalikan error jika company_type tidak valid
            valid_values = [e.name for e in CompanyType]
            return response(400, f"Invalid company_type. Valid values are: {valid_values}")
        
        # Set partner_type ke VENDOR
        data["partner_type"] = PartnerType.VENDOR
        
        # Konversi service dan goods ke list jika perlu
        if "service" in data:
            if isinstance(data["service"], str):
                try:
                    data["service"] = json.loads(data["service"])
                except json.JSONDecodeError:
                    data["service"] = []
            elif not isinstance(data["service"], list):
                data["service"] = []
        
        if "goods" in data:
            if isinstance(data["goods"], str):
                try:
                    data["goods"] = json.loads(data["goods"])
                except json.JSONDecodeError:
                    data["goods"] = []
            elif not isinstance(data["goods"], list):
                data["goods"] = []
        
        # Panggil create dari BaseService
        result = super().create(data)
        
        # Jika berhasil, kembalikan data vendor yang baru dibuat
        if result.get("success") and "data" in result:
            # Ambil vendor yang baru dibuat
            vendor_id = result["data"].id if hasattr(result["data"], 'id') else result["data"]
            new_vendor = self.db.query(self.model).get(vendor_id)
            if new_vendor:
                result["data"] = new_vendor.to_dict()
        
        return result