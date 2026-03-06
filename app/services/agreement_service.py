from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.services.base_service import BaseService
from app.models.agreements import Agreement
from app.models.agreement_partners import AgreementPartner
from app.utils import response

class AgreementService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Agreement)

    def get_agreement_by_id(self, id: int):
        """Get Detail Agreement by ID"""
        try:
            agreement = self._get_by_id(id)
            if not agreement:
                return response(404, "Agreement not found")
            
            # Ambil daftar partner_id dari relasi pivot
            result = agreement.to_dict()
            result['partner_ids'] = [ap.partner_id for ap in agreement.agreement_partners]

            return response(200, "Success", result)
        except Exception as e:
            return response(500, f"Error retrieving agreement: {str(e)}")

    def get_agreement_list_filter(self, payload: dict):
        """Get Agreements with Filtering, Searching, and Pagination"""
        try:
            page_size = payload.get('page_size', 10)
            page_number = payload.get('page_number', 1)
            search_query = payload.get('search', '')
            sort_order = payload.get('sort_order', 'DESC')

            query = self.db.query(Agreement)

            if search_query:
                query = query.filter(
                    or_(
                        Agreement.name.ilike(f"%{search_query}%"),
                        Agreement.description.ilike(f"%{search_query}%")
                    )
                )

            # Sorting
            if sort_order.upper() == 'ASC':
                query = query.order_by(asc(Agreement.id))
            else:
                query = query.order_by(desc(Agreement.id))

            # Pagination Logic
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            
            raw_data = query.offset(offset).limit(page_size).all()

            data_list = []
            for item in raw_data:
                data_dict = item.to_dict()
                # Sertakan partner_ids dalam list jika diperlukan
                data_dict['partner_ids'] = [ap.partner_id for ap in item.agreement_partners]
                data_list.append(data_dict)

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
            return response(500, f"Error filtering agreements: {str(e)}")

    def create_agreement(self, data: dict):
        """Create Agreement and its Partner relations"""
        try:
            # Ekstrak partner_ids dari payload
            partner_ids = data.pop("partner_ids", [])

            new_agreement = Agreement(**data)
            self.db.add(new_agreement)
            
            # Flush untuk mendapatkan ID sebelum commit
            self.db.flush()

            # Insert ke tabel pivot agreement_partners
            if partner_ids:
                for p_id in partner_ids:
                    new_partner_rel = AgreementPartner(
                        agreement_id=new_agreement.id, 
                        partner_id=p_id
                    )
                    self.db.add(new_partner_rel)

            self.db.commit()
            self.db.refresh(new_agreement)

            return response(201, "Agreement created successfully", new_agreement.to_dict())

        except Exception as e:
            self.db.rollback()
            return response(500, f"Error creating agreement: {str(e)}")

    def update_agreement(self, id: int, data: dict):
        """Update Agreement and refresh Partner relations"""
        try:
            agreement = self._get_by_id(id)
            if not agreement:
                return response(404, "Agreement not found")

            partner_ids = data.pop("partner_ids", None)

            # Update main attributes
            for key, value in data.items():
                if hasattr(agreement, key):
                    setattr(agreement, key, value)

            # Sync Partner Relations
            if partner_ids is not None:
                # Remove old relations
                self.db.query(AgreementPartner).filter_by(agreement_id=id).delete()
                
                # Add new relations
                for p_id in partner_ids:
                    self.db.add(AgreementPartner(agreement_id=id, partner_id=p_id))

            self.db.commit()
            self.db.refresh(agreement)
            
            return response(200, "Agreement updated successfully", agreement.to_dict())

        except Exception as e:
            self.db.rollback()
            return response(500, f"Error updating agreement: {str(e)}")

    def delete_agreement(self, id: int):
        """Delete Agreement and its associated relations"""
        try:
            agreement = self._get_by_id(id)
            if not agreement:
                return response(404, "Agreement not found")

            # Hapus relasi pivot terlebih dahulu
            self.db.query(AgreementPartner).filter_by(agreement_id=id).delete()
            
            self.db.delete(agreement)
            self.db.commit()

            return response(200, "Agreement deleted successfully")
        except Exception as e:
            self.db.rollback()
            return response(500, f"Error deleting agreement: {str(e)}")