from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ETipoUsuario(enum.Enum):
    ADMINISTRADOR = "OPERADOR"
    APOSTADOR = "CLIENTE"


class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    activo = db.Column(db.Boolean, default=True)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    nombre = db.Column(db.String(250))
    correo = db.Column(db.String(250))
    tipo_usuario = db.Column(db.Enum(ETipoUsuario), default=ETipoUsuario.ADMINISTRADOR)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'))


class EnumATipoUsuario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value


class UsuarioSchema(SQLAlchemyAutoSchema):
    tipo_usuario = EnumATipoUsuario(attribute=("tipo_usuario"))

    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True


class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        include_relationships = True
        load_instance = True


class ResponseSchema(Schema):
    message = fields.Str(default='Success')


class RequestSchema(Schema):
    api_type = fields.String(required=True, description="API type of awesome API")
