"""
    Primeiro programa de integração com banco de dados
    utilizando SQLAlchemy e modelo ORM

"""
import sqlalchemy


from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import select
from sqlalchemy import Integer
from sqlalchemy import DECIMAL
from sqlalchemy import String
from sqlalchemy import BINARY
from sqlalchemy import ForeignKey


Base = declarative_base()


class Cliente(Base):
    """
        Esta classe representa a tabela Cliente dentro
        do SQlite.
    """
    # Nome da tabela
    __tablename__ = "Cliente"
    # Atributos
    idCliente = Column(Integer, primary_key=True, autoincrement="auto")
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String(9))

    # Criando o relacionamento
    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"idCliente={self.idCliente}, "
            f"nome={self.nome}, "
            f"cpf={self.cpf}, "
            f"endereco={self.endereco})"
        )


class Conta(Base):
    """
        Esta classe representa a tabela Conta dentro
        do SQlite.
    """
    # Nome da tabela
    __tablename__ = "Conta"
    # Atributos
    idConta = Column(BINARY, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey(
        "Cliente.idCliente"), nullable=False)
    saldo = Column(DECIMAL)

    cliente = relationship(
        "Cliente", back_populates="conta"
    )

    def __repr__(self):
        return (
            f"idConta={self.idConta}, "
            f"tipo={self.tipo}, "
            f"agencia={self.agencia}, "
            f"num={self.num}, "
            f"id_cliente={self.id_cliente}, "
            f"saldo={self.saldo} "
        )


# Conexão com o banco de dados
engine = sqlalchemy.create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Definindo um Inspect (Que serve para investigar o seu schema do banco de dados POO)
inspetor_engine = sqlalchemy.inspect(engine)

# Criando uma conexão
conector = engine.connect()

# Mostra os nomes das tabelas
print(inspetor_engine.get_table_names(), end="\n\n")

# Estabelecendo uma seção
with Session(engine) as session:
    # Adicionando dados as tabelas
    rodrigo = Cliente(
        nome='Rodrigo',
        cpf='49987677789',
        endereco='Cabreúva, 665',
        conta=[Conta(idConta=b'\x00', tipo='Cc',
                     agencia='0001', num=36455, saldo=10.00)]
    )

    # Adicionando dados as tabelas
    pamela = Cliente(
        nome='Pamela',
        cpf='03399733476',
        endereco='Carpina, 10',
        conta=[Conta(idConta=b'\x01', tipo='Cp',
                     agencia='0001', num=56878, saldo=100.00)]
    )

    # Enviando para o BANCO DE DADOS (Persistência De Dados)
    session.add_all([rodrigo, pamela])
    session.commit()


# Criando um Statments

# Tabela Cliente
stmt = select(Cliente).where(Cliente.nome.in_(['Rodrigo', 'Pamela']))

# Tabela Conta
stmt_conta = select(Conta)

# Join Cliente e Conta
stmt_join = select(Cliente.nome, Cliente.cpf, Cliente.endereco,
                   Conta.tipo, Conta.agencia, Conta.num, Conta.saldo).join(
                       target=Conta,
                       onclause=Cliente.idCliente == Conta.id_cliente)

# imprimindo a consulta sobre toda a tabela Cliente
print("--------------CONSULTA TABELA CLIENTE USANDO O MÉTODO SCALARS----------------------------")
for data in session.scalars(stmt):
    print(data)
print("-----------------------------------------------------------------------------------------")

print()

# imprimindo a consulta sobre toda a tabela Cliente
consultas = conector.execute(stmt).fetchall()
print("--------------CONSULTA TABELA CLIENTE USANDO À PARTIR DO CONECTOR------------------------")
for data in consultas:
    print(data)
print("-----------------------------------------------------------------------------------------")


# imprimindo a consulta sobre toda a tabela Conta
print("--------------CONSULTA TABELA CONTA USANDO O MÉTODO SCALARS------------------------------")
for data in session.scalars(stmt_conta):
    print(data)
print("-----------------------------------------------------------------------------------------")

print()

# imprimindo a consulta sobre toda a tabela Conta
consultas = conector.execute(stmt_conta).fetchall()
print("--------------CONSULTA TABELA CONTA USANDO À PARTIR DO CONECTOR--------------------------")
for data in consultas:
    print(data)
print("-----------------------------------------------------------------------------------------")

print()

# imprimindo a consulta sobre toda a tabela Cliente e Conta
consultas = conector.execute(stmt_join).fetchall()
print("-----------CONSULTA TABELA CLIENTE E CONTA USANDO À PARTIR DO CONECTOR----------------")
for data in consultas:
    print(
        f"Nome:            {data[0]}\n"
        f"CPF:             {data[1][:3]}.{data[1][3:6]}.{data[1][6:9]}-{data[1][9:]}\n"
        f"Endereço:        {data[2]}\n"
        f"Tipo de conta:   {data[3][:1]}/{data[3][1:2]}\n"
        f"Agência:         {data[4]}\n"
        f"Conta:           {data[5]}\n"
        f"Saldo:           {data[6]:.2f}\n"
        )
print("--------------------------------------------------------------------------------------")
