#!/bin/bash

# Funciones comunes para tests QA
# Autor: Kevin Antonio Navarro Carrera

# Función para obtener token de autenticación
# Uso: get_auth_token
# Retorna: ACCESS_TOKEN global variable
get_auth_token() {
    local email="${QA_EMAIL:-test@test.com}"
    local password="${QA_PASSWORD:-test123}"

    echo -n "Obteniendo token de autenticación... " >&2

    local response=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$email\", \"password\": \"$password\"}")

    ACCESS_TOKEN=$(echo "$response" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('access_token', ''))" 2>/dev/null)

    if [ -n "$ACCESS_TOKEN" ]; then
        echo -e "${GREEN}✓${NC}" >&2
        return 0
    else
        echo -e "${RED}✗ No se pudo obtener token${NC}" >&2
        echo "Response: $response" >&2
        return 1
    fi
}

# Función para hacer curl con autenticación
# Uso: curl_auth [curl options]
curl_auth() {
    if [ -n "$ACCESS_TOKEN" ]; then
        curl -H "Authorization: Bearer $ACCESS_TOKEN" "$@"
    else
        curl "$@"
    fi
}
