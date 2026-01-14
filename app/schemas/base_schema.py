from flask_restx import fields, Model

class BaseSchema:
    """ Schema for consistent response """
    
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model(cls.__name__, {
            "code": fields.Integer(example=200),
            "message": fields.String(example="Success"),
            "data": fields.Raw() 
        })