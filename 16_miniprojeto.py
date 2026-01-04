# Miniprojeto - web app com tempo com OpenWeather

import os
import requests
from pprint import pprint

import streamlit as st
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

def fazer_request(url, params=None):
    resposta = requests.get(url, params)
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f"Erro no request: {e}")
        resultado = None
    
    else:
        resultado = resposta.json()
    return resultado

def pegar_tempo_para_local(local):
    token = os.environ.get('CHAVE_API_WEATHER')
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': local,
        'units': 'metric',
        'appid': token,
        'lang': 'pt_br',
    }
    dados_tempo = fazer_request(url, params)
    return dados_tempo

def main():
    st.title("Previsão do Tempo com OpenWeather")
    st.write("Dados fornecidos por OpenWeather (fonte: https://openweathermap.org/)")
    
    local = st.text_input("Digite o nome da cidade:", value="Brasília")
           
    # if st.button("Obter Previsão do Tempo"):
    #     dados_tempo = pegar_tempo_para_local(local)

    #     if dados_tempo:
    #         st.subheader(f"Previsão do tempo para {local}:")
    #         st.write(f"Temperatura: {dados_tempo['main']['temp']} °C")
    #         st.write(f"Condição: {dados_tempo['weather'][0]['description'].capitalize()}")
    #         st.write(f"Umidade: {dados_tempo['main']['humidity']}%")
    #         st.write(f"Velocidade do Vento: {dados_tempo['wind']['speed']} m/s")
    #     else:
    #         st.error("Não foi possível obter os dados do tempo. Verifique o nome da cidade ou a chave da API.")
    
    if not local:
        st.stop()
    dados_tempo = {}
    # quero colocar um botão para atualizar os dados
    if st.button("Obter Previsão do Tempo"):    
        dados_tempo = pegar_tempo_para_local(local) 
        if dados_tempo:
            clima_atual = dados_tempo['weather'][0]['description'].capitalize()
            temperatura = dados_tempo['main']['temp']
            sensacao_termica = dados_tempo['main']['feels_like']
            umidade = dados_tempo['main']['humidity']
            cobertura_nuvens = dados_tempo['clouds']['all']
        else:
            st.warning(f'Localidade "{local}" não foi encontrada no banco de dados da OpenWeather!')
            st.stop()

    # if not dados_tempo:
    #     st.warning(f'Localidade "{local}" não foi encontrada no banco de dados da OpenWeather!')
    #     st.stop()

    clima_atual = dados_tempo['weather'][0]['description'].capitalize()
    temperatura = dados_tempo['main']['temp']
    sensacao_termica = dados_tempo['main']['feels_like']
    umidade = dados_tempo['main']['humidity']
    cobertura_nuvens = dados_tempo['clouds']['all']
    
    st.metric(label="Clima Atual", value=clima_atual)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Temperatura (°C)", value=f"{temperatura} °C")
        st.metric(label="Sensação Térmica (°C)", value=f"{sensacao_termica} °C")
    with col2:
        st.metric(label="Umidade (%)", value=f"{umidade} %")
        st.metric(label="Cobertura de Nuvens (%)", value=f"{cobertura_nuvens} %")

if __name__ == "__main__":
    main()