"""
Desafio usando pymongo, criando coleção bank usando
MongoDBAtlas 
"""
from pymongo import MongoClient
from decouple import config
from flask import Flask


# Carrega as variáveis de ambiente do arquivo .env
MONGO_URI = config("MONGO_URI")
client = MongoClient(MONGO_URI)

# Criando um banco de dados no MongoDB
db = client.bancoMongoDB

# Criando uma collection
collection = db.desafio_dio

# Consultando todos os dados dentro de coleções
for data in collection.find():
    print(
        f'\nId:             {data["_id"]}'
        f'\nNúmero:         {data["Number"]}'
        f'\nNome:           {data["Name"]}'
        f'\nIdade:          {data["Age"]}'
        f'\nCidade:         {data["City"]}'
        f'\nPaís:           {data["Country"]}'
    )

app = Flask(__name__)

@app.route('/')

def index():
    """
        Função criada para trazer retorno de dados á página inicial
        Index.html
    """

    # Consultando todos os dados dentro de coleções
    data_str = ""
    for data_collection in collection.find():
        data_str += (
            f'Id: {data_collection["_id"]}'
            f'<br>Número: {data_collection["Number"]}'
            f'<br>Nome: {data_collection["Name"]}'
            f'<br>Idade: {data_collection["Age"]}'
            f'<br>Cidade: {data_collection["City"]}'
            f'<br>País: {data_collection["Country"]}<br><br>'
        )

    # Criando a resposta HTML
    html_response = f"""
    <html>
        <head>
            <title>Desafio DIO</title>
            <style>
                .main {{
                    width: 100%;
                    text-align: center;
                }}
                .centered {{
                    text-align: left;
                    display: inline-block;
                }}
                h1 {{
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <h1>Dados da Coleção desafio_dio:</h1>
            <div class="main">
                <div class="centered">
                    {data_str}
                </div>
            </div>
        </body>
    </html>
    """
    return html_response


app.run()
