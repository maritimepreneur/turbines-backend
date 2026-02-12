from sqlalchemy.orm import Session
from app.models.expenses import Expense
from app.services.base_service import BaseService
from app.utils import response
from sqlalchemy import func
from datetime import date, datetime

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
        """ Create a new Expense """
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

        return super().create(expense_data)
    
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