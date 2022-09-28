from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    correo = db.Column(db.String(250))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)

class UsuarioSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True