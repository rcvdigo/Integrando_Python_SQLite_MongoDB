"""
    Primeiro programa de integração com banco de dados
    utilizando SQLAlchemy e modelo ORM

"""
import sqlalchemy as sqlA
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import text

Base = declarative_base()


class User(Base):
    """
        Esta classe representa a tabela user_account dentro
        do SQlite.
    """
    # Nome da tabela
    __tablename__ = "User"
    # Atributos
    idUser = Column(Integer, primary_key=True, autoincrement="auto")
    nome = Column(String(20))
    sobre_nome = Column(String(30))

    # Criando o relacionamento
    endereco = relationship(
        "Endereco", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.idUser}, nome={self.nome}, sobre_nome={self.sobre_nome})"


class Endereco(Base):
    """
        Esta classe representa a tabela user_endereço dentro
        do SQlite.
    """
    # Nome da tabela
    __tablename__ = "Endereco"
    # Atributos
    idEndereco = Column(Integer, primary_key=True, autoincrement="auto")
    endereco_de_email = Column(String(50), nullable=False, unique=True)
    user_idUser = Column(Integer, ForeignKey("User.idUser"), nullable=False)

    user = relationship(
        "User", back_populates="endereco"
    )

    def __repr__(self):
        return f"""Endereco(idEndereco={self.idEndereco},
endereco_de_email={self.endereco_de_email}, 
user_idUser={self.user_idUser})"""


print(User.__tablename__, User.__table__, sep="*", end=" ")
print(User.__table__, end="\n\n")
print(Endereco.__table__)
print(Endereco.__tablename__, end="\n\n")

# Conexão com o banco de dados
engine = sqlA.create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Definindo um Inspect (Que serve para investigar o seu schema do banco de dados POO)
inspetor_engine = sqlA.inspect(engine)

# Mostra os nomes das tabelas
print(inspetor_engine.get_table_names(), end="\n\n")

# Mostra o nome do banco de dados (Por Default = main)
print(inspetor_engine.default_schema_name, end="\n\n")

# Estabelecendo uma seção
with Session(engine) as session:
    # Adicionando dados as tabelas
    rodrigo = User(
        nome='rodrigo',
        sobre_nome='Camurça Vera',
        endereco=[Endereco(endereco_de_email='rcvdigo@gmail.com')]
    )

    # Adicionando dados as tabelas
    juliana = User(
        nome='juliana',
        sobre_nome='Mascarenhas',
        endereco=[Endereco(endereco_de_email='julianam@email.com')]
    )

    # Adicionando dados as tabelas
    sandy = User(
        nome='sandy',
        sobre_nome='Junior',
        endereco=[Endereco(endereco_de_email='sandy@email.com'),
                   Endereco(endereco_de_email='junior@email.com')]
    )

    # Adicionando dados as tabelas
    patrick = User(
        nome='patrick',
        sobre_nome='Cardoso'
    )

    # Enviando para o BANCO DE DADOS (Persistência De Dados)
    session.add_all([rodrigo, juliana, sandy, patrick])

    session.commit()

# Criando um Statment SELECT

# Tabela User
stmt = select(User).where(User.nome.in_(['rodrigo', 'juliana', 'sandy']))
print(stmt, end="\n\n")

# Tabela Endereco
stmt_endereco = select(Endereco).where(Endereco.user_idUser.in_([1, 2, 3]))
print(stmt_endereco, end="\n\n")

# Usando Order By
stmt_order_by = select(User).order_by(User.sobre_nome.asc())
print(stmt_order_by, end="\n\n")

# Usando o Join
stmt_join = select(User, Endereco).join_from(Endereco, User)

# Usando o Join
stmt_count = select(func.count('*')).select_from(User)

print("@"*50)
print(stmt_join)
print("@"*50)

# Final de criação de Statment SELECT

print("------CONSULTA TABELA USUARIOS COM ORDER BY--------")
# imprimindo a consulta sobre toda a tabela User com OrderBy
for user in session.scalars(stmt_order_by):
    print(user, end="------CONSULTA TABELA USUARIOS COM ORDER BY--------\n\n")
print("---------------------------------------------------")

print("------CONSULTA TABELA USUARIOS--------")
# imprimindo a consulta sobre toda a tabela User
for user in session.scalars(stmt):
    print(user, end="------CONSULTA TABELA USUARIOS--------\n\n")
print("--------------------------------------")

print("------CONSULTA TABELA ENDERECO--------")
# imprimindo a consulta sobre toda a tabela Endereço
for address in session.scalars(stmt_endereco):
    print(address, end="------CONSULTA TABELA ENDERECO--------\n\n")
print("--------------------------------------")

print("------CONSULTA TABELA ENDERECO E USUARIOS--------")
# imprimindo a consulta sobre toda a tabela ENDERECO E USUARIOS
for data in session.scalars(stmt_join):
    print(data, end="\n\n")
print("--------------------------------------")

print("------CONSULTA TABELA USUARIOS--------")
# imprimindo a consulta sobre toda a tabela USUARIOS
for data in session.scalars(stmt_count):
    print(data, end="\n\n")
print("--------------------------------------")

# Criando uma conexão
conector = engine.connect()

consultas = conector.execute(stmt_join).fetchall()
print("\nExecutando Statment a partir da connection")
for data in consultas:
    print(data)

# COUNT COM CONECTOR
consultas = conector.execute(stmt_count).fetchall()
print("\nExecutando Statment a partir da connection")
for data in consultas:
    print(data)

# COUNT COM SCALARS
print("------CONSULTA TABELA USUER COM COUNT SCALARS--------")
# imprimindo a consulta sobre toda a tabela Endereço
for data in session.scalars(stmt_count):
    print(data, end="\n\n")
print("--------------------------------------")


stmt_TXT = text(
    """SELECT u.nome, e.endereco_de_email
               FROM User AS u 
               INNER JOIN Endereco AS e 
               ON u.idUser = e.user_idUser
            """)


consultas = conector.execute(stmt_TXT).fetchall()


# USANDO O OBJETO TEXT
print("------CONSULTA TABELA USER USANDO O OBJETO TEXT--------")
# imprimindo a consulta sobre toda a tabela USANDO O OBJETO TEXT
for data in consultas:
    print(data)
print("--------------------------------------")
