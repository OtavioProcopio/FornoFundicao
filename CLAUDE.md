# Forno Fundição — instruções para agentes

Sistema para digitalizar o registro de medições de pirômetros da Rei Auto
Parts (ver `docs/00-visao-geral.md` para o contexto completo do negócio).

## Antes de trabalhar

1. Leia `docs/00-visao-geral.md` a `docs/04-perguntas-abertas.md` pra entender
   o domínio (pirômetros, codificação 0–99, setores de fundição).
2. Leia `docs/git-workflow.md` — este repo segue Git Flow (`main`/`develop`/
   `feature`/`release`/`hotfix`), não é livre pra commitar direto em `main`
   ou `develop`.
3. Leia `docs/automacao-ci.md` pra entender o ciclo issue → PR → fechamento
   automático antes de abrir uma PR.

## Ferramental — SEMPRE use o devcontainer/Makefile

Este repo tem `.devcontainer/` (Python 3.11 + Postgres) e `app/Makefile`
prontos. **Não instale dependências soltas no sistema, não crie venv manual
fora do container.** O fluxo correto é:

```bash
# abrir o repo no devcontainer (VS Code: "Reopen in Container", ou
# `devcontainer up` via CLI) — isso já sobe Python 3.11 + Postgres
cd app
make install   # cria .venv dentro do container, se preferir rodar fora do docker-compose da API
make build     # compila
make lint      # flake8 + mypy
make test      # pytest (unit)
make test-coverage
make up        # sobe api + postgres via docker compose (app/docker-compose.yml)
make migrate   # aplica migrations Alembic dentro do container da API
```

Se o devcontainer não estiver disponível no ambiente do agente, use
`docker compose` diretamente (`app/docker-compose.yml`) em vez de instalar
pacotes Python no host — mantém o ambiente idêntico ao CI.

## Stack e arquitetura da API

A API (`app/`) segue o mesmo padrão de Clean Architecture usado no projeto
`area-verde` (referência): FastAPI + SQLModel + Alembic + PostgreSQL +
`dependency-injector`.

```
app/core/domain/        → Entidades, enums (0 deps de framework)
app/core/application/   → Use cases
app/core/interfaces/    → Ports (interfaces de repositório/infra)
app/adapter/            → Controllers, repositórios concretos
app/infra/              → Config (settings, container DI, database), tools (logger)
app/api.py              → Bootstrap do FastAPI, inclui /health
```

- Novos endpoints: controller em `adapter/controllers/`, caso de uso em
  `core/application/use_cases/`, modelo em `core/domain/models.py`.
- Nunca acesse o banco direto do controller — sempre via use case + porta de
  repositório definida em `core/interfaces/`.
- Migrations sempre via Alembic (`app/migrations/`), nunca alteração manual
  de schema.

## Regras de commit e PR

- Toda mudança nasce de uma branch a partir de `develop`
  (`feat/*`, `fix/*`, `docs/*`, `chore/*` — ver `docs/git-workflow.md`).
- Commits em Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:` etc).
- PR que resolve uma issue **precisa** de `Closes #<numero>` no corpo (o
  template já tem o campo).
- Rodar `make build && make lint && make test` dentro de `app/` antes de
  abrir PR (ver `app/Makefile`).

## O que NÃO fazer

- Não commitar `.env` real, senha, token ou chave.
- Não misturar escopo de pirômetros com o escopo futuro de espectrômetros
  (`docs/03-espectrometros.md`) ou CLPs — são fases separadas.
- Não fixar a lista de pirômetros em código — é dado (tabela `pirometro` +
  `codigo_pirometro`), não constante (ver `docs/01-pirometros.md`).
