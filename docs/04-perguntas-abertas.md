# 🔍 Perguntas Abertas — Validação do Software Receptor USB

Este documento consolida o estado das perguntas abertas sobre o modelo de negócios e a integração automática com o **software do receptor USB dos pirômetros** instalado no computador da gestão.

---

## 🟢 1. Respostas Consolidadas (Atualização de Escopo)

*   **Fim do Apontamento Manual de Temperatura**: Confirmado que os pirômetros possuem um receptor USB conectado a um computador local na fábrica (PC da chefe) que já recebe os dados de medição.
*   **Modo de Ingestão**: O sistema coletará os dados **automaticamente** do software do receptor USB (seja configurando o nosso banco de dados PostgreSQL diretamente no software, ou através de um importador contínuo de planilhas Excel/CSV geradas por ele).
*   **Identificadores de Corrida/Lote/Panela**: Como a temperatura vem automática pelo rádio USB, o operador/supervisor usará o sistema apenas para vincular a corrida/lote/panela ativa ao forno ou visualizar o painel em tempo real.

---

## 📋 2. Perguntas Técnicas sobre o Software do Receptor USB

Para definirmos a forma de integração (Opção A: Banco Direto ou Opção B: Importador Excel), precisamos inspecionar o software no PC da chefe:

1. **Nome do Software e Fabricante**: Qual é o nome do programa/software instalado no PC da chefe que gerencia o dispositivo USB?
2. **Suporte a Banco de Dados (Opção A)**:
   - Nas telas de *Configurações* / *Preferências* / *Exportação* desse software, existe alguma opção para conectar a um banco de dados SQL (ex: PostgreSQL, SQL Server, MySQL, ODBC)?
   - Se sim, podemos simplesmente criar o banco PostgreSQL, passar as credenciais (host, porta, usuário, senha) para o software, e ele passará a gravar diretamente na nossa base.
3. **Exportação para Planilha Excel/CSV (Opção B - Fallback)**:
   - Se o software não tiver conexão com banco de dados, em qual pasta do computador ele salva o arquivo Excel (`.xlsx`) ou CSV?
   - Ele atualiza um único arquivo continuamente ou gera um arquivo novo por dia/turno?

---

## 🟡 3. Novas Perguntas em Aberto

1. **Localização do Servidor/PC**: Onde a nossa API/PostgreSQL vai rodar? (No mesmo PC da chefe onde está o receptor USB ou em um servidor/computador separado na mesma rede local?).
2. **Tempo Real na Fábrica**: Haverá uma TV/Monitor no setor de fundição exibindo o painel web das medições em tempo real para os operadores?
