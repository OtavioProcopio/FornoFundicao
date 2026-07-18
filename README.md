# Forno Fundição

Sistema para digitalizar e padronizar o registro de medições de temperatura
feitas nos pirômetros das linhas de fundição da Rei Auto Parts (centrífuga de
aço 1045, fundição de aço-liga, fundição de ferro), com plano de evolução
para integração futura com espectrômetros e CLPs dos fornos.

**Status:** levantamento e documentação (pré-implementação).

## Documentação

| | |
|---|---|
| 📋 [Visão Geral](docs/00-visao-geral.md) | Contexto do negócio, setores de fundição, objetivo da fase 1 |
| 🌡️ [Pirômetros](docs/01-pirometros.md) | Inventário dos 4 pirômetros e modelo de dados da codificação 0–99 |
| 🏗️ [Arquitetura](docs/02-arquitetura.md) | Proposta de sistema (app web local + banco de dados) |
| 🔬 [Espectrômetros](docs/03-espectrometros.md) | Notas sobre o pedido futuro e o problema dos PCs sem rede |
| ❓ [Perguntas Abertas](docs/04-perguntas-abertas.md) | Pontos a validar com o chefe/operadores |
| 🌳 [Fluxo de Git](docs/git-workflow.md) | Branches, convenção de commits e processo de PR |

## Fluxo de trabalho

Este repositório segue Git Flow simplificado (`main` / `develop` / branches de
feature). Ver [docs/git-workflow.md](docs/git-workflow.md) para detalhes.
