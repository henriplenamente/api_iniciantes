import base64
import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

# Configurações iniciais (simulando uma API que exige senha)
url = "https://httpbin.org/basic-auth/meu-usuario/senha-secreta"
usuario = "meu-usuario"
senha = "senha-secreta"

# ==============================================================================
# MÉTODO 1: Autenticação "Manual" (Hard Mode)
# Útil para entender como o cabeçalho HTTP é construído internamente.
# ==============================================================================

print("\n--- Método 1: Construindo o Header Manualmente ---")

# PASSO 1: Criar a string no formato padrão "usuario:senha"
credenciais = f'{usuario}:{senha}' 

# PASSO 2: Transformar texto em bytes (ASCII/UTF-8)
# O computador e o Base64 trabalham com bytes, não com strings de texto direto.
auth_bytes = credenciais.encode() 

# PASSO 3: Codificar em Base64
# A autenticação básica exige que a string seja convertida para Base64.
# Isso NÃO é criptografia (é fácil reverter), é apenas uma codificação para transporte seguro via HTTP.
auth_base64_bytes = base64.b64encode(auth_bytes)

# PASSO 4: Decodificar de volta para String para usar no Header
# Precisamos transformar os bytes de volta em texto para colocar no dicionário do Python.
auth_string = auth_base64_bytes.decode()

print(f'String gerada: {auth_string}')

# PASSO 5: Montar o Cabeçalho (Header)
# O padrão HTTP exige a palavra chave 'Basic' seguida de espaço e a string gerada.
headers = {
    'Authorization': f'Basic {auth_string}'
}

# Enviamos o request passando manualmente o header 'Authorization'
resposta_manual = requests.get(url, headers=headers)
print(f'Status Code Manual: {resposta_manual.status_code}\n {resposta_manual.json()}')


# ==============================================================================
# MÉTODO 2: Autenticação com HTTPBasicAuth (Easy Mode)
# É assim que fazemos no dia a dia. O requests faz tudo acima automaticamente.
# ==============================================================================

print("\n--- Método 2: Utilizando HTTPBasicAuth ---")

# PASSO ÚNICO: Criar o objeto de autenticação
# O HTTPBasicAuth faz todo o trabalho sujo:
# 1. Junta usuario:senha
# 2. Converte para Base64
# 3. Cria o header 'Authorization' e anexa ao request
auth_helper = HTTPBasicAuth(username=usuario, password=senha)

# Passamos o objeto no parâmetro 'auth' (não precisamos tocar nos headers)
resposta_auto = requests.get(url, auth=auth_helper)
print(f'Status Code Automático: {resposta_auto.status_code}')

# Apenas para conferir se deu certo (200 = OK)
if resposta_auto.status_code == 200:
    print("\nSucesso! A API reconheceu o usuário.")
    pprint(resposta_auto.json())