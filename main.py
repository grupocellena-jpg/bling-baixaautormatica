import requests
import os
from datetime import datetime

print("🔥 NOVO FLUXO DIRETO (SEM ARQUIVO)")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

BASE_URL = "https://www.bling.com.br/Api/v3"

def gerar_token():
    print("🔑 TOKEN (SECRET):", REFRESH_TOKEN[:10], "...")

    url = f"{BASE_URL}/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    resp = response.json()

    if "access_token" not in resp:
        print("❌ ERRO TOKEN:", resp)
        exit()

    return resp["access_token"]

def buscar_contas(token):
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{BASE_URL}/contas/receber"

    params = {
        "pagina": 1,
        "situacao": "atrasado"
    }

    r = requests.get(url, headers=headers, params=params)

    print("📄 RESPOSTA:", r.json())

if __name__ == "__main__":
    token = gerar_token()
    buscar_contas(token)
