import pandas as pd
import requests
import streamlit as st
from pprint import pprint

def fazer_requisição_ibge(url, params=None):
    resposta = requests.get(url, params=params)
    try:
        resposta.raise_for_status()
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro na requisição: {e}")
        return None
    else:
        resultado = resposta.json()
    return resultado

def pegar_nome_por_decada(nome):
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"
    nome_por_decada = fazer_requisição_ibge(url)
    if not nome_por_decada:
        return {}
    dict_decadas = {}
    for dados in nome_por_decada[0]['res']:
        decada = dados['periodo']
        frequencia = dados['frequencia']
        dict_decadas[decada] = frequencia
    return dict_decadas

def main():
    st.title("Frequência de Nomes no Brasil por Década ")
    st.write('Dados do IBGE (Fonte: https://servicodados.ibge.gov.br/api/docs/censos/nomes)')
    nome = st.text_input("Digite um nome para consultar:", value="Maria")
    if not nome:
        st.stop()
    dict_decadas = pegar_nome_por_decada(nome)
    #pprint(dict_decadas)
    df = pd.DataFrame.from_dict(dict_decadas, orient='index', columns=['Frequência'])
    if not dict_decadas:
        st.warning("Nenhum dado encontrado para o nome informado.")
        st.stop()
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.write('Freq. por Década')
        st.dataframe(df)
    with col2:
        st.write(f'Evolução da Frequência do nome {nome} por década')
        st.line_chart(df)

if __name__ == '__main__':
    main()
