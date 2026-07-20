# 🏛️ System Design & Arquitetura de Engenharia — Forno Fundição

Este documento especifica o **System Design completo** do projeto **Forno Fundição**, abordando o planejamento de banco de dados (ERD e indexação), workflows de dados e operação, infraestrutura, ferramentas de desenvolvimento, observabilidade, logging e métricas industriais.

---

## 📐 1. System Design & Topologia da Solução

### Diagrama de Containers (C4 Model Level 2)

```mermaid
graph TB
    subgraph Fabrica ["Unidade Fabril - Rei Auto Parts"]
        PIR["🌡️ Pirômetros Físicos (PIR-01 a PIR-04)"] -- "Sinal Rádio 24/7" --> USB["💻 PC Host Local 24/7 + Receptor USB"]
        USB -- "Driver Serial/SQL Direct" --> DB
        UI_TV["🖥️ Monitor TV Fábrica (WebSocket)"]
        UI_TAB["📱 Tablet Operador (Rastreabilidade)"]
    end

    subgraph Nuvem_VPS ["VPS Cloud / Servidor Local"]
        DB[("🗄️ PostgreSQL 16
        (Base de Dados)")]
        
        subgraph Backend_App ["App Core (FastAPI Container)"]
            API_CTRL["🌐 REST API Controllers"]
            WS_MGR["⚡ WebSocket Realtime Push"]
            USE_CASES["⚙️ Application UseCases"]
            REPO_IMPL["💾 SQLModel Repositories"]
            LOG_SYS["📝 Structured JSON Logger"]
        end
    end

    API_CTRL --> USE_CASES
    USE_CASES --> REPO_IMPL
    REPO_IMPL --> DB
    DB -. "LISTEN/NOTIFY ou Poll" .-> WS_MGR
    WS_MGR -- "WebSocket Push" --> UI_TV
    UI_TAB -- "POST REST API" --> API_CTRL
    LOG_SYS --> API_CTRL
```

---

## 🗄️ 2. Planejamento do Banco de Dados (Database Design)

### Diagrama de Entidade-Relacionamento (ERD)

```mermaid
erDiagram
    PIROMETRO ||--o{ CODIGO_PIROMETRO : "possui"
    PIROMETRO ||--o{ LEITURA : "recebe"
    CODIGO_PIROMETRO ||--o{ LEITURA : "classifica"
    PIROMETRO ||--o{ CADINHO_CAMPANHA : "monitora"
    CADINHO_CAMPANHA ||--o{ REGISTRO_DESGARTE_CADINHO : "registra"

    PIROMETRO {
        string id PK "PIR-01, PIR-02..."
        string nome "Centrífuga 1, etc."
        string setor "Aço, Ferro"
        string material_alvo "SAE 1045, Nodular"
        string processo "Centrifugação, Fundição"
        string molde "Coquilha, Areia"
        boolean ativo "default: true"
    }

    CODIGO_PIROMETRO {
        int id PK "Auto-increment"
        string pirometro_id FK "FK -> pirometro.id"
        int codigo "0 a 99"
        string etapa_nome "Liberação de Forno, etc."
        string descricao "Opcional"
        float temp_min_esperada "Temperatura Mínima"
        float temp_max_esperada "Temperatura Máxima"
        int ordem_no_processo "1, 2, 3..."
        boolean ativo "default: true"
    }

    LEITURA {
        int id PK "Auto-increment"
        string pirometro_id FK "FK -> pirometro.id"
        int codigo_pirometro_id FK "FK -> codigo_pirometro.id"
        float temperatura_lida "Valor em °C"
        string operador_id "Identificador Operador"
        datetime timestamp "Data/Hora UTC"
        string corrida_id "Lote de Fusão"
        string lote_id "Lote de Peças"
        string panela_id "Número da Panela / Ladle"
        string observacao "Justificativa/Notas"
    }

    CADINHO_CAMPANHA {
        int id PK "Auto-increment"
        string pirometro_id FK "FK -> pirometro.id"
        string codigo_identificador "Cadinho-2026-01"
        datetime data_instalacao "Data de início"
        int corridas_acumuladas "Contador de fusões"
        float espessura_inicial_mm "Espessura nova"
        float espessura_atual_mm "Espessura atual"
        string status "ATIVO, SUBSTITUIDO, ALERTA"
    }

    REGISTRO_DESGARTE_CADINHO {
        int id PK "Auto-increment"
        int cadinho_campanha_id FK "FK -> cadinho_campanha.id"
        float espessura_medida_mm "Medição atual"
        string operador_id "Responsável"
        datetime timestamp "Data/Hora"
        string observacao "Condições visuais"
    }
```

