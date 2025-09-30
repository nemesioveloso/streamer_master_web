from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine, Midia as MidiaDB
from scraper import scrape_publicdomainmovies
import logging
from sqlalchemy import func
from typing import List, Optional
from models import MidiaBase, PaginatedResponse, ScraperSummary

# Configuração do log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/filmes", response_model=ScraperSummary)
def listar_filmes(db: Session = Depends(get_db)):
    filmes = scrape_publicdomainmovies()
    logger.info(f"🔎 Scraper retornou {len(filmes)} filmes")

    novos = 0
    for f in filmes:
        existe = db.query(MidiaDB).filter(MidiaDB.url == f.url).first()
        if not existe:
            midia_db = MidiaDB(
                titulo=f.titulo,
                url=f.url,
                tipo=f.tipo,
                imagem=f.imagem,  # 🔥 adiciona a imagem
            )
            db.add(midia_db)
            novos += 1

    db.commit()
    total = db.query(MidiaDB).count()

    logger.info(f"💾 {novos} novos registros inseridos no banco")
    logger.info(f"📦 Banco contém {total} registros no total")

    return ScraperSummary(status="✅ Finalizado", novos=novos, total_no_banco=total)


@app.get("/filmesListar", response_model=PaginatedResponse)
def listar_filmes_db(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Quantidade por página"),
    titulo: Optional[str] = Query(None, description="Filtrar por título"),
):
    query = db.query(MidiaDB)

    # aplica filtro se parametro for passado
    if titulo:
        query = query.filter(func.lower(MidiaDB.titulo).like(f"%{titulo.lower()}%"))

    total = query.count()
    offset = (page - 1) * size
    filmes = query.offset(offset).limit(size).all()

    filmes_convertidos = [MidiaBase.model_validate(f) for f in filmes]

    return PaginatedResponse(
        page=page,
        size=size,
        total=total,
        results=filmes_convertidos,
    )


@app.delete("/reset")
def resetar_banco(db: Session = Depends(get_db)):
    """
    Remove todos os registros da tabela de mídias.
    Útil para testes quando raspagem salva títulos vazios.
    """
    count = db.query(MidiaDB).delete()
    db.commit()
    logger.warning(f"⚠️ Banco resetado. {count} registros apagados.")
    return {"message": f"{count} registros apagados."}
