import requests
import os
import time
from datetime import datetime

print("🔥 USANDO ARQUIVO LOCAL")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

BASE_URL = "https://www.bling.com.br/Api/v3"


# =========================
# TOKEN (AUTOMÁTICO)
# =========================

def ler_refresh_token():
    with open("refresh_token.txt", "r") as f:
        return f.read().strip()


def salvar_refresh_token(token):
    with open("refresh_token.txt", "w") as f:
        f.write(token)


def gerar_token():
    refresh_token = ler_refresh_token()

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
# EXECUÇÃO
# =========================

access_token = gerar_token()

headers = {
    "Authorization": f"Bearer {access_token}"
}

pagina = 1
total_baixadas = 0

while True:
    print(f"\n📄 Página {pagina}")

    url = f"{BASE_URL}/contas/receber?page={pagina}&limite=100"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Erro ao buscar contas:", response.text)
        break

    data = response.json()
    contas = data.get("data", [])

    if not contas:
        print("✅ Sem mais contas")
        break

    for conta in contas:
        try:
            conta_id = conta.get("id")
            situacao = conta.get("situacao", {}).get("descricao", "")
            valor = conta.get("valor", 0)

            print(f"🔎 Conta {conta_id} - {situacao} - R$ {valor}")

            # 🔥 SOMENTE ATRASADAS
            if "Atrasad" not in situacao:
                continue

            print(f"💰 Baixando {conta_id}")

            baixa_url = f"{BASE_URL}/contas/receber/{conta_id}/baixar"

            payload = {
                "valor": valor,
                "data": datetime.now().strftime("%Y-%m-%d")
            }

            baixa = requests.post(baixa_url, json=payload, headers=headers)

            print("📥 RESPOSTA:", baixa.status_code, baixa.text)

            if baixa.status_code in [200, 201]:
                print(f"✅ BAIXADO {conta_id}")
                total_baixadas += 1
            else:
                print(f"⚠️ NÃO BAIXOU {conta_id}")

            time.sleep(0.3)

        except Exception as e:
            print("⚠️ ERRO:", e)

    pagina += 1

print(f"\n🏁 FINALIZADO - {total_baixadas} contas baixadas")
