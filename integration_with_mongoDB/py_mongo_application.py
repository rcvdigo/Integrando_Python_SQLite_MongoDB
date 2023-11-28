"""
Primeira aplicação com integração ao banco de dados
MongoDBAtlas
"""
import datetime
import pprint
import pymongo

from decouple import config


# Carrega as variáveis de ambiente do arquivo .env
MONGO_URI = config("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)

db = client.bancoMongoDB
collection = db.test_collection
print("\n\n", collection, end="\n\n")

# Definição de informações para compor o DOC no MONGODBATLAS
data = {
    "author": "Mike",
    "text": "minha primeira aplicação com mongoDB com python!!!",
    "tags": ["Mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()
}

# bulk inserts
new_posts = [
    {
        "author": "Rodrigo",
        "text": "Novos dados!!!",
        "tags": ["Mongodb", "python7", "pymongo"],
        "date": datetime.datetime.utcnow()
    },
    {
        "author": "Pamela",
        "text": "Novos dados!!!",
        "title": "Mostrando a flexibilidade de um banco de dados não relacional",
        "date": datetime.datetime(2009, 11, 10, 10, 45)
    }
]

calendario = {
    "1": "Janeiro",
    "2": "Fevereiro",
    "3": "Março",
    "4": "Abril",
    "5": "Maio",
    "6": "Junho",
    "7": "Julho",
    "8": "Agosto",
    "9": "Setembro",
    "10": "Outubro",
    "11": "Novembro",
    "12": "Dezembro"
}

colecoes = db.colecoes  # Criando uma collection

# Preparando para submeter as informações:
# inserir_dados_MongoDB = colecoes.insert_many(new_posts).inserted_ids
# Inserindo dados na collection
# post_id = colecoes.insert_one(calendario).inserted_id # Inserindo dados na collection


# posts = db.posts # Definindo um post que será executado
# post_id = posts.insert_one(data).inserted_id # Inserindo os dados com um ID
# print(post_id, end="\n\n")

print(db.list_collection_names(), end="\n\n")

print(db.colecoes.find_one(), end="\n\n")

pprint.pprint(db.colecoes.find_one())

print("\n\n\n\n")
pprint.pprint(db.colecoes.find_one({"author": "Rodrigo"}))

print("\n\n\n", colecoes.find(), end="\n\n")


# Consultando todos os dados dentro de coleções
for data in colecoes.find():
    print("\n\n")
    pprint.pprint(data, sort_dicts=False)

print(
    f"\n\nTotal de documentos encontrados --> {colecoes.count_documents({})}")
print(
    "\n\nTotal de documentos encontrados com o nome do author = Mike -->"
    f"{colecoes.count_documents({'author':'Mike'})}")
print(
    f"\n\nTotal de documentos encontrados com o nome de tags = Mongodb -->"
    f"{colecoes.count_documents({'tags':'Mongodb'})}\n\n\n")

# buscando apenas o primeiro documento que encontrar com essas caracteristicas
print("buscando apenas o primeiro documento que encontrar com essas caracteristicas:"
      "'tags': 'Mongodb'\n".title())
pprint.pprint(colecoes.find_one({'tags': 'Mongodb'}))

print("\n\nRecuperando info da coleção coleções de maneira ordenada: \n\n".title())
for dados in colecoes.find({}).sort("date"):
    pprint.pprint(dados)
    print("\n")

# Definindo um Index no MongoDB
result = db.profiles.create_index([('author', pymongo.ASCENDING)], unique=True)
print("\n\nDefinindo um Index no MongoDB\n".title())
print(sorted(list(db.profiles.index_information())))

# Criando profiles users de usuarios

user_profile_user = [
    {'user_id': 211, 'name': 'rcvdigo'},
    {'user_id': 212, 'name': 'theo'}
]

# valores = db.profiles_user.insert_many(user_profile_user)
print("\n\nColeções armazenadas no mongoDB\n".title())
print(db.list_collection_names(), "\n\n")

collections = db.list_collection_names()

# # Definindo o filtro para encontrar o documento que você deseja atualizar
# filtro_atualizacao = {'author': 'Rodrigo'}

# # Definindo as atualizações que você deseja aplicar
# atualizacao_dados = {
#     '$set': {
#         'text': 'Dados atualizados!',
#         'tags': ['ATUALIZANDO', 'UM', 'DOCUMENTO'],
#         'date': datetime.datetime.utcnow()
#     }
# }

# # Atualizando um único documento que atende ao filtro
# colecoes.update_one(filtro_atualizacao, atualizacao_dados)

# Está instrução irá excluir a coleção inteira!!! CUIDADO
# db['colecoes'].drop()

# Está instrução irá excluir Todas as coleções existententes em seu servidor mongoDB!!! CUIDADO
# for dados in collections:
#     db[dados].drop()
# print("Todas as coleções foram deletadas.")

# print("\n\nDELETANDO O DOCUMENTO AUTHOR IGUAL A MIKE NA COLEÇÃO: COLEÇÕES\n")
# colecoes.delete_one({'author':'Mike'})
# pprint.pprint(colecoes.find_one({'author':'Mike'}))

# Este comando irá remover o banco de DADOS completo no servidor do MongoDB
# client.drop_database('bancoMongoDB')
