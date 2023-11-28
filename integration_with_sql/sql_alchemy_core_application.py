from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import text

engine = create_engine('sqlite:///:memory:')
metadata_obj = MetaData()

user = Table(
    'user',
    metadata_obj,
    Column('user_id', Integer, primary_key=True, autoincrement="auto"),
    Column('endereco_email', String(60), unique=True),
    Column('user_name', String(60), unique=True, nullable=False),
    Column('nickname', String(60), unique=True, nullable=False)
)

user_prefs = Table(
    'user_prefs',
    metadata_obj,
    Column('pref_id', Integer, primary_key=True, autoincrement="auto"),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(40), nullable=False),
    Column('pref_value', String(100))
)

for table in metadata_obj.sorted_tables:
    print(f"\n{table}", end="\n\n")

metadata_db_obj = MetaData()

financial_info = Table(
    'financial_info',
    metadata_db_obj,
    Column('id', Integer, primary_key=True),
    Column('value', String(100), nullable=False)
)

print("Info da tabela financial_info")
print(financial_info.primary_key)
print(financial_info.constraints, end="\n\n\n")

# Criando as tabelas em um engine
metadata_obj.create_all(engine)

# Criando uma conexão
conn = engine.connect()

# INSERINDO OS DADOS NAS TABELAS
sql_insert_into_user = text('insert into user values(1,"Rodrigo","rcvdigo@gmail.com","rcv"), (2,"Pamela","pamelatalita@gmail.com","prt")')
consulta = conn.execute(sql_insert_into_user)

# Executando a consulta SQL
sql = text('SELECT * FROM user')
consulta = conn.execute(sql)

# Iterando pelos resultados
for row in consulta:
    print(row)

# Fechando a conexão
conn.close()