### Estratégia de Indexação e Desempenho (Indexes)
Para garantir consultas instantâneas no painel e relatórios gerenciais sem lentidão:
1. **Índice Composto por Equipamento e Timestamp**: `CREATE INDEX idx_leitura_pirometro_timestamp ON leitura (pirometro_id, timestamp DESC);`
2. **Índice de Rastreabilidade por Corrida e Lote**: `CREATE INDEX idx_leitura_corrida_lote ON leitura (corrida_id, lote_id);`
3. **Índice de Códigos Ativos**: `CREATE INDEX idx_codigo_pirometro_ativo ON codigo_pirometro (pirometro_id, codigo) WHERE ativo = true;`

---

## 🔄 3. Workflows de Dados & Operação

### Workflow A: Ingestão Automática e Disparo de Alerta Térmico
```
[Pirômetro Físico] ──(Rádio)──► [Receptor USB] ──(Driver SQL)──► [INSERT INTO leitura]
                                                                        │
                                                                        ▼
                                                             [Backend Service Listener]
                                                                        │
                                                              ┌─────────┴─────────┐
                                                              ▼                   ▼
                                                     [Busca Limites Código]  [Grava Log]
                                                              │
                                                     (Fora da Faixa?)
                                                      ├── SIM ──► Notifica WebSocket (Alerta Vermelho/Sonoro)
                                                      └── NÃO ──► Notifica WebSocket (Verde / Normal)
```

### Workflow B: Rastreabilidade (Vinculação de Corrida e Panela)
```
[Operador no Tablet] ──► Seleciona Forno PIR-01 ──► Define Corrida "CR-2026-88" & Panela "#3"
                                                                  │
                                                                  ▼
                                                      [API /api/v1/sessoes-forno]
                                                                  │
                                                                  ▼
                                         [Registra contexto ativo na memória do Ingestor]
                                                                  │
                                                                  ▼
                            [Novas leituras recebidas via USB herdam Corrida "CR-2026-88" e Panela "#3"]
```

---

## 🛠️ 4. Ferramentas de Desenvolvimento & Ambiente (DX)

*   **Ambiente Isolado (Devcontainer)**: `.devcontainer/` pré-configurado com Python 3.12, PostgreSQL 16 e dependências.
*   **Gestão de Tarefas (Makefile)**:
    *   `make install`: Cria venv e instala dependências.
    *   `make validate`: Executa `py_compile` + `black` + `isort` + `flake8` + `mypy` + `pytest` (exigindo **>90% de cobertura**).
    *   `make up`: Sobe container da API + PostgreSQL via Docker Compose.
    *   `make migrate`: Executa `alembic upgrade head`.
*   **Migrações de Banco (Alembic)**: Controle estrito de alterações de schema DDL com versionamento em código (`app/migrations/versions/`).

---

## 📊 5. Observabilidade, Logging e Métricas Industriais

### Formato de Log Estruturado (JSON)
Todos os componentes do sistema utilizam o logger unificado (`infra/tools/logger.py`), emitindo logs formatados em JSON para fácil agregação e auditoria:

```json
{
  "timestamp": "2026-07-20T03:08:00Z",
  "level": "WARN",
  "logger": "forno-fundicao",
  "event": "ALERTA_TEMPERATURA_FORA_DA_FAIXA",
  "pirometro_id": "PIR-01",
  "codigo": 5,
  "temperatura_lida": 1620.5,
  "temp_min_esperada": 1500.0,
  "temp_max_esperada": 1600.0,
  "corrida_id": "CR-2026-88",
  "panela_id": "P-03",
  "correlation_id": "req-98dc6b785c31"
}
```

### Métricas Industriais de Saúde (KPIs do Sistema)
1. **Ingestão Rate (Medições/Minuto)**: Volume de leituras capturadas por pirômetro.
2. **Taxa de Anomalias Térmicas (Alert Ratio)**: Porcentagem de leituras fora da faixa por turno/liga.
3. **Latência E2E de Ingestão**: Tempo decorrido desde a gravação do USB no PostgreSQL até a atualização da tela na fábrica (meta: `< 500ms`).
4. **Healthcheck Probes (`GET /health`)**:
   * Checagem de conectividade com o banco PostgreSQL.
   * Checagem de integridade do listener de recepção.
