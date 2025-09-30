from pydantic import BaseModel, ConfigDict
from typing import List


class MidiaBase(BaseModel):
    titulo: str
    url: str
    tipo: str = "FILME"
    imagem: str | None = None
    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel):
    page: int
    size: int
    total: int
    results: List[MidiaBase]


class ScraperSummary(BaseModel):
    status: str
    novos: int
    total_no_banco: int
