from flask_cors import CORS
from flask import Flask, jsonify
from flask_restful import Api, Resource
from modelos import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///micro-autorizador.db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app, resources={r'*': {"origins": "*"}})

api = Api(app)


@app.route('/autorizador/login')
class APILogin(Resource):
    def post(self):
        # TODO: Generar token
        return jsonify({"token": False})


@app.route('/autorizador/logout')
class APILogout(Resource):
    def post(self):
        # TODO:Destruir token
        return {"message": "Token destruido"}


@app.route('/autorizador/logout')
class APIValidate(Resource):
    def post(self, **kwargs):
        # TODO: Validar token
        return {"success": True}


if __name__ == '__main__':
    app.run(debug=True)
