from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from modelos import db, Usuario, UsuarioSchema
from flask_jwt_extended import create_access_token, JWTManager, jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///micro-autorizador.db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'frase-secreta'

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app, resources={r'*': {"origins": "*"}})

api = Api(app)

jwt = JWTManager(app)


@app.route('/autorizador/login', methods=['POST'])
def post():
    print(request.json["usuario"])
    usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                   Usuario.contrasena == request.json["contrasena"]).first()

    if usuario is None:
        return "El usuario no existe", 404
    else:
        token_de_acceso = create_access_token(identity=usuario.id,
                                              additional_claims={
                                                  "rol": usuario.rol.id
                                              })
        return {"status": "success", "token-access": token_de_acceso}


@app.route('/autorizador/logout')
class APILogout(Resource):
    def post(self):
        # TODO:Destruir token
        return {"message": "Token destruido"}


@app.route('/autorizador/validate')
@jwt_required()
def APIValidate():
    print(request.json["url"])

    return {"success": True}


if __name__ == '__main__':
    app.run(debug=True)
