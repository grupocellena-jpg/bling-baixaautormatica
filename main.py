import requests
from datetime import datetime
import time
import os

print("🤖 ROBÔ INICIADO")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

# 🔁 GERAR NOVO ACCESS TOKEN
token_url = "https://www.bling.com.br/Api/v3/oauth/token"

token_data = {
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN
}

response = requests.post(token_url, data=token_data, auth=(CLIENT_ID, CLIENT_SECRET))
token_json = response.json()

access_token = token_json.get("access_token")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

BASE_URL = "https://api.bling.com.br/Api/v3"

pagina = 1
total_baixadas = 0

while True:
    print(f"\n📄 Página {pagina}")

    url = f"{BASE_URL}/contas/receber?page={pagina}"

    r = requests.get(url, headers=headers)
    data = r.json()

    contas = data.get("data", [])

    if not contas:
        break

    hoje = datetime.today().date()

    for conta in contas:
        try:
            id_conta = conta.get("id")
            vencimento = conta.get("dataVencimento")

            if not vencimento:
                continue

            # 🔍 PEGAR CLIENTE
            contato = conta.get("contato", {})

            cpf = contato.get("cpf")
            cnpj = contato.get("cnpj")

            # ❌ IGNORA PESSOA JURÍDICA
            if cnpj:
                print(f"🏢 Ignorado PJ: {id_conta}")
                continue

            # ❌ IGNORA SEM CPF
            if not cpf:
                print(f"⚠️ Sem CPF: {id_conta}")
                continue

            # 📅 VERIFICA VENCIMENTO
            venc_data = datetime.strptime(vencimento, "%Y-%m-%d").date()

            if venc_data <= hoje:
                print(f"💰 Baixando PF {id_conta}")

                url_baixa = f"{BASE_URL}/contas/receber/{id_conta}/baixar"

                payload = {
                    "data": hoje.strftime('%Y-%m-%d'),
                    "valor": conta.get("valor", 0)
                }

                r2 = requests.post(url_baixa, json=payload, headers=headers)

                if r2.status_code == 200:
                    total_baixadas += 1
                    print("✅ OK")
                else:
                    print("❌ Erro:", r2.text)

                time.sleep(0.2)

        except Exception as e:
            print("Erro:", e)

    pagina += 1

print(f"\n🏁 FINALIZADO - {total_baixadas} contas baixadas (somente PF)")
