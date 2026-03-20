import requests
import os
import time

# 🔐 Dados do GitHub Secrets
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

BASE_URL = "https://www.bling.com.br/Api/v3"

print("🤖 ROBÔ DE BAIXA INICIADO")

# 🔄 GERAR ACCESS TOKEN
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

while True:
    print(f"\n📄 Buscando página {pagina}...")

    url = f"{BASE_URL}/contas/receber?page={pagina}&limite=100"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Erro na requisição:", response.text)
        break

    data = response.json()
    contas = data.get("data", [])

    # 🛑 PARADA
    if not contas:
        print("\n✅ Fim das páginas.")
        break

    for conta in contas:
        try:
            cliente = conta.get("contato", {})
            tipo = cliente.get("tipoPessoa")
            situacao = conta.get("situacao")

            # 🎯 FILTRO PF
            if tipo != "F":
                continue

            # 🎯 FILTRO ATRASADO
            if situacao != "ATRASADO":
                continue

            conta_id = conta.get("id")

            print(f"💰 Baixando conta {conta_id}")

            # 🔻 DAR BAIXA
            baixa_url = f"{BASE_URL}/contas/receber/{conta_id}/baixar"

            payload = {
                "valor": conta.get("valor"),
                "data": time.strftime("%Y-%m-%d")
            }

            baixa = requests.post(baixa_url, json=payload, headers=headers)

            if baixa.status_code in [200, 201]:
                print(f"✅ Baixado com sucesso: {conta_id}")
                total_baixadas += 1
            else:
                print(f"⚠️ Erro ao baixar {conta_id}: {baixa.text}")

            time.sleep(0.2)

        except Exception as e:
            print("⚠️ Erro na conta:", e)

    pagina += 1

print(f"\n🏁 Finalizado. Total baixadas: {total_baixadas}")
