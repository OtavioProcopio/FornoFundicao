# 🏛️ Arquitetura do Sistema — Ingestão Automática de Pirômetros

## 💡 Mudança Fundamental de Escopo: Fim do Apontamento Manual
Conforme alinhado com a gestão, **os pirômetros já possuem um receptor USB conectado a um PC local na fábrica**, rodando um software proprietário do fabricante que recebe os dados dos pirômetros automaticamente via rádio/wireless.

Portanto, **o sistema NÃO terá apontamento manual de temperatura**. O fluxo passa a ser **100% automatizado na coleta de dados térmicos**.

---

## 🏗️ Modos de Ingestão de Dados do Receptor USB

O software instalado no PC possui duas capacidades que aproveitaremos:

### Opção A: Conexão Direta ao Banco de Dados (Preferencial)
*   **Como Funciona**: Configuramos as credenciais do nosso banco de dados (PostgreSQL local) no software do receptor USB.
*   **Fluxo**: O software insere diretamente as leituras recebidas via USB nas tabelas de staging/leitura do PostgreSQL.
*   **Vantagem**: Latência de milissegundos, sem intermediários.

### Opção B: Importador/Watcher de Planilhas Excel/CSV (Fallback)
*   **Como Funciona**: Se o software do receptor apenas salvar arquivos `.xlsx` ou `.csv` em uma pasta local/compartilhada, o backend do nosso sistema terá um serviço de **File Watcher / Parser**.
*   **Fluxo**: O backend detecta novos registros inseridos na planilha Excel e os importa automaticamente para o PostgreSQL.
*   **Vantagem**: Funciona mesmo se o software do receptor tiver limitações no suporte a banco de dados.

---

## 🔄 Novo Fluxo do Sistema

```
[4 Pirômetros Físicos]
       │ (Sinal Wireless)
       ▼
[Receptor USB + Software no PC]
       │
       ├──► (Opção A) Gravação Direta no PostgreSQL
       └──► (Opção B) Exportação Excel ──► [Watcher/Importador Backend] ──► PostgreSQL
                                                                               │
                                                                               ▼
                                                            [API FastAPI + Regras de Negócio]
                                                                               │
                                                                               ├──► Enriquecimento (Corrida/Lote/Panela)
                                                                               ├──► Validação de Limites Térmicos
                                                                               └──► Dashboards & Alertas em Tempo Real
```

---

## 🎯 Novo Papel do Sistema (Painel de Monitoramento & Rastreabilidade)

Como o operador não precisa mais digitar a temperatura:
1. **Monitoramento Automático**: A tela exibe as temperaturas chegando em tempo real.
2. **Associação de Rastreabilidade**: O operador/supervisor apenas associa a corrida/lote/panela ativa ao pirômetro do forno naquele momento (1 clique/campo).
3. **Alertas Visuais**: Se a temperatura coletada automaticamente pelo USB estiver fora da faixa daquela etapa/liga, o sistema emite alerta sonoro/visual.
