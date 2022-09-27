# Seguridad

## Microservicios

### Api-gateway

para correrlo entrar a la carpeta y correr : ``flask run``, sirve como un proxy para las peticiones

### Autorizador

para correrlo entrar a la carpeta y correr : ``flask run``

1. Endpoints propuestos

```bash
-- POST: /autorizador/login {usuario:string, password:string}
-- POST: /autorizador/logout header:{Authorization: [token]}
-- GET: /autorizador/validate/{TOKEN} 
```

### Usuario

aun sin hacer

