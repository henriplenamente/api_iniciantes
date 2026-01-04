import requests

url = "https://httpbin.org/esta-url/nao-existe"
#url = "https://httpbin.org/get"

resposta = requests.get(url)

try:
    resposta.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f'Impossível fazer a requisição!\n Erro: {e}')
else:
    print("Resultado:")
    print(resposta.json())