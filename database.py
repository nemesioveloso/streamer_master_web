from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Banco em memória (troque para "sqlite:///meubanco.db" ou MySQL depois)
DATABASE_URL = "sqlite:///./streamer.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Midia(Base):
    __tablename__ = "midia"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    tipo = Column(String, default="FILME")
    imagem = Column(String, nullable=True)


# Cria as tabelas no banco em memória
Base.metadata.create_all(bind=engine)
