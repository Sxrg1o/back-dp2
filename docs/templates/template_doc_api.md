# Especificación (breve) — GET Roles
## META
- **Host (variable):**
    - **Prod:** `https://back-dp2.onrender.com`
    - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/roles`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna | Bearer JWT)
- **Notas:** En **GET** no enviar body. Usar **path/query params**.
**URL patrón (componentes separadas):**
```
{HOST}{BASE_PATH}{RECURSO}?skip={skip}&limit={limit}
````
## ENTRADA
```json  
{  
   "userId": "string",  
   "period": "string",  
   "callId": 0,  
   "refNumer": "string"  
}  
```
### Query Params
**DICTIONARY**

| Field | Data Type | Required | Format | Comment                       |
|------|-----------|----------|--------|-------------------------------|
| skip | integer   | NO       | >=0    | Offset (default `0`).         |
| limit| integer   | NO       | 1..100 | Tamaño de página (default 20).|
### Headers
**DICTIONARY**

| Field   | Data Type | Required | Format              | Comment            |
|---------|-----------|----------|---------------------|--------------------|
| accept  | string    | YES      | `application/json`  | Tipo de respuesta. |
> **Body:** *(no aplica en GET).*
## SALIDA (200 OK — ejemplo)
```json
{
  "items": [
    { "id": "uuid", "name": "string" }
  ],
  "skip": 0,
  "limit": 20,
  "total": 57
}
````
**DICTIONARY (OUTPUT)**

| Field        | Data Type | Format | Comment             |
| ------------ | --------- | ------ | ------------------- |
| items        | array     |        | Lista de roles.     |
| items[].id   | string    | uuid   | ID del rol.         |
| items[].name | string    |        | Nombre del rol.     |
| skip         | integer   |        | Offset aplicado.    |
| limit        | integer   |        | Tamaño de página.   |
| total        | integer   |        | Total de registros. |
## ERRORES (4xx/5xx)
**Problem+JSON (recomendado)**
```json
{
  "type": "https://back-dp2.onrender.com/errors/<code>",
  "title": "Bad Request",
  "status": 400,
  "detail": "...",
  "instance": "/api/v1/roles"
}
```

| HTTP | Code             | Title / Message        | Comment                      |
| ---: | ---------------- | ---------------------- | ---------------------------- |
|  400 | VALIDATION_ERROR | Parámetros inválidos   | `skip/limit` fuera de rango. |
|  401 | UNAUTHORIZED     | Token inválido/ausente | Si requiere auth.            |
|  404 | NOT_FOUND        | Recurso no encontrado  | Ruta/endpoint.               |
|  500 | INTERNAL_ERROR   | Error interno          | Revisar logs.                |
## URLs completas (listas para usar)
* **Producción:**
    * **URL completa:** `https://back-dp2.onrender.com/api/v1/roles?skip=0&limit=100`
    * **cURL:**
    ```bash
    curl -X GET \
      "https://back-dp2.onrender.com/api/v1/roles?skip=0&limit=100" \
      -H "accept: application/json"
    ```
* **Local:**
    * **URL completa:** `http://127.0.0.1:8000/api/v1/roles?skip=0&limit=100`
    * **cURL:**
    ```bash
    curl -X GET \
      "http://127.0.0.1:8000/api/v1/roles?skip=0&limit=100" \
      -H "accept: application/json"
    ```
## Variables y constantes (resumen)
* **Constantes:**
    * `BASE_PATH = /api/v1`
    * `RECURSO = /roles`
* **Variables:**
    * `HOST = https://back-dp2.onrender.com` *(prod)* | `http://127.0.0.1:8000` *(local)*
    * `skip`, `limit`
> Tip: define `HOST` por ambiente (env var) y construye la URL como:
> `"$HOST/api/v1/roles?skip=$SKIP&limit=$LIMIT"`.
 