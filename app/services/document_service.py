from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.documents import Document, DocumentType
from app.models.projects import Project
from app.models.quotations import Quotation
from app.services.base_service import BaseService
from app.utils import response
from datetime import datetime

class DocumentService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Document)

    def generate_document_number(self, doc_type_enum, doc_name):
        """
        Format: (Prefix Enum)-(4 huruf nama doc)-ISODATETIME
        Contoh: INV-SERT-20260302T113000
        """
        # 1. Ambil 3 huruf pertama dari Key Enum (Contoh: INVOICE -> INV, QUOTATION -> QUO)
        # Jika PO (2 huruf), dia tetap terambil PO
        type_prefix = doc_type_enum.name[:3].upper()

        # 2. Ambil 4 huruf pertama dari nama dokumen (hapus spasi)
        clean_name = "".join(doc_name.split())
        name_snippet = clean_name[:4].upper().ljust(4, 'X') # ljust: tambah X jika nama kurang dari 4 huruf

        # 3. Timestamp format ISO rapat (Tanpa timezone object untuk menghindari error Windows)
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

        return f"{type_prefix}-{name_snippet}-{timestamp}"

    def create(self, data):
        """Create Document dengan Validasi Enum dan Auto-Generate Number"""
        try:
            doc_type_raw = data.get('document_type')
            doc_name = data.get('name', 'DOC')

            # 1. Konversi input string ke Enum Object
            if doc_type_raw and isinstance(doc_type_raw, str):
                try:
                    # Mencari berdasarkan Key Enum (Misal input "INVOICE")
                    enum_obj = DocumentType[doc_type_raw.upper()]
                    data['document_type'] = enum_obj
                except KeyError:
                    # Jika tidak ketemu di Key, coba cari berdasarkan Value (Misal input "Invoice")
                    found = False
                    for member in DocumentType:
                        if member.value.lower() == doc_type_raw.lower():
                            data['document_type'] = member
                            found = True
                            break
                    if not found:
                        return response(400, f"Invalid document type. Allowed keys: {[e.name for e in DocumentType]}")

            # 2. Generate Number otomatis sebelum simpan
            # Pastikan kita sudah punya enum object untuk generate number
            current_enum = data.get('document_type', DocumentType.OTHER)
            if not data.get('number'):
                data['number'] = self.generate_document_number(current_enum, doc_name)

            # 3. Fix Timezone Error & Integer Casting
            # Gunakan datetime.now() langsung tanpa timezone key 'UTC' agar tidak error di Windows
            now = datetime.now()
            data['created_at'] = now
            data['updated_at'] = now

            for field in ['created_by', 'updated_by', 'project_id', 'quotation_id', 'agreement_id']:
                if field in data and data[field] is not None:
                    try:
                        data[field] = int(data[field])
                    except (ValueError, TypeError):
                        data[field] = None

            # 4. Kembalikan Enum ke bentuk string .name sebelum masuk ke super().create
            # agar sesuai dengan ekspektasi SQLAlchemy SQLEnum
            if isinstance(data.get('document_type'), DocumentType):
                data['document_type'] = data['document_type'].name

            return super().create(data)

        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")
            return response(500, f"Gagal simpan ke database: {str(e)}")

    def get_all_documents(self):
        """Get All dengan Serialisasi"""
        data = [x.to_dict() for x in self.db.query(Document).all()]
        return response(200, "Success", data)

    def get_document_by_id(self, id):
        """Get One dengan Serialisasi"""
        doc = self._get_by_id(id) 
        if not doc:
            return response(404, "Document not found", None)
        return response(200, "Success", doc.to_dict())

    def update(self, id, data):
        """Update Document"""
        if 'document_type' in data and isinstance(data['document_type'], str):
            try:
                data['document_type'] = DocumentType[data['document_type'].upper()]
            except KeyError:
                return response(400, "Invalid document type")
        return super().update(id, data)

    def delete(self, id):
        return super().delete(id)

    def get_document_list_filter(self, payload):
        """Search, Filter, and Pagination"""
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            document_types = payload.get('document_types', [])
            project_ids = payload.get('project_ids', [])
            quotation_ids = payload.get('quotation_ids', [])

            query = self.db.query(Document)\
                .outerjoin(Project, Document.project_id == Project.id)\
                .outerjoin(Quotation, Document.quotation_id == Quotation.id)

            if search_query:
                query = query.filter(Document.name.ilike(f"%{search_query}%"))

            if document_types:
                enum_list = []
                for dt in document_types:
                    key = dt.upper().replace(" ", "_")
                    if key in DocumentType.__members__:
                        enum_list.append(DocumentType[key])
                if enum_list:
                    query = query.filter(Document.document_type.in_(enum_list))

            if project_ids:
                query = query.filter(Document.project_id.in_(project_ids))
                
            if quotation_ids:
                query = query.filter(Document.quotation_id.in_(quotation_ids))

            sort_column = getattr(Document, sort_by) if hasattr(Document, sort_by) else Document.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))

            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            
            raw_data = query.offset(offset).limit(page_size).all()
            
            data_list = []
            for doc in raw_data:
                item = doc.to_dict()
                item["project_name"] = doc.project.name if doc.project else None
                item["quotation_summary"] = doc.quotation.summary if doc.quotation else None
                data_list.append(item)

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
            return response(500, f"Error processing document filter: {str(e)}")