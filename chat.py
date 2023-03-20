import openai
import json
import requests

# Configuração da chave de acesso à API do GPT
openai.api_key = "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"

# Definindo os dados que serão inseridos na API
with open("artigos.json", "r") as f:
    dados = json.load(f)

# Divide os dados em 5 partes iguais
num_parts = 802
part_size = len(dados) // num_parts
partitions = [dados[i:i+part_size] for i in range(0, len(dados), part_size)]

# Envia uma consulta para a API para cada partição
respostas = []
for i in range(num_parts):
    resposta = openai.Completion.create(
        engine="davinci",
        prompt="Pergunta: Qual é o valor que mais se repete na coluna 'date' nos dados fornecidos?\nDados: " + str(partitions[i]),
        temperature=0.5,
        max_tokens=100,
        n=1,
        stop=None,
    )

# Exibe a resposta da API
print(resposta.choices[0].text)
""" 
# Faz uma solicitação para obter os dados da cidade do IBGE
url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios/2304400"
response = requests.get(url)
dados_cidade = response.json()

# Envia uma consulta para a API
resposta = openai.Completion.create(
    engine="davinci",
    prompt="Pergunta: Qual é a população da cidade de " + dados_cidade["nome"] + "?\nDados: " + str(dados_cidade),
    temperature=0.5,
    max_tokens=100,
    n=1,
    stop=None,
)

# Exibe a resposta da API
print(resposta.choices[0].text) """