import requests

url = 'https://httpbin.org/get'
#resposta = requests.get(url)
#print(resposta.json())
#print(resposta.status_code)

params = {
    "dataInicio": "2025-01-01",
    "dataFim": "2025-12-31",
}

data = {
    "meus_dados": [1, 2, 3],
    "pessoa":{
        "nome": "Juliano",
        "professor": True
    }
}
resposta = requests.post(url, json=data, params=params)
print(resposta.request.url)
#print(resposta.json())

print(resposta.text)

print(resposta.status_code)

resposta.raise_for_status()