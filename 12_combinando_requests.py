import requests
from pprint import pprint

def fazer_request(url, params=None):
    resposta = requests.get(url, params=params)
    try:
        resposta.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Erro na requisição: {e}")
        resultado = None
    else:
        resultado = resposta.json()
    return resultado

def pegar_id_estados():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    dados_estados = fazer_request(url, params={'view':'nivelado'})
    dict_estados = {}
    for dados in dados_estados:
        id_estado = dados['UF-id']
        nome_estado = dados['UF-nome']
        dict_estados[id_estado] = nome_estado
    return dict_estados

def pegar_frequencia_nomes_por_estado(nome):
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"
    frequencia_nomes_por_estado = fazer_request(url, params={'groupBy': 'UF'})
    dict_frequencia_nomes = {}
    for dados in frequencia_nomes_por_estado:
        id_estado = int(dados['localidade'])
        frequencia = dados['res'][0]['proporcao']
        dict_frequencia_nomes[id_estado] = frequencia
    return dict_frequencia_nomes

def main(nome):
    dict_estados = pegar_id_estados()
    dict_frequencia = pegar_frequencia_nomes_por_estado(nome)
    print(f'--- Frequência do nome "{nome}" no Estados (por 100.000 habitantes)')
    for id_estado, nome_estado in dict_estados.items():
        #frequencia_estado = dict_frequencia[id_estado]
        frequencia_estado = dict_frequencia.get(id_estado, 0)
        pprint(f'--> {nome_estado
        }: {frequencia_estado}')

if __name__ == '__main__':
    main('Felipe')
11