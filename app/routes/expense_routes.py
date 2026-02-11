from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.expense_service import ExpenseService
from app.schemas.expense_schema import ExpenseSchema
from app.utils import role_required

expense_ns = Namespace("expenses", description="Expense Management")
expense_svc = ExpenseService(db.session)

expense_response_schema = ExpenseSchema.get_schema(expense_ns)
expense_post_schema = ExpenseSchema.post_schema(expense_ns)

@expense_ns.route("/")
class ExpenseList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION")
    @expense_ns.doc(security="Bearer Auth")
    @expense_ns.marshal_list_with(expense_response_schema)
    def get(self):
        """ Get all expenses """
        return expense_svc.get_all_expenses()
    
@expense_ns.route("/create")
class ExpenseCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "FINANCE")
    @expense_ns.doc(security="Bearer Auth")
    @expense_ns.expect(expense_post_schema)
    @expense_ns.marshal_with(expense_response_schema)
    def post(self):
        """ Create a new expense """
        return expense_svc.create(expense_ns.payload)
    
@expense_ns.route("/<int:id>")
class ExpenseDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @expense_ns.doc(security="Bearer Auth")
    @expense_ns.marshal_with(expense_response_schema)
    def get(self, id):
        """ Get detail expense """
        return expense_svc.get_expense_by_id(id)
    
    @jwt_required()
    @role_required("ADMIN", "FINANCE")
    @expense_ns.doc(security="Bearer Auth")
    @expense_ns.expect(expense_post_schema)
    @expense_ns.marshal_with(expense_response_schema)
    def put(self, id):
        """ Update expense detail """
        return expense_svc.update(id, expense_ns.payload)

    @jwt_required()
    @role_required("ADMIN")
    @expense_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete a expense """
        return expense_svc.delete(id)