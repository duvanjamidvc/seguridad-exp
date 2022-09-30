from datetime import timedelta
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import jwt


from modelos import db, Usuario, UsuarioSchema, LogAccess
from flask_jwt_extended import create_access_token, JWTManager

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

jwtmanager = JWTManager(app)
usuario_scheme = UsuarioSchema()


def validatePath(usuario, targetPath):
    allowed = False
    for permiso in usuario['rol']['permisos']:
        if permiso['url'] == targetPath:
            allowed = True
            break
        else:
            allowed = False
    return allowed


def log(token, id, targetPath, allowed):
    accesLog = LogAccess(token=token, user_id=id, target=targetPath, allowed=allowed)
    db.session.add(accesLog)
    db.session.commit()


@app.route('/autorizador/login', methods=['POST'])
def login():
    print(request.json["usuario"])
    usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                   Usuario.contrasena == request.json["contrasena"]).first()

    if usuario is None:
        return {"message": "El usuario no existe"}, 404
    else:
        token_de_acceso = create_access_token(identity=usuario.id,
                                              additional_claims=usuario_scheme.dump(usuario),
                                              expires_delta=timedelta(minutes=1))
        usuario.token = token_de_acceso
        db.session.add(usuario)
        db.session.commit()
        return {"status": "success", "token-access": token_de_acceso}


@app.route('/autorizador/signin', methods=['POST'])
def signin():
    usuario = Usuario(usuario=request.json["usuario"],
                      contrasena=request.json["contrasena"])

    db.session.add(usuario)
    db.session.commit()
    token_de_acceso = create_access_token(identity=usuario.id,
                                          additional_claims=usuario_scheme.dump(usuario),
                                          expires_delta=timedelta(minutes=1))
    usuario.token = token_de_acceso
    return {"status": "success", "token-access": token_de_acceso}


@app.route('/autorizador/logout', methods=['GET'])
def logout():
    usuario = Usuario.query.filter(Usuario.token == request.headers["Authorization"]).first()
    if usuario:
        usuario.token = None
        db.session.add(usuario)
        db.session.commit()
    return {"success": True}


@app.route('/autorizador/validate', methods=['POST'])
def validate():
    authorization_token = request.headers["Authorization"]
    allowed = False
    user_id = None
    try:
        decoded = jwt.decode(authorization_token, options={"verify_signature": False})
        usuario = Usuario.query.filter(Usuario.token == authorization_token).first()
        print(usuario_scheme.dump(usuario))
        user_id = decoded['id']
        if usuario:
            targetPath = request.json['targetPath']
            allowed = validatePath(usuario_scheme.dump(usuario), targetPath)
        else:
            allowed = False
    except jwt.exceptions.DecodeError:
        allowed = False

    log(authorization_token, user_id, targetPath, allowed)
    if allowed:
        return {"valid": True}
    else:
        return {"valid": False}, 403


@app.route('/autorizador/actualizar-rol', methods=['POST'])
def update():
    usuario = Usuario.query.get_or_404(request.json.get('id_usuario'))
    usuario.id_rol = request.json.get("id_rol")
    db.session.commit()
    return usuario_scheme.dump(usuario)


@app.after_request
def add_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    app.run(debug=True)
