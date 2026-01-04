import requests
from pprint import pprint

nome = "Alexandre"
url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"

params = {
    'sexo': 'M',
    #'localidade':33,
    'groupBy':'UF',
}
resposta = requests.get(url, params=params)
try:
    resposta.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f'Erro na requisição {e}')
    resultado = None
else:
    resultado = resposta.json()
    pprint(resultado)