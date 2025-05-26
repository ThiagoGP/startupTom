# ativador.py
import sys
import requests

if len(sys.argv) < 2:
    print("Erro: URL de ativação não fornecida.")
    sys.exit(1)

url_ativacao = sys.argv[1]

try:
    response = requests.get(url_ativacao)
    print("URL ativada com sucesso!")
    # print("Resposta:", response.text)
except Exception as e:
    print("Erro ao ativar a URL:", e)
