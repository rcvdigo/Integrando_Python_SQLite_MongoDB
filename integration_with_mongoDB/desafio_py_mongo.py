"""
Desafio usando pymongo, criando coleção bank usando
MongoDBAtlas 
"""
from pymongo import MongoClient
from decouple import config


# Carrega as variáveis de ambiente do arquivo .env
MONGO_URI = config("MONGO_URI")
client = MongoClient(MONGO_URI)

# Criando um banco de dados no MongoDB
db = client.bancoMongoDB

# Criando uma collection
bank = db.bank

# Definição de informações para compor o DOC no MONGODBATLAS
data = [
    {
        "nome": "Rodrigo",
        "cpf": "49987677789",
        "endereco": "Cabreúva, 665",
        "contas": [
            {
                "tipo": "Cc",
                "agencia": "0001",
                "num": 36455,
                "saldo": 10.00
            }
        ]
    },
    {
        "nome": "Pamêla",
        "cpf": "03399733476",
        "endereco": "Carpina, 10",
        "contas": [
            {
                "tipo": "Cp",
                "agencia": "0001",
                "num": 56878,
                "saldo": 100.00
            }
        ]
    }
]

print(db.list_collection_names(), end="\n")

# Preparando para submeter as informações:
# Inserindo dados na collection
inserir_dados_MongoDB = bank.insert_many(data).inserted_ids

# Consultando todos os dados dentro de coleções
for data in bank.find():
    print(
        f'\nNome:           {data["nome"]}'
        f'\nCPF:            {data["cpf"][:3]}.'
        f'{data["cpf"][3:6]}.{data["cpf"][6:9]}-{data["cpf"][9:11]}'
        f'\nEndereço:       {data["endereco"]}'
        f'\nTipo de conta:  {data["contas"][0]["tipo"]}'
        f'\nAgência:        {data["contas"][0]["agencia"]}'
        f'\nConta:          {data["contas"][0]["num"]}'
        f'\nSaldo:          {data["contas"][0]["saldo"]:.2f}\n'
    )
