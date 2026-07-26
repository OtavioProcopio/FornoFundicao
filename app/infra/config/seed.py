from sqlmodel import Session, select

from core.domain.models import CodigoPirometro, Pirometro


def seed_data(session: Session):
    # Verificar se já existem pirômetros
    existing = session.exec(select(Pirometro)).first()
    if existing:
        return

    # PIR-01 (Centrífuga de Aço 1045)
    p1 = Pirometro(
        id="PIR-01",
        nome="PIR-01 - Centrífuga de Aço",
        setor="Aço",
        material_alvo="SAE 1045",
        processo="Centrifugação",
        molde="Coquilha",
        ativo=True,
    )
    session.add(p1)

    c1_0 = CodigoPirometro(
        pirometro_id="PIR-01",
        codigo=0,
        etapa_nome="Liberação de Forno",
        descricao="Temperatura ideal para liberar o forno de centrifugação de aço",
        temp_min_esperada=1520.0,
        temp_max_esperada=1560.0,
        ordem_no_processo=1,
        ativo=True,
    )
    c1_1 = CodigoPirometro(
        pirometro_id="PIR-01",
        codigo=1,
        etapa_nome="Vazamento",
        descricao="Temperatura ideal de vazamento na coquilha",
        temp_min_esperada=1500.0,
        temp_max_esperada=1540.0,
        ordem_no_processo=2,
        ativo=True,
    )
    session.add(c1_0)
    session.add(c1_1)

    # PIR-02 (Fundição de Aço Ligas)
    p2 = Pirometro(
        id="PIR-02",
        nome="PIR-02 - Fundição de Aço Ligas",
        setor="Aço Ligas",
        material_alvo="SAE 8640",
        processo="Fundição em molde",
        molde="Areia",
        ativo=True,
    )
    session.add(p2)

    c2_0 = CodigoPirometro(
        pirometro_id="PIR-02",
        codigo=0,
        etapa_nome="Liberação de Forno",
        descricao="Temperatura ideal para liberar o forno de aço ligas",
        temp_min_esperada=1540.0,
        temp_max_esperada=1580.0,
        ordem_no_processo=1,
        ativo=True,
    )
    session.add(c2_0)

    # PIR-03 (Fundição de Ferro Cinzento)
    p3 = Pirometro(
        id="PIR-03",
        nome="PIR-03 - Fundição de Ferro Cinzento",
        setor="Ferro",
        material_alvo="Ferro Cinzento",
        processo="Fundição em molde",
        molde="Areia",
        ativo=True,
    )
    session.add(p3)

    c3_0 = CodigoPirometro(
        pirometro_id="PIR-03",
        codigo=0,
        etapa_nome="Vazamento",
        descricao="Temperatura ideal de vazamento de ferro cinzento",
        temp_min_esperada=1380.0,
        temp_max_esperada=1420.0,
        ordem_no_processo=1,
        ativo=True,
    )
    session.add(c3_0)

    # PIR-04 (Fundição de Ferro Nodular)
    p4 = Pirometro(
        id="PIR-04",
        nome="PIR-04 - Fundição de Ferro Nodular",
        setor="Ferro",
        material_alvo="Ferro Nodular",
        processo="Fundição em molde",
        molde="Areia",
        ativo=True,
    )
    session.add(p4)

    c4_0 = CodigoPirometro(
        pirometro_id="PIR-04",
        codigo=0,
        etapa_nome="Vazamento",
        descricao="Temperatura ideal de vazamento de ferro nodular",
        temp_min_esperada=1400.0,
        temp_max_esperada=1440.0,
        ordem_no_processo=1,
        ativo=True,
    )
    session.add(c4_0)

    session.commit()
