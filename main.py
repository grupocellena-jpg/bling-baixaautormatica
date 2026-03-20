import requests
import os
import time
from datetime import datetime

print("🔥 VERSAO NOVA RODANDO")
print("🤖 ROBÔ DE BAIXA INICIADO")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

BASE_URL = "https://www.bling.com.br/Api/v3"

# =========================
# GERAR TOKEN
# =========================
def gerar_token():
    print("🔑 TOKEN (SECRET):", REFRESH_TOKEN[:10], "...")

    url = f"{BASE_URL}/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    resp = response.json()

    print("🔍 RESPOSTA TOKEN:", resp)

    if "access_token" not in resp:
        print("❌ ERRO AO GERAR TOKEN:", resp)
        exit()

    return resp["access_token"]

# =========================
# BUSCAR E BAIXAR CONTAS
# =========================
def buscar_contas(token):
    pagina = 1
    total_baixadas = 0

    headers = {
        "Authorization": f"Bearer {token}"
    }

    while True:
        print(f"\n📄 Buscando página {pagina}...")

        url = f"{BASE_URL}/contas/receber"

        params = {
            "pagina": pagina,
            "situacao": "atrasado"
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        print("🔍 RESPOSTA BRUTA:", data)

        contas = data.get("data", [])

        if not contas:
            print("🚫 Nenhuma conta encontrada, encerrando...")
            break

        print(f"📊 {len(contas)} contas encontradas")

        for conta in contas:
            try:
                # garante que é dict
                if not isinstance(conta, dict):
                    print("⚠️ Ignorando item inválido:", conta)
                    continue

                id_conta = conta.get("id")

                if not id_conta:
                    print("⚠️ Conta sem ID:", conta)
                    continue

                print(f"💰 Baixando conta {id_conta}")

                baixa_url = f"{BASE_URL}/contas/receber/{id_conta}/baixar"

                payload = {
                    "valor": conta.get("valor", 0),
                    "dataPagamento": datetime.now().strftime("%Y-%m-%d")
                }

                r = requests.post(baixa_url, headers=headers, json=payload)

                if r.status_code == 200:
                    print("✅ Baixada com sucesso")
                    total_baixadas += 1
                else:
                    print("⚠️ Erro ao baixar:", r.text)

                time.sleep(0.5)

            except Exception as e:
                print("⚠️ ERRO:", e)

        pagina += 1
        time.sleep(1)

    print(f"\n🏁 FINALIZADO - {total_baixadas} contas baixadas")

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    token = gerar_token()
    buscar_contas(token)
