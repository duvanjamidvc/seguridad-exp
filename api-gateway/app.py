import json

import jwt
from flask import Flask, request
from requests import get, post, put

app = Flask("__main__")
MS_AUTORIZADOR_HOST = "http://localhost:5000"
MS_USUARIO_HOST = "http://localhost:3000"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    print(request.headers)
    if path == 'autorizador/login' or path == 'autorizador/logout' or path == 'autorizador/validate':
        return resolveRequest(MS_AUTORIZADOR_HOST, request, path)
    else:
        if validateToken(request):
            return resolveRequest(MS_USUARIO_HOST, request, path)
        else:
            return {"ERROR": "Un-Authorized"}, 403


def resolveRequest(micro, request_mod, path):
    method = request_mod.method
    new_url = f'{micro}/{path}'
    print(f'>> {method}:{new_url}')

    def switch(method):
        if method == 'GET':
            return get(url=new_url, headers=request_mod.headers).content
        if method == 'POST':
            return post(url=new_url, data=request.data, headers=request_mod.headers).content
        if method == 'PUT':
            return put(url=new_url, data=request.data, headers=request_mod.headers).content

    return switch(method)


def validateToken(request_mod):
    print(request_mod.headers['Authorization'])
    header_token = request_mod.headers['Authorization']
    try:
        decoded = jwt.decode(header_token, options={"verify_signature": False})
    except jwt.exceptions.DecodeError:
        return False
    validateREsp = get(url=f'{MS_AUTORIZADOR_HOST}/autorizador/validate',
                       headers={'Authorization': header_token}).content
    data = json.loads(validateREsp)
    return data['valid'] | False


@app.after_request
def add_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response


app.run(host="0.0.0.0", port=8080)
