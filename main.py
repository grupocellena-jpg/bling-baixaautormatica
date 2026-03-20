import requests
import os
import time
from datetime import datetime

print("🚀 VERSAO NOVA RODANDO")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

BASE_URL = "https://www.bling.com.br/Api/v3"

print("🤖 ROBÔ DE BAIXA INICIADO")

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
total_baixadas = 0

# 🚀 Limite alto pra pegar tudo
MAX_PAGINAS = 50

while pagina <= MAX_PAGINAS:
    print(f"\n📄 Buscando página {pagina}...")

    url = f"{BASE_URL}/contas/receber?page={pagina}&limite=100"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Erro:", response.text)
        break

    data = response.json()
    contas = data.get("data", [])

    print(f"📊 {len(contas)} contas encontradas")

    if not contas:
        print("✅ Sem mais contas")
        break

    for conta in contas:
        try:
            conta_id = conta.get("id")
            situacao = conta.get("situacao", {}).get("descricao", "")
            valor = conta.get("valor", 0)

            print(f"🔎 Conta {conta_id} - Situação: {situacao} - Valor: {valor}")

            # 🔥 FILTRO: SOMENTE ATRASADAS
            if "Atrasad" not in situacao:
                continue

            print(f"💰 Tentando baixar conta {conta_id}")

            baixa_url = f"{BASE_URL}/contas/receber/{conta_id}/baixar"

            payload = {
                "valor": valor,
                "data": datetime.now().strftime("%Y-%m-%d")
            }

            baixa = requests.post(baixa_url, json=payload, headers=headers)

            print("📥 RESPOSTA:", baixa.status_code, baixa.text)

            if baixa.status_code in [200, 201]:
                print(f"✅ BAIXOU: {conta_id}")
                total_baixadas += 1
            else:
                print(f"⚠️ NÃO BAIXOU: {conta_id}")

            time.sleep(0.3)

        except Exception as e:
            print("⚠️ ERRO:", e)

    pagina += 1

print(f"\n🏁 FINALIZADO - {total_baixadas} contas baixadas")
