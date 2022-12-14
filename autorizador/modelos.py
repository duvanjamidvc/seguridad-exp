from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

roles_permisos = db.Table('rol_permiso',
                          db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'), primary_key=True),
                          db.Column('permiso_id', db.Integer, db.ForeignKey('permiso.id'), primary_key=True))


class Permiso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    url = db.Column(db.String(128))
    roles = db.relationship('Rol', secondary='rol_permiso', back_populates="permisos")


class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    activo = db.Column(db.Boolean, default=True)
    permisos = db.relationship('Permiso', secondary='rol_permiso', back_populates="roles")


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    token = db.Column(db.String(500))
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'))
    rol = db.relationship('Rol', foreign_keys=[id_rol], single_parent=True)


class LogAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50))
    user_id = db.Column(db.Numeric())
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now())
    target = db.Column(db.String(500))
    allowed = db.Column(db.Boolean())


class PermisoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Permiso
        include_relationships = True
        load_instance = True


class EnumATipoUsuario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value


class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        include_relationships = True
        load_instance = True

    permisos = fields.List(fields.Nested(PermisoSchema()))


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

    rol = fields.Nested(RolSchema())


class ResponseSchema(Schema):
    message = fields.Str(default='Success')


class RequestSchema(Schema):
    api_type = fields.String(required=True, description="API type of awesome API")
