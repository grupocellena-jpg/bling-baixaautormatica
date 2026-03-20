import requests
import os
import time
from datetime import datetime

print("🔥 VERSAO NOVA RODANDO")
print("🤖 ROBÔ DE BAIXA INICIADO")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

BASE_URL = "https://www.bling.com.br/Api/v3"

# =========================
# LEITURA DO TOKEN
# =========================
def ler_refresh_token():
    with open("refresh_token.txt", "r") as f:
        return f.read().replace("\n", "").replace("\r", "").strip()

def salvar_refresh_token(token):
    with open("refresh_token.txt", "w") as f:
        f.write(token.strip())

# =========================
# GERAR ACCESS TOKEN
# =========================
def gerar_token():
    refresh_token = ler_refresh_token()

    print("🔑 TOKEN LIDO:", repr(refresh_token))

    url = f"{BASE_URL}/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    resp_json = response.json()

    if "access_token" not in resp_json:
        print("❌ Erro ao gerar token:", resp_json)
        exit()

    novo_refresh = resp_json.get("refresh_token")

    if novo_refresh:
        print("🔄 Atualizando refresh_token automaticamente")
        salvar_refresh_token(novo_refresh)

    return resp_json["access_token"]

# =========================
# BUSCAR CONTAS
# =========================
def buscar_contas(access_token):
    pagina = 1
    total_baixadas = 0

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    while True:
        print(f"📄 Página {pagina}")

        url = f"{BASE_URL}/contas/receber"

        params = {
            "pagina": pagina,
            "situacao": "atrasado"
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        contas = data.get("data", [])

        if not contas:
            break

        for conta in contas:
            id_conta = conta.get("id")

            print(f"💰 Baixando conta {id_conta}")

            baixa_url = f"{BASE_URL}/contas/receber/{id_conta}/baixar"

            payload = {
                "valor": conta.get("valor"),
                "dataPagamento": datetime.now().strftime("%Y-%m-%d")
            }

            r = requests.post(baixa_url, headers=headers, json=payload)

            if r.status_code == 200:
                total_baixadas += 1
            else:
                print("⚠️ Erro ao baixar:", r.text)

        pagina += 1
        time.sleep(1)

    print(f"✅ FINALIZADO - {total_baixadas} contas baixadas")

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    token = gerar_token()
    buscar_contas(token)
