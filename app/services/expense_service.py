from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc, asc
from app.models.expenses import Expense
from app.services.base_service import BaseService
from app.utils import response
from datetime import date, datetime
from app.services.approval_service import ApprovalService

class ExpenseService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Expense)

    def generate_code(self, period_date: date) -> str:
        prefix = f"EXP-{period_date.strftime('%Y%m')}"

        last_code = (
            self.db.query(Expense.code)
            .filter(Expense.code.like(f"{prefix}-%"))
            .order_by(Expense.code.desc())
            .first()
        )

        if not last_code:
            sequence = 1
        else:
            last_seq = int(last_code[0].split("-")[-1])
            sequence = last_seq + 1

        return f"{prefix}-{sequence:04d}"
    
    def get_all_expenses(self):
        """ Get all Expense """
        expenses = self.db.query(Expense).all()
        return response(200, "Success", expenses or [])
    
    def create(self, expense_data: dict):
        period_date = expense_data.get("period_date")

        if not period_date:
            return response(400, "period_date is required")
        
        try:
            if isinstance(period_date, str):
                period_date = datetime.strptime(period_date, "%Y-%m-%d").date()
                expense_data["period_date"] = period_date
        except ValueError:
            return response(400, "Invalid period_date format. Use YYYY-MM-DD")
        
        expense_data["code"] = self.generate_code(period_date)

        result = super().create(expense_data)

        
        try:

            new_expense_id = result.get('data', {}).get('id')

            if new_expense_id:
                approval_service = ApprovalService(self.db)
                approval_payload = {
                    "entity_type": "Expense",
                    "expense_id": new_expense_id,
                    "quotation_id": 0,
                    "po_id": 0,
                    "invoice_id": 0
                }
                
                approval_service.create(approval_payload)
                
        except Exception as e:
            print(f"Warning: Automatic Approval for Expense failed: {str(e)}")

        return result
    
    def get_expense_by_id(self, expense_id):
        """ Get Expense details """
        expense = self._get_by_id(expense_id)
        if not expense:
            return response(404, "Expense not found")
        return super().get_by_id(expense_id)
    
    def update_expense_by_id(self, expense_id, updated_data):
        """ Update Expense """
        expense = self._get_by_id(expense_id)
        if not expense:
            return response(404, expense_id)
        
        updated_data.pop("code", None)

        return super().update(expense_id, updated_data)

    def get_expense_list_filter(self, payload):
        """NEW: Search, Filter, and Pagination for Expenses"""
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            
            search_query = payload.get('search', '')
            statuses = payload.get('statuses', [])
            period_start = payload.get('period_start')
            period_end = payload.get('period_end')
            min_amount = payload.get('min_amount')
            max_amount = payload.get('max_amount')

            query = self.db.query(Expense)

            if search_query:
                query = query.filter(
                    or_(
                        Expense.code.ilike(f"%{search_query}%"),
                        Expense.notes.ilike(f"%{search_query}%")
                    )
                )

            if statuses:
                query = query.filter(Expense.status.in_(statuses))
            
            if period_start and period_end:
                query = query.filter(Expense.period_date.between(period_start, period_end))
            elif period_start:
                query = query.filter(Expense.period_date >= period_start)
            elif period_end:
                query = query.filter(Expense.period_date <= period_end)

            if min_amount is not None:
                query = query.filter(Expense.total_amount >= min_amount)
            if max_amount is not None:
                query = query.filter(Expense.total_amount <= max_amount)

            sort_column = getattr(Expense, sort_by) if hasattr(Expense, sort_by) else Expense.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            raw_data = query.offset(offset).limit(page_size).all()
            data_list = [exp.to_dict() for exp in raw_data]

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
            return response(500, f"Error processing expense filter: {str(e)}")