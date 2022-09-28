from flask_cors import CORS
from flask import Flask, jsonify
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

@app.route('/ubicacion-usuario/<id_usuario>')
def get(id_usuario):
    usuario = usuario_schema.dump(Usuario.query.get_or_404(id_usuario))
    return jsonify({"usuario": usuario})

if __name__ == '__main__':
    app.run(debug=True)