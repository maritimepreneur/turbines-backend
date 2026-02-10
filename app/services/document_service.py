from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.documents import Document, DocumentType
from app.services.base_service import BaseService
from app.utils import response

class DocumentService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Document)

    def get_all_documents(self):
        """Get All dengan Serialisasi"""
        data = [x.to_dict() for x in self.db.query(Document).all()]
        return response(200, "Success", data)

    def get_document_by_id(self, id):
        """Get One dengan Serialisasi"""
        # Gunakan _get_by_id agar mendapatkan instance Model, bukan hasil fungsi response()
        doc = self._get_by_id(id) 
    
        if not doc:
            return response(404, "Document not found", None)
        
        return response(200, "Success", doc.to_dict())

    def create(self, data):
        """Create Document dengan Validasi Enum"""
        # Konversi string ke Enum jika data dikirim sebagai string (misal: "INVOICE")
        if 'document_type' in data and isinstance(data['document_type'], str):
            try:
                data['document_type'] = DocumentType[data['document_type']]
            except KeyError:
                return response(400, f"Invalid document type. Allowed: {[e.name for e in DocumentType]}")

        return super().create(data)

    def update(self, id, data):
        """Update Document"""
        # Validasi Enum saat update
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
        """Search & Filter dengan Pagination (Pola sama dengan Employee)"""
        try:
            q = self.db.query(Document)
            
            # 1. Search Logic (Mencari berdasarkan Nama Dokumen)
            if s := payload.get('search'):
                term = f"%{s}%"
                # Menggunakan ilike untuk case-insensitive search pada nama
                q = q.filter(Document.name.ilike(term))

            # 2. Filter Logic
            # Filter berdasarkan Tipe Dokumen
            if doc_types := payload.get('document_types'): # Expecting list of strings
                # Konversi list string ke list Enum untuk query
                enum_list = []
                for dt in doc_types:
                    if dt in DocumentType.__members__:
                        enum_list.append(DocumentType[dt])
                if enum_list:
                    q = q.filter(Document.document_type.in_(enum_list))
            
            # Filter berdasarkan Project ID
            if project_id := payload.get('project_id'):
                q = q.filter(Document.project_id == project_id)

            # 3. Sorting Logic
            sort_col = getattr(Document, payload.get('sort_by', 'id'), Document.id)
            sort_dir = payload.get('sort_order', 'DESC')
            q = q.order_by(asc(sort_col) if sort_dir == 'ASC' else desc(sort_col))
            
            # 4. Pagination Logic
            page = payload.get('page_number', 1)
            size = payload.get('page_size', 25)
            total = q.count()
            
            data = [x.to_dict() for x in q.offset((page - 1) * size).limit(size).all()]

            return response(200, "Success", {
                "list": data,
                "pagination": {
                    "current_page": page,
                    "page_size": size,
                    "total_pages": (total + size - 1) // size,
                    "total_items": total
                }
            })
        except Exception as e:
            return response(500, f"Error: {str(e)}")