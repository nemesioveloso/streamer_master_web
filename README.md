# 🎬 Streamer Master

Projeto em **FastAPI** para scraping e listagem de filmes do [Public Domain Movie](https://publicdomainmovie.net).
Os filmes são salvos em um banco SQLite e podem ser consultados via API com paginação e busca por título.

---

## 📋 Pré-requisitos

* [Python 3.10+](https://www.python.org/downloads/) instalado
* [Git](https://git-scm.com/downloads) instalado

---

## 🚀 Como rodar o projeto

### 1. Clonar o repositório

```
git clone https://github.com/seu-usuario/streamer_master_web.git
cd streamer_master_web
```

### 2. Criar e ativar o ambiente virtual

Windows (PowerShell):

```
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```
pip install -r requirements.txt
```

### 4. Rodar a aplicação FastAPI com Uvicorn

```
uvicorn main:app
```

Por padrão a API sobe em:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📚 Endpoints principais

### 1. Scraper de filmes

Faz scraping de `/feature_movies` e `/cartoons`, salva no banco e retorna resumo:

```
GET /filmes
```

Exemplo de resposta:

```
{
  "status": "✅ Finalizado",
  "novos": 120,
  "total_no_banco": 1568
}
```

---

### 2. Listagem paginada

Consulta filmes já salvos no banco, com paginação e filtro opcional por título:

```
GET /filmesListar?page=1&size=10&titulo=night
```

Exemplo de resposta:

```
{
  "page": 1,
  "size": 10,
  "total": 1237,
  "results": [
    {
      "titulo": "Night of the Living Dead",
      "url": "https://publicdomainmovie.net/movie/night-of-the-living-dead-3",
      "tipo": "FILME",
      "imagem": "https://publicdomainmovie.net/image.php?id=NightLivingDead"
    }
  ]
}
```

---

### 3. Resetar banco

Apaga todos os registros da tabela de mídias:

```
DELETE /reset
```

---

## 🛠️ Estrutura de pastas

```
streamer-master/
│── database.py       # Configuração do banco (SQLite + SQLAlchemy)
│── main.py           # Entrypoint da aplicação FastAPI
│── models.py         # Schemas Pydantic
│── scraper.py        # Scraper para filmes e cartoons
│── streamer.db       # Banco SQLite
│── requirements.txt  # Dependências do projeto
│── .gitignore        # Arquivos/pastas ignorados pelo Git
└── venv/             # Ambiente virtual (ignorado pelo Git)
```
