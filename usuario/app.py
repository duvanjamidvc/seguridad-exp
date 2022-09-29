from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_restful import Api

from modelos import db, UsuarioSchema, Usuario

usuario_schema = UsuarioSchema()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///micro-usuario.db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app, resources={r'*': {"origins": "*"}})

api = Api(app)

usuario_schema = UsuarioSchema()


@app.route('/usuarios', methods=['GET'])
def get():
    return [usuario_schema.dump(usuario) for usuario in Usuario.query.all()]


@app.route('/crear-usuario', methods=['POST'])
def post():
    new_usuario = Usuario(nombre=request.json["nombre"], correo=request.json["correo"], latitud=request.json["latitud"],
                          longitud=request.json["longitud"])
    db.session.add(new_usuario)
    db.session.commit()
    return usuario_schema.dump(new_usuario)


if __name__ == '__main__':
    app.run(debug=True)
