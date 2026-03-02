from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.documents import Document, DocumentType
from app.models.projects import Project
from app.models.quotations import Quotation
from app.services.base_service import BaseService
from app.utils import response
from datetime import datetime # Tambahkan import ini

class DocumentService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Document)

    # --- Tambahkan Method Generator Ini ---
    def generate_document_number(self, doc_type_enum, doc_name):
        """
        Format: (DocumentType)-(4 huruf nama doc)-ISODATETIME
        Contoh: INV-SERT-20231027T103000
        """
        # 1. Ambil 3 huruf pertama dari tipe dokumen (contoh: INVOICE -> INV)
        type_code = doc_type_enum.name[:3].upper()

        # 2. Ambil 4 huruf pertama dari nama dokumen (hapus spasi dulu)
        clean_name = "".join(doc_name.split())
        name_code = clean_name[:4].upper().ljust(4, 'X') # ljust untuk jaga-jaga jika nama < 4 huruf

        # 3. Ambil ISO Timestamp (Format: YYYYMMDDTHHMMSS agar rapi di string)
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

        return f"{type_code}-{name_code}-{timestamp}"
    # ---------------------------------------

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

    def create(self, data):
        """Create Document dengan Validasi Enum dan Auto-Generate Number"""
        try:
            doc_type_raw = data.get('document_type')
            doc_name = data.get('name', 'DOC')

            # 1. Validasi Enum (Konversi String ke Enum Object untuk logika)
            if doc_type_raw and isinstance(doc_type_raw, str):
                try:
                    # Kita gunakan .upper() untuk jaga-jaga input huruf kecil
                    enum_obj = DocumentType[doc_type_raw.upper()]
                    data['document_type'] = enum_obj
                except KeyError:
                    return response(400, f"Invalid document type. Allowed: {[e.name for e in DocumentType]}")

            # 2. Generate Number (Hanya jika belum ada)
            if 'document_type' in data and not data.get('number'):
                # Pastikan data['document_type'] sudah berupa Enum object
                data['number'] = self.generate_document_number(data['document_type'], doc_name)

            # 3. FIX: Pastikan ID User adalah Integer, bukan String
            # Postgres sangat ketat, string '2' tidak dianggap sama dengan angka 2
            for field in ['created_by', 'updated_by', 'project_id', 'quotation_id']:
                if field in data and data[field] is not None:
                    try:
                        data[field] = int(data[field])
                    except (ValueError, TypeError):
                        data[field] = None # Set null jika data tidak valid

            # 4. Sesaat sebelum kirim ke base_service, 
            # Pastikan document_type adalah string/name-nya saja agar tidak error di driver SQL
            if isinstance(data.get('document_type'), DocumentType):
                data['document_type'] = data['document_type'].name

            return super().create(data)

        except Exception as e:
            # Print ke terminal untuk kamu cek error detailnya
            print(f"DEBUG ERROR: {str(e)}")
            return response(500, f"Gagal simpan ke database: {str(e)}")

    def update(self, id, data):
        """Update Document"""
        if 'document_type' in data and isinstance(data['document_type'], str):
            try:
                data['document_type'] = DocumentType[data['document_type']]
            except KeyError:
                return response(400, f"Invalid document type. Allowed: {[e.name for e in DocumentType]}")

        return super().update(id, data)

    def delete(self, id):
        """Delete Document"""
        return super().delete(id)

    def get_document_list_filter(self, payload):
        """Search, Filter, and Pagination for Documents"""
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