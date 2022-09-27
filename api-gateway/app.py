from flask import Flask, request
from requests import get, post, put

app = Flask("__main__")
MS_AUTORIZADOR_HOST = "http://localhost:5000"
MS_USUARIO_HOST = "http://localhost:3000"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def proxy(path):
    print(request.headers)
    method = request.method

    # Peticion para obtener/destruir el token
    if path == 'autorizador/login' or path == 'autorizador/logout':
        return resolveRequest(MS_AUTORIZADOR_HOST, request, path)
    else:
        if validateToken(request):
            return resolveRequest(MS_USUARIO_HOST, request, path)
        else:
            return {"ERROR": "Un-Authorized"}, 403


def resolveRequest(micro, request_mod, path):
    method = request_mod.method
    new_url = f'{micro}/{path}'

    def switch(method):
        if method == 'GET':
            return get(url=new_url).content
        if method == 'POST':
            return post(url=new_url, data=request.data).content
        if method == 'PUT':
            return put(url=new_url, data=request.data).content

    switch(method)


def validateToken(request_mod):
    print(request_mod.headers['Authorization'])
    # TODO: validar el token
    return False


app.run(host="0.0.0.0", port=8080)
