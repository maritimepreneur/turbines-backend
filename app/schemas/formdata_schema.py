from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema


class FormDataSchema(BaseSchema):

    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("FormDataResponse", {
            **BaseSchema.get_schema(namespace),

            "data": fields.Nested(namespace.model("FormData", {
                "id": fields.Integer,
                "batch_number": fields.Integer,
                "timestamp": fields.DateTime,
                "nama_lengkap": fields.String,
                "nomor_whatsapp": fields.String,
                "tempat_lahir": fields.String,
                "jenis_kelamin": fields.String,
                "alamat_ktp": fields.String,
                "domisili": fields.String,
                "pendaftaran": fields.String,
                "prodi": fields.String,
                "status_pendidikan": fields.String,
                "instansi_pendidikan_akhir": fields.String,
                "link_cv": fields.String,

                "is_email_sent": fields.Boolean,
                "interview_datetime": fields.DateTime,

                "status": fields.String,
                "selection_status": fields.String(
                    enum=["Eligible", "Ineligible"]
                ),

                "meta": fields.Nested(namespace.model("Meta", {
                    "created_at": fields.String,
                    "updated_at": fields.String,
                    "created_by": fields.Integer,
                    "updated_by": fields.Integer,
                }))
            }, ordered=True))

        }, ordered=True)

    @classmethod
    def post_schema(cls, namespace: Model):

        return namespace.model("FormDataPostRequest", {

            "batch_number": fields.Integer(required=True),

            "timestamp": fields.DateTime(
                required=True,
                description="Submission time"
            ),

            "nama_lengkap": fields.String(required=True),
            "nomor_whatsapp": fields.String(required=True),

            "tempat_lahir": fields.String(required=True),

            "jenis_kelamin": fields.String(
                required=True,
                enum=["Laki-laki", "Perempuan"]
            ),

            "alamat_ktp": fields.String(required=True),
            "domisili": fields.String(required=True),

            "pendaftaran": fields.String(required=True),
            "prodi": fields.String(required=True),

            "status_pendidikan": fields.String(required=True),

            "instansi_pendidikan_akhir": fields.String(required=True),

            "link_cv": fields.String(required=True),

        }, ordered=True)


    @classmethod
    def filter_schema(cls, namespace: Model):

        return namespace.model("FormDataFilterRequest", {

            "page_size": fields.Integer(default=25),

            "page_number": fields.Integer(default=1),

            "search": fields.String(
                description="Search by nama_lengkap or nomor_whatsapp"
            ),

            "selection_status": fields.String(
                enum=["Eligible", "Ineligible"]
            ),

            "sort_by": fields.String(default="id"),

            "sort_order": fields.String(
                enum=["ASC", "DESC"],
                default="DESC"
            )

        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):

        item_model = namespace.model("FormDataFilterItem", {

            "id": fields.Integer,
            "batch_number": fields.Integer,
            "timestamp": fields.DateTime,

            "nama_lengkap": fields.String,
            "nomor_whatsapp": fields.String,

            "pendaftaran": fields.String,

            "status": fields.String,
            "selection_status": fields.String

        }, ordered=True)

        return namespace.model("FormDataFilterResponse", {

            **BaseSchema.get_schema(namespace),

            "data": fields.Nested(namespace.model("FormDataFilterData", {

                "list": fields.List(fields.Nested(item_model)),

                "pagination": fields.Nested(namespace.model("FormDataPagination", {

                    "current_page": fields.Integer,
                    "page_size": fields.Integer,
                    "total_pages": fields.Integer,
                    "total_items": fields.Integer

                }))

            }))

        }, ordered=True)