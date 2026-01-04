import os
import requests
from pprint import pprint

# Tente importar o dotenv. Se der erro, avisa que precisa instalar.
try:
    import dotenv
except ImportError:
    print("ERRO: A biblioteca 'python-dotenv' não está instalada.")
    print("Instale rodando: pip install python-dotenv")
    exit()

# ==============================================================================
# PARTE 1: O Jeito "Perigoso" (Hardcoded)
# Funciona, mas se você subir isso para o GitHub, hackers podem roubar sua chave.
# ==============================================================================
print("\n--- Parte 1: Chave Exposta no Código (Não recomendado) ---")

url = "http://api.openweathermap.org/data/2.5/weather"

# A chave aqui está "hardcoded" (escrita diretamente no código).
# Em projetos reais, EVITE fazer isso.
params_inseguros = {
    'q': 'Porto Alegre',
    'units': 'metric', # Adicionei para vir em Celsius
    'appid': '09afb38ed59655301914f34dc9a1cd60', # <--- O perigo mora aqui
}

# requests.get com 'params': A biblioteca monta a URL automaticamente.
# A URL final fica: .../weather?q=Porto Alegre&units=metric&appid=...
resposta = requests.get(url, params=params_inseguros)

if resposta.status_code == 401:
    print("Erro 401: Provavelmente a chave 'hardcoded' é inválida (o que é esperado neste exemplo).")
elif resposta.status_code == 200:
    print("Sucesso (Hardcoded)!")
    pprint(resposta.json())

# ==============================================================================
# PARTE 2: O Jeito "Profissional" (Usando variáveis de ambiente)
# A chave fica em um arquivo .env que NÃO é compartilhado/versionado.
# ==============================================================================
print("\n--- Parte 2: Usando python-dotenv (Recomendado) ---")

# 1. find_dotenv(): Procura um arquivo chamado ".env" na pasta do projeto
# 2. load_dotenv(): Lê esse arquivo e carrega as variáveis para a memória do sistema
dotenv.load_dotenv(dotenv.find_dotenv())

# os.environ.get(): Pega o valor da variável carregada na memória.
# Se a variável não existir, retorna None (evitando erro crasso).
app_id_secreto = os.environ.get('CHAVE_API_WEATHER')

# Verificação de segurança antes de tentar a conexão
if not app_id_secreto:
    print("AVISO: Variável 'CHAVE_API_WEATHER' não encontrada no arquivo .env")
    print("Crie um arquivo chamado .env na mesma pasta com o conteúdo:")
    print("CHAVE_API_WEATHER=sua_chave_real_aqui")
else:
    print(f"Chave carregada com sucesso: {app_id_secreto[:4]}... (ocultada)")

    params_seguros = {
        'q': 'Porto Alegre',
        'units': 'metric',
        'appid': app_id_secreto # Usamos a variável, não a string direta
    }

    resposta = requests.get(url, params=params_seguros)

    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f"Erro no request: {e}")
        # É útil imprimir o JSON de erro da API para saber o motivo (ex: chave bloqueada, cidade não existe)
        try:
            print("Detalhe do erro:", resposta.json())
        except:
            pass
        resultado = None
    else:
        resultado = resposta.json()
        print("\nDados do Clima Recebidos:")
    pprint(resultado)