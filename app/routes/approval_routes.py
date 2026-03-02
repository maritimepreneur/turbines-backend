from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from flask import request
from app.database import db
from app.services.approval_service import ApprovalService
from app.schemas.approval_schema import ApprovalSchema
from app.utils import role_required

approval_ns = Namespace("approvals", description="Approval Management")

service = ApprovalService(db.session)

approval_detail_schema = ApprovalSchema.get_schema(approval_ns)
approval_post_schema = ApprovalSchema.post_schema(approval_ns)
approval_update_schema = ApprovalSchema.update_schema(approval_ns)
approval_filter_schema = ApprovalSchema.filter_response_schema(approval_ns)

@approval_ns.route("/")
class ApprovalList(Resource):

    @jwt_required()
    @role_required("ADMIN", "FINANCE", "BIZDEV")
    @approval_ns.doc(security="Bearer Auth")
    @approval_ns.marshal_with(approval_filter_schema)
    def get(self):
        """ Get all approvals with pagination """
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        return service.get_all(page, per_page)

@approval_ns.route("/create")
class ApprovalCreate(Resource):

    @jwt_required()
    @role_required("ADMIN", "FINANCE", "BIZDEV")
    @approval_ns.doc(security="Bearer Auth")
    @approval_ns.expect(approval_post_schema)
    @approval_ns.marshal_with(approval_detail_schema)
    def post(self):
        """ Create new approval """
        return service.create(approval_ns.payload)


@approval_ns.route("/<int:id>")
class ApprovalDetail(Resource):

    @jwt_required()
    @role_required("ADMIN", "FINANCE", "BIZDEV")
    @approval_ns.doc(security="Bearer Auth")
    @approval_ns.marshal_with(approval_detail_schema)
    def get(self, id):
        """ Get approval detail """
        return service.get_by_id(id)

    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @approval_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete approval """
        return service.delete(id)

@approval_ns.route("/update/<int:id>")
class ApprovalUpdate(Resource):

    @jwt_required()
    @role_required("ADMIN", "FINANCE", "BIZDEV")
    @approval_ns.doc(security="Bearer Auth")
    @approval_ns.expect(approval_update_schema)
    @approval_ns.marshal_with(approval_detail_schema)
    def put(self, id):
        """ Update approval status """
        return service.update(id, approval_ns.payload)