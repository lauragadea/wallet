from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('mysql://root:root@localhost:3306/walletdb', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
class Persona(Base):
    __tablename__ = 'persona'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id_persona = Column(Integer, primary_key=True)
    dni = Column(Integer)
    usuario = Column(String(45))
    contrasenia = Column(String(45))
    nombre = Column(String(45))
    apellido = Column(String(45))
    domicilio = Column(String(45))

	def __init__(self, dni, usuario, contrasenia, nombre, apellido, domicilio):
			self.dni = dni
			self.usuario = usuario
			self.contrasenia = contrasenia
			self.nombre = nombre
			self.apellido = apellido
			self.domicilio = domicilio
Ñ[]
	def __repr__(self):
			return "<Persona(%d, %s, %s, %s, %s, %s)>" % (self.name, self.value)

