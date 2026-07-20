# 📌 Quadro do Projeto (Project Board) — Forno Fundição

Este documento organiza o backlog de tarefas e o status do desenvolvimento do projeto **Forno Fundição**, dividido pelas colunas do Kanban e alinhado aos Milestones do GitHub.

---

## 🎯 Visão Geral das Fases (Milestones)

*   **Fase 1: Ingestão Automática e Rastreabilidade (v0.1.0)** — *Foco Atual (MVP)*
*   **Fase 2: Campanha do Forno e Desgaste de Cadinhos**
*   **Fase 3: Painel em Tempo Real e Relatórios Fabris**

---

## 📋 Quadro Kanban do Projeto

### 🟢 Concluído (Done)
| Issue / Task | Categoria | Descrição | Merge / Commit |
|---|---|---|---|
| **#1** | `feat` | API mínima FastAPI com `/health` e CI/CD. | PR #1 |
| **#2** | `feat` | Modelos de banco SQLModel (`Pirometro`, `CodigoPirometro`, `Leitura` com `panela_id`) + Migração Alembic. | PR #15 (Closes #2) |
| **#6** | `test` | Estruturação da suíte de testes em `app/tests/` (Clean Arch) com **99.03% de cobertura**. | PR #14 (Closes #6) |
| **#10** | `docs` | Levantamento de requisitos, diagramas de caso de uso e sequência, especificação Direct-to-DB e guia do receptor USB 24/7. | PR #16 (Closes #10) |

---

### 🟡 Em Progresso (In Progress)
| Issue / Task | Milestone | Categoria | Descrição / Próximo Passo | Responsável |
|---|---|---|---|---|
| **#12** | Fase 1 (v0.1.0) | `infra` | **Setup do Servidor Host 24/7**: Conectar receptor USB no PC Host/Servidor da fábrica e configurar o software para gravação direta no PostgreSQL (Opção A). | Infra TI / Dev |
| **#13** | Fase 1 (v0.1.0) | `backend` | **Ingestor de Leituras e Validação Térmica**: Criar o serviço de backend que processa novas leituras gravadas no Postgres, valida a faixa térmica (`temp_min`/`temp_max`) e notifica o painel. | Dev |

---

### 🔴 A Fazer (To Do / Backlog)

#### 🎯 Fase 1 — MVP (v0.1.0)
1. **[#11] Rastreabilidade de Corridas, Lotes e Panelas**:
   - Implementar os endpoints e formulários de seleção rápida para o operador associar a Corrida, Lote e Panela ativa no forno.
2. **[#3] Repositórios Concretos de Dados**:
   - Implementar `PirometroRepository` e `LeituraRepository` em `app/adapter/repositories/` estendendo as interfaces do domínio.
3. **[#4] Casos de Uso Core**:
   - Implementar `CadastrarLeituraUseCase` e `ListarLeiturasDoDiaUseCase` em `app/core/application/use_cases/`.
4. **[#5] Endpoints FastAPI de Leituras e Pirômetros**:
   - Expor as rotas HTTP `/api/v1/pirometros` e `/api/v1/leituras` integrando via contêiner de injeção de dependência (`container.py`).

#### 🧪 Fase 2 — Campanha do Forno e Cadinhos
5. **[#9] Controle de Desgaste dos Cadinhos**:
   - Criar o acompanhamento de desgaste e histórico da vida útil do refratário do forno via GitHub Issues / Banco de Dados.

#### 📊 Fase 3 — Painel e Interface Fabril
6. **[#7] Frontend Web Responsivo (Dashboard da Fábrica)**:
   - Desenvolver a interface gráfica web para exibição em tempo real do estado dos 4 fornos na fábrica com alertas sonoros/visuais.

---

## ⚙️ Diretrizes de Execução (Git Flow)

1. **Seleção de Tarefa**: Escolha uma issue da coluna **A Fazer (To Do)** vinculada ao **Milestone 1**.
2. **Criação da Branch**: Crie uma branch a partir de `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feat/nome-da-funcionalidade
   ```
3. **Desenvolvimento e Validação**: Desenvolva o código e execute `make validate` dentro de `app/` (garantindo build + format + lint + testes com min 90% cobertura).
4. **Pull Request**: Abra o PR apontando para `develop` adicionando no corpo: `Closes #<numero-da-issue>`.
