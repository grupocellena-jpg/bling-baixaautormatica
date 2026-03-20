import requests
import os
import time

# 🔐 Dados do GitHub Secrets
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

BASE_URL = "https://www.bling.com.br/Api/v3"

print("🤖 ROBÔ DE BAIXA INICIADO")

# 🔄 GERAR TOKEN
def gerar_token():
    url = f"{BASE_URL}/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    resp_json = response.json()

    if "access_token" not in resp_json:
        print("❌ Erro ao gerar token:", resp_json)
        exit()

    return resp_json["access_token"]

access_token = gerar_token()

headers = {
    "Authorization": f"Bearer {access_token}"
}

pagina = 1

while True:
    print(f"\n📄 Buscando página {pagina}...")

    url = f"{BASE_URL}/contas/receber?page={pagina}&limite=100"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Erro na requisição:", response.text)
        break

    data = response.json()
    contas = data.get("data", [])

    # 🛑 PARA SE ACABAR
    if not contas:
        print("\n✅ Fim das páginas.")
        break

    for conta in contas:
        print("\n==============================")
        print("🔍 DEBUG CONTA COMPLETA:")
        print(conta)

        cliente = conta.get("contato", {})
        tipo = cliente.get("tipoPessoa")
        situacao = conta.get("situacao")

        print("👉 tipoPessoa:", tipo)
        print("👉 situacao:", situacao)

        # 🚨 PARA AQUI PRA ANALISAR
        break

    # 🚨 PARA SÓ NA PRIMEIRA PÁGINA
    break
