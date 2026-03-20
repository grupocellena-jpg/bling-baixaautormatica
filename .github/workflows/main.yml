import requests
import os
from datetime import datetime
import time

# 🔐 VEM DO GITHUB SECRETS
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

BASE_URL = "https://www.bling.com.br/Api/v3"

# 🔄 GERAR ACCESS TOKEN
def gerar_token():
    url = "https://www.bling.com.br/Api/v3/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    resp_json = response.json()

    access_token = resp_json.get("access_token")

    if not access_token:
        print("❌ Erro ao gerar token:", resp_json)
        exit()

    return access_token


# 🚀 INÍCIO
print("🤖 ROBÔ DE BAIXA INICIADO")

token = gerar_token()

headers = {
    "Authorization": f"Bearer {token}"
}

hoje = datetime.today().date()

pagina = 1
total_baixadas = 0

while True:
    print(f"\n📄 Buscando página {pagina}...")

    url = f"{BASE_URL}/contas/receber?page={pagina}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Erro ao buscar contas:", response.text)
        break

    dados = response.json()
    contas = dados.get("data", [])

    if not contas:
        print("✅ Fim das páginas")
        break

    for conta in contas:
        try:
            id_conta = conta.get("id")
            vencimento = conta.get("vencimento")
            valor = conta.get("valor", 0)

            cliente = conta.get("contato", {})
            tipo_pessoa = cliente.get("tipoPessoa")  # F = Física, J = Jurídica

            # ❌ IGNORA PJ
            if tipo_pessoa != "F":
                continue

            # 📅 DATA
            venc_data = datetime.strptime(vencimento, "%Y-%m-%d").date()

            # 🔥 REGRA: TODAS VENCIDAS
            if venc_data <= hoje:
                print(f"💰 Baixando PF {id_conta} | Venc: {vencimento}")

                url_baixa = f"{BASE_URL}/contas/receber/{id_conta}/baixar"

                payload = {
                    "data": hoje.strftime("%Y-%m-%d"),
                    "valor": valor
                }

                r = requests.post(url_baixa, json=payload, headers=headers)

                if r.status_code == 200:
                    print("✅ OK")
                    total_baixadas += 1
                else:
                    print("❌ Erro:", r.text)

                time.sleep(0.2)

        except Exception as e:
            print("⚠️ Erro na conta:", e)

    pagina += 1

print(f"\n🏁 FINALIZADO | Total baixadas: {total_baixadas}")
