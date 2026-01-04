import requests

url = "https://www.google.com.br"

resposta = requests.get(url)

print(resposta, end="\n -----xxxxx------\n\n\n\n")

print(resposta.text)

with open('pagina_google.html', 'w') as arquivo:
    arquivo.write(resposta.text)