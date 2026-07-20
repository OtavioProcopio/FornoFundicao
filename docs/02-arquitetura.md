# 🏛️ Arquitetura do Sistema — Ingestão Automática Direct-to-DB (24/7)

## 💡 Princípios de Arquitetura Confirmados

1. **Ingestão 100% Automática (Sem Apontamento Manual)**: Os pirômetros transmitem os dados via rádio para o receptor USB.
2. **Conexão Direta ao Banco (Opção A Exclusiva)**: O software do receptor USB insere diretamente as medições no banco de dados PostgreSQL. A opção de leitura via Excel foi descartada e declarada inviável.
3. **Servidor Host Dedicado 24/7 (Infraestrutura)**: O receptor USB **não pode ficar no computador pessoal da chefia**, pois este é desligado ao fim do expediente. O receptor USB e o software correspondente devem estar instalados em um **PC Host / Servidor Dedicado que permaneça ligado 24/7** na fábrica.

---

## 🏗️ Diagrama de Infraestrutura e Fluxo de Dados

```
  [4 Pirômetros Físicos (Fábrica)]
                 │
                 │ (Sinal de Rádio / Wireless 24/7)
                 ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 💻 Servidor Host / PC Dedicado da Fábrica (Ligado 24/7)    │
 │                                                             │
 │   [Receptor USB Físico] ◄── Plugado na porta USB           │
 │            │                                                │
 │            ▼                                                │
 │   [Software do Receptor USB]                                │
 │            │ (Grava direto via driver SQL/Postgres)         │
 └────────────┼────────────────────────────────────────────────┘
              │
              ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 🗄️ PostgreSQL (Banco de Dados Local)                       │
 └────────────┬────────────────────────────────────────────────┘
              │
              ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 🌐 Backend API (FastAPI + Clean Architecture)               │
 │    - Valida limites térmicos em tempo real                  │
 │    - Atribui contexto (Corrida, Lote, Panela)               │
 └────────────┬────────────────────────────────────────────────┘
              │
              ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 🖥️ Painel Web da Fábrica (Dashboards e Alertas em Tela)     │
 └─────────────────────────────────────────────────────────────┘
```

---

## 🔒 Governança de Infraestrutura

*   **Redirecionamento do Hardware**: O receptor USB deve ser fisicamente transferido do computador da chefia para o servidor local ou PC dedicado da fundição.
*   **Serviço de Inicialização Automática (Daemon/Service)**: O software do receptor USB no PC Host 24/7 deve ser configurado como Serviço do Sistema Operacional (Windows Service ou Daemon Linux) para iniciar automaticamente em caso de reinicialização do servidor.
