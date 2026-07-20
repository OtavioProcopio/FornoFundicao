from datetime import datetime

from core.domain.models import CodigoPirometro, Leitura, Pirometro


def test_pirometro_model():
    pirometro = Pirometro(
        id="PIR-01",
        nome="Centrífuga 1",
        setor="Aço",
        material_alvo="SAE 1045",
        processo="Centrifugação",
        molde="Coquilha",
        ativo=True,
    )
    assert pirometro.id == "PIR-01"
    assert pirometro.nome == "Centrífuga 1"
    assert pirometro.ativo is True


def test_codigo_pirometro_model():
    codigo = CodigoPirometro(
        pirometro_id="PIR-01",
        codigo=5,
        etapa_nome="Vazamento",
        descricao="Início de vazamento",
        temp_min_esperada=1500.0,
        temp_max_esperada=1600.0,
        ordem_no_processo=1,
        ativo=True,
    )
    assert codigo.codigo == 5
    assert codigo.etapa_nome == "Vazamento"
    assert codigo.temp_min_esperada == 1500.0


def test_leitura_model():
    leitura = Leitura(
        pirometro_id="PIR-01",
        codigo_pirometro_id=1,
        temperatura_lida=1550.0,
        operador_id="OP01",
        corrida_id="C01",
        lote_id="L01",
        panela_id="P01",
        observacao="Leitura regular",
    )
    assert leitura.pirometro_id == "PIR-01"
    assert leitura.temperatura_lida == 1550.0
    assert isinstance(leitura.timestamp, datetime)
