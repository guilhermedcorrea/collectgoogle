from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, ForeignKey, join, select, insert, update
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

from config import get_engine


Base = declarative_base()
Session = sessionmaker(bind=get_engine())
session = Session()

class MonitoramentoPrecos(Base):
    __tablename__="MonitoramentoPrecos"
    __table_args__ = {"schema": "Produtos"}
    idpreco = Column(Integer, primary_key=True)
    idproduto = Column(Integer)
    urlgoogle = Column(String, unique=False, nullable=False)
    marcaproduto = Column(String, unique=False, nullable=False)
    paginaanuncio = Column(String, unique=False, nullable=False)
    concorrente = Column(String, unique=False, nullable=False)
    precoconcorrente = Column(Float)
    nomeproduto = Column(String, unique=False, nullable=False)
    ean = Column(String, unique=False, nullable=False)
    sku = Column(String, unique=False, nullable=False)
    precohausz = Column(Float)
    dataatualizado = Column(DateTime, unique=False, nullable=False)
    vendidoem = Column(String, unique=False, nullable=False)
    custo = Column(Float)
    diferenca = Column(Float)
    margem = Column(Float)
    statuspreco = Column(String, unique=False, nullable=False)
    urljet = Column(String, unique=False, nullable=False)
    categoriahausz = Column(String, unique=False, nullable=False)
    subcategoria = Column(String, unique=False, nullable=False)
    departamento = Column(String, unique=False, nullable=False)


class UrlsBase(Base):
    __tablename__ = "UrlsBase"
    __table_args__ = {"schema": "Produtos"}
    idurl = Column(Integer, primary_key=True)
    idproduto = Column(Integer)
    loja = Column(String, unique=False, nullable=False)
    urlanuncio = Column(String, unique=False, nullable=False)
    dataanuncio = Column(DateTime, unique=False, nullable=False)
    referencia = Column(String, unique=False, nullable=False)


