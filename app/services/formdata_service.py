from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

from app.models.formdata import FormData, SelectionStatus
from app.services.base_service import BaseService
from app.utils import response


class FormDataService(BaseService):

    def __init__(self, db: Session):
        super().__init__(db, FormData)


    def get_all_formdata(self):

        forms = (
            self.db.query(FormData)
            .order_by(desc(FormData.id))
            .all()
        )

        return {
            "message": "Success",
            "code": 200,
            "status": "success",
            "data": [f.to_dict() for f in forms]
        }

    def create_formdata(self, data):
        current_user_id = get_jwt_identity()

        existing = (
            self.db.query(FormData)
            .filter(FormData.nomor_whatsapp == data.get("nomor_whatsapp"))
            .first()
        )

        if existing:
            return response(400, "This WhatsApp number has already registered")

        new_form = FormData(
            batch_number=data.get("batch_number"),
            nama_lengkap=data.get("nama_lengkap"),
            nomor_whatsapp=data.get("nomor_whatsapp"),
            tempat_lahir=data.get("tempat_lahir"),
            jenis_kelamin=data.get("jenis_kelamin"),
            alamat_ktp=data.get("alamat_ktp"),
            domisili=data.get("domisili"),
            pendaftaran=data.get("pendaftaran"),
            prodi=data.get("prodi"),
            status_pendidikan=data.get("status_pendidikan"),
            instansi_pendidikan_akhir=data.get("instansi_pendidikan_akhir"),
            link_cv=data.get("link_cv"),
            timestamp=datetime.utcnow(),
            status="Pending",
            created_by=current_user_id
        )

        self.db.add(new_form)
        self.db.commit()

        return {
            "message": "Form Data created successfully",
            "code": 201,
            "status": "success",
            "data": new_form.to_dict()
        }

    def get_formdata_by_id(self, form_id):

        form = self._get_by_id(form_id)

        if not form:
            return response(404, "FormData not found", None)

        return response(200, "Success", form.to_dict())

    def update_selection(self, form_id, data):

        form = self._get_by_id(form_id)

        if not form:
            return response(404, f"FormData ID {form_id} not found")

        try:
            if "selection_status" in data:
                data["selection_status"] = SelectionStatus(data["selection_status"])
        except ValueError:
            return response(400, "Invalid selection status")

        if "interview_datetime" in data:
            form.interview_datetime = data["interview_datetime"]

        data["updated_by"] = get_jwt_identity()

        return super().update(form_id, data)

    def get_formdata_list_filter(self, payload):

        try:
            page_size = payload.get("page_size", 25)
            page_number = payload.get("page_number", 1)
            sort_by = payload.get("sort_by", "id")
            sort_order = payload.get("sort_order", "DESC")
            search_query = payload.get("search", "")
            selection_status = payload.get("selection_status")

            query = self.db.query(FormData)

            if search_query:
                query = query.filter(
                    or_(
                        FormData.nama_lengkap.ilike(f"%{search_query}%"),
                        FormData.nomor_whatsapp.ilike(f"%{search_query}%")
                    )
                )

            if selection_status:
                try:
                    query = query.filter(
                        FormData.selection_status == SelectionStatus(selection_status)
                    )
                except ValueError:
                    pass

            sort_column = getattr(FormData, sort_by) if hasattr(FormData, sort_by) else FormData.id

            query = query.order_by(
                desc(sort_column) if sort_order.upper() == "DESC" else asc(sort_column)
            )

            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size

            raw_data = query.offset(offset).limit(page_size).all()

            data_list = [f.to_dict() for f in raw_data]

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
            return response(500, f"Error processing formdata filter: {str(e)}")
        
    def delete_formdata(self, form_id):

        form = self._get_by_id(form_id)

        if not form:
            return response(404, f"FormData ID {form_id} not found")

        self.db.delete(form)
        self.db.commit()

        return response(200, "FormData deleted successfully")