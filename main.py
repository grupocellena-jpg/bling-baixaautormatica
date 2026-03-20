import requests
import os

print("🚀 VERSAO SEM REFRESH")
print("🤖 ROBÔ DE BAIXA INICIADO")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

BASE_URL = "https://www.bling.com.br/Api/v3"

# =========================
# BUSCAR CONTAS
# =========================
def buscar_contas():
    url = f"{BASE_URL}/contas/receber"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "pagina": 1
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    print("🔍 Buscando página 1...")

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
    contas, headers = buscar_contas()
    total = baixar_contas(contas, headers)

    print(f"✅ FINALIZADO - {total} contas baixadas")

if __name__ == "__main__":
    main()
