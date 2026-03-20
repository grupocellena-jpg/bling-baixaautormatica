import requests
from datetime import datetime
import time

print("🤖 ROBÔ INICIADO")

API_KEY = "b30e0a4ebee3e3ac23ad6fbce5b7b73542d5e078"
BASE_URL = "https://api.bling.com.br/Api/v3"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

pagina = 1
total = 0

while True:
    print(f"📄 Página {pagina}")

    url = f"{BASE_URL}/contas/receber?pagina={pagina}"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print("Erro:", resp.text)
        break

    contas = resp.json().get("data", [])

    if not contas:
        break

    hoje = datetime.today().date()

    for conta in contas:
        try:
            id_conta = conta.get("id")
            vencimento = conta.get("vencimento")
            situacao = conta.get("situacao")

            if situacao != 1:
                continue

            if not vencimento:
                continue

            venc_data = datetime.strptime(vencimento, "%Y-%m-%d").date()

            if venc_data <= hoje:
                print(f"💰 Baixando {id_conta}")

                url_baixa = f"{BASE_URL}/contas/receber/{id_conta}/baixar"

                payload = {
                    "data": datetime.today().strftime('%Y-%m-%d'),
                    "valor": conta.get("valor", 0)
                }

                r = requests.post(url_baixa, json=payload, headers=headers)

                if r.status_code == 200:
                    total += 1
                    print("✅ OK")
                else:
                    print("❌ Erro:", r.text)

                time.sleep(0.2)

        except Exception as e:
            print("Erro:", e)

    pagina += 1

print("🎯 Total baixadas:", total)
