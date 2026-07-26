from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Pirometro(SQLModel, table=True):
    __tablename__ = "pirometro"

    id: str = Field(primary_key=True)
    nome: str
    setor: str
    material_alvo: str
    processo: str
    molde: str
    ativo: bool = Field(default=True)

    # Relacionamentos
    codigos: List["CodigoPirometro"] = Relationship(back_populates="pirometro")
    leituras: List["Leitura"] = Relationship(back_populates="pirometro")
    cadinhos: List["Cadinho"] = Relationship(back_populates="pirometro")


class CodigoPirometro(SQLModel, table=True):
    __tablename__ = "codigo_pirometro"

    id: Optional[int] = Field(default=None, primary_key=True)
    pirometro_id: str = Field(foreign_key="pirometro.id")
    codigo: int = Field(ge=0, le=99)
    etapa_nome: str
    descricao: Optional[str] = Field(default=None)
    temp_min_esperada: Optional[float] = Field(default=None)
    temp_max_esperada: Optional[float] = Field(default=None)
    ordem_no_processo: Optional[int] = Field(default=None)
    ativo: bool = Field(default=True)

    # Relacionamentos
    pirometro: Pirometro = Relationship(back_populates="codigos")
    leituras: List["Leitura"] = Relationship(back_populates="codigo_pirometro")


class Leitura(SQLModel, table=True):
    __tablename__ = "leitura"

    id: Optional[int] = Field(default=None, primary_key=True)
    pirometro_id: str = Field(foreign_key="pirometro.id")
    codigo_pirometro_id: int = Field(foreign_key="codigo_pirometro.id")
    temperatura_lida: float
    operador_id: Optional[str] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Rastreabilidade e melhorias solicitadas
    corrida_id: Optional[str] = Field(default=None)
    lote_id: Optional[str] = Field(default=None)
    panela_id: Optional[str] = Field(default=None)

    observacao: Optional[str] = Field(default=None)

    # Relacionamentos
    pirometro: Pirometro = Relationship(back_populates="leituras")
    codigo_pirometro: CodigoPirometro = Relationship(back_populates="leituras")


class Cadinho(SQLModel, table=True):
    __tablename__ = "cadinho"

    id: Optional[int] = Field(default=None, primary_key=True)
    pirometro_id: str = Field(foreign_key="pirometro.id")
    codigo_identificador: str
    espessura_inicial_mm: float
    espessura_atual_mm: float
    espessura_minima_seguranca_mm: float = Field(default=50.0)
    corridas_acumuladas: int = Field(default=0)
    max_corridas_esperadas: Optional[int] = Field(default=200)
    data_instalacao: datetime = Field(default_factory=datetime.utcnow)
    data_substituicao: Optional[datetime] = Field(default=None)
    status: str = Field(default="ATIVO")
    observacao: Optional[str] = Field(default=None)

    # Relacionamentos
    pirometro: Pirometro = Relationship(back_populates="cadinhos")
    registros_desgaste: List["RegistroDesgasteCadinho"] = Relationship(
        back_populates="cadinho"
    )


class RegistroDesgasteCadinho(SQLModel, table=True):
    __tablename__ = "registro_desgaste_cadinho"

    id: Optional[int] = Field(default=None, primary_key=True)
    cadinho_id: int = Field(foreign_key="cadinho.id")
    espessura_medida_mm: float
    corridas_no_momento: Optional[int] = Field(default=None)
    operador_id: Optional[str] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    observacao: Optional[str] = Field(default=None)

    # Relacionamentos
    cadinho: Cadinho = Relationship(back_populates="registros_desgaste")
