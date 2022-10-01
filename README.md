# Seguridad

## Microservicios

### Api-gateway

Para ejecutarlo entrar a la carpeta /api-gateway y ejecutar el comando: ``flask run -p 8080``, sirve como un proxy para las peticiones

### Autorizador

Para ejecutarlo entrar a la /carpeta y ejecutar el comando : ``flask run -p 5000``

1. Endpoints propuestos

```bash
-- POST: /autorizador/login BODY {usuario:string, password:string}
-- POST: /autorizador/logout header:{Authorization: [token]}
-- GET: /autorizador/validate/{TOKEN} 
-- POST: /autorizador/actualizar-rol header:{Authorization: [token]} BODY {id_rol:number, id_usuario:number}
```

### Usuario

Para ejecutarlo entrar a la carpeta /usuario y ejecutar el comando : ``flask run -p 3000``

1. Endpoints propuestos

```bash
-- GET: /usuarios
```
