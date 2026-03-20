import requests
import os
import time

# 🔐 Credenciais (GitHub Secrets)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

BASE_URL = "https://www.bling.com.br/Api/v3"

print("🤖 ROBÔ DE BAIXA INICIADO")

# 🔄 Gerar access_token
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

# 🚨 LIMITE DE SEGURANÇA (evita travar no GitHub)
MAX_PAGINAS = 50

while pagina <= MAX_PAGINAS:
    print(f"\n📄 Buscando página {pagina}...")

    url = f"{BASE_URL}/contas/receber?page={pagina}&limite=100"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Erro na requisição:", response.text)
        break

    data = response.json()
    contas = data.get("data", [])

    # 🛑 Para quando acabar
    if not contas:
        print("\n✅ Fim das páginas.")
        break

    for conta in contas:
        try:
            cliente = conta.get("contato", {})
            tipo = cliente.get("tipoPessoa")
            situacao = conta.get("situacao")

            # 🔍 NORMALIZAÇÃO
            tipo_str = str(tipo).upper() if tipo else ""
            situacao_str = str(situacao).upper() if situacao else ""

            # 🎯 FILTRO PF (flexível)
            if not any(x in tipo_str for x in ["F", "FISICA", "PF"]):
                continue

            # 🎯 FILTRO ATRASADO (flexível)
            if not any(x in situacao_str for x in ["ATRAS", "VENC", "ABERTO"]):
                continue

            conta_id = conta.get("id")

            print(f"💰 Baixando conta {conta_id}")

            # 🔻 Baixa
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

            # ⏳ evita bloqueio API
            time.sleep(0.2)

        except Exception as e:
            print("⚠️ Erro na conta:", e)

    pagina += 1

print(f"\n🏁 FINALIZADO - {total_baixadas} contas baixadas (somente PF)")
