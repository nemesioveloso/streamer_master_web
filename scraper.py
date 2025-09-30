import requests
import logging
from bs4 import BeautifulSoup
from models import MidiaBase
from urllib.parse import urljoin

BASE_URL = "https://publicdomainmovie.net"

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def scrape_section(path: str):
    url = urljoin(BASE_URL, f"/{path}")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    filmes = []
    pagina = 1
    visitadas = set()

    while url and url not in visitadas:
        visitadas.add(url)
        logger.info(f"🔎 Acessando {url}")
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            logger.error(f"❌ Erro ao acessar {url}: {resp.status_code}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        # Cada “bloco” de filme fica dentro de .views-field-nothing-1
        elementos = soup.select(".views-field-nothing-1")
        logger.info(f"📄 Página {pagina} → {len(elementos)} filmes encontrados")

        for bloco in elementos:
            link = bloco.select_one(".details h1 a")
            if not link:
                continue

            titulo = link.get_text(strip=True)
            href = urljoin(BASE_URL, link.get("href", ""))

            img_tag = bloco.select_one("img")
            imagem = (
                urljoin(BASE_URL, img_tag["src"])
                if img_tag and img_tag.get("src")
                else None
            )

            if not titulo:
                logger.warning(f"⚠️ Link sem título ignorado: {href}")
                continue

            filmes.append(
                MidiaBase(titulo=titulo, url=href, tipo="FILME", imagem=imagem)
            )
            logger.info(f"🎬 Extraído: {titulo} ({imagem}) -> {href}")

        # Próxima página (“next ›”)
        next_el = soup.select_one("li.pager-next a")
        if next_el and next_el.get("href"):
            url = urljoin(BASE_URL, next_el["href"])
            pagina += 1
        else:
            url = None  # acabou a paginação

    logger.info(f"✅ Total extraído na seção /{path}: {len(filmes)}")
    return filmes


def scrape_publicdomainmovies():
    """
    Faz scraping de múltiplas seções e retorna tudo como FILME.
    """
    filmes = scrape_section("feature_movies")
    cartoons = scrape_section("cartoons")

    total = len(filmes) + len(cartoons)
    logger.info(f"🎉 Total geral extraído: {total} filmes")
    return filmes + cartoons
