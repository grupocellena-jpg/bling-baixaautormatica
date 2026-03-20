import requests
import os
import time
from datetime import datetime

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
MAX_PAGINAS = 50

hoje = datetime.today().date()

while pagina <= MAX_PAGINAS:
    print(f"\n📄 Buscando página {pagina}...")

    url = f"{BASE_URL}/contas/receber?page={pagina}&limite=100"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Erro:", response.text)
        break

    data = response.json()
    contas = data.get("data", [])

    if not contas:
        print("\n✅ Fim das páginas.")
        break

    for conta in contas:
        try:
            vencimento = conta.get("dataVencimento")

            if not vencimento:
                continue

            data_venc = datetime.strptime(vencimento, "%Y-%m-%d").date()

            # 🎯 ATRASADO = venceu antes de hoje
            if data_venc >= hoje:
                continue

            conta_id = conta.get("id")

            print(f"💰 Baixando conta {conta_id} | Vencimento: {vencimento}")

            baixa_url = f"{BASE_URL}/contas/receber/{conta_id}/baixar"

            payload = {
                "valor": conta.get("valor"),
                "data": hoje.strftime("%Y-%m-%d")
            }

            baixa = requests.post(baixa_url, json=payload, headers=headers)

            if baixa.status_code in [200, 201]:
                print(f"✅ Baixado: {conta_id}")
                total_baixadas += 1
            else:
                print(f"⚠️ Erro ao baixar {conta_id}: {baixa.text}")

            time.sleep(0.2)

        except Exception as e:
            print("⚠️ Erro:", e)

    pagina += 1

print(f"\n🏁 FINALIZADO - {total_baixadas} contas baixadas")
