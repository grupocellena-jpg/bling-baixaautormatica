import requests
import os

print("🚀 VERSAO NOVA RODANDO")
print("🤖 ROBÔ DE BAIXA INICIADO")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

BASE_URL = "https://www.bling.com.br/Api/v3"

# =========================
# GERAR TOKEN
# =========================
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

    print("🔄 Token gerado com sucesso")
    return resp_json["access_token"]

# =========================
# BUSCAR CONTAS
# =========================
def buscar_contas(token):
    url = f"{BASE_URL}/contas/receber"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "pagina": 1
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    print("🔍 Buscando página 1...")

    # 🔥 AQUI ESTÁ A CORREÇÃO
    contas = data.get("data", [])

    print(f"📊 {len(contas)} contas encontradas")

    return contas, headers

# =========================
# BAIXAR CONTAS
# =========================
def baixar_contas(contas, headers):
    total = 0

    for conta in contas:
        try:
            # 🔥 GARANTE QUE É DICIONÁRIO
            if not isinstance(conta, dict):
                continue

            situacao = conta.get("situacao")

            if situacao != "aberto":
                continue

            conta_id = conta.get("id")

            if not conta_id:
                continue

            url = f"{BASE_URL}/contas/receber/{conta_id}/baixar"

            response = requests.post(url, headers=headers)

            if response.status_code == 200:
                total += 1
                print(f"💰 Conta {conta_id} baixada")
            else:
                print(f"⚠️ Erro ao baixar {conta_id}:", response.text)

        except Exception as e:
            print("⚠️ ERRO:", e)

    return total

# =========================
# EXECUÇÃO
# =========================
def main():
    token = gerar_token()
    contas, headers = buscar_contas(token)

    total = baixar_contas(contas, headers)

    print(f"✅ FINALIZADO - {total} contas baixadas")

if __name__ == "__main__":
    main()
