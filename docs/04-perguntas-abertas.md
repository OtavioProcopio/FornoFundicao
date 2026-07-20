# 🔍 Perguntas Abertas e Mapeamento de Processo

Este documento consolida o estado das perguntas abertas sobre o modelo de negócios do projeto **Forno Fundição**, registrando as respostas dadas pela gestão da Rei Auto Parts e estabelecendo o questionário de mapeamento para as próximas etapas.

---

## 🟢 1. Respostas Consolidadas (Validações Realizadas)

### Sobre os Pirômetros e Códigos
*   **Lista de Códigos (0-99)**: Hoje, os códigos numéricos de 0 a 99 ainda não são utilizados para indicar nada específico operacionalmente.
*   **PIR-03 e PIR-04**: São dois equipamentos físicos diferentes (um dedicado a ferro cinzento e outro a ferro nodular).
*   **Novas Centrífugas**: No futuro, a inclusão de uma nova centrífuga pode ocorrer sob duas formas: realocação de um pirômetro existente ou aquisição de um novo aparelho físico.

### Sobre Operação e Rastreabilidade
*   **Identificadores de Corrida/Lote**: Sim, existem identificadores de **Corrida** (lote de fusão) e **Lote** (lote de peças). Atualmente, os operadores anotam estes dados à mão em papel.
*   **Identificação de Panelas (Ladles)**: Não há numeração oficial de panelas hoje. No entanto, há interesse dos gestores em implementar essa identificação física e amarrar o número da panela a cada leitura de temperatura para melhorar a rastreabilidade.
*   **Desgaste dos Cadinhos**: Existe uma necessidade formal do PO de controlar o desgaste dos cadinhos para acompanhar a **Campanha do Forno** (vida útil operacional do cadinho). Hoje, esse registro é manual no papel. A ideia inicial é gerenciar e rastrear isso por meio de **Issues no GitHub** (abrindo uma issue por campanha e registrando o histórico de desgaste nela).

---

## 📋 2. Questionário para Mapeamento de Procedimentos de Campo

Para explorar e formalizar os procedimentos industriais na Rei Auto Parts, o gestor deve mapear as seguintes perguntas junto à equipe de operação:

### Seção A: Mapeamento de Etapas do Processo e Limites Térmicos
1. **Quais são as etapas oficiais do processo de fusão/vazamento?** (Ex: fusão inicial, tratamento da liga, inoculação, vazamento na centrífuga).
2. **Quais ligas metálicas são produzidas em cada pirômetro?** (Ex: Ferro Cinzento no PIR-03, Ferro Nodular no PIR-04, etc.).
3. **Quais são as faixas de temperatura aceitáveis (mínima e máxima) esperadas por liga e por etapa?** (Estes limites serão usados para emitir alertas visuais no sistema).
4. **O que o operador deve fazer caso uma leitura apresente temperatura fora da faixa?** (Há alguma ação de segurança imediata ou apenas o registro visual do alerta?).

### Seção B: Rastreabilidade (Corrida, Lote e Panelas)
5. **Como é gerado o código de identificação de uma "Corrida"?** (Ex: segue uma data `AAAAMMDD-XX`, é um sequencial anual, etc.).
6. **Qual a relação física entre Corrida e Lote?** (Uma única corrida abastece vários lotes de moldagem/centrifugação, ou um lote é composto de metal de várias corridas?).
7. **Como as panelas (ladles) são utilizadas?**
   - Elas possuem tamanhos/capacidades diferentes?
   - Quantas corridas uma panela aguenta antes de refazer o refratário?
   - Como pretendem implementar a identificação das panelas? (Ex: pintura de números de 1 a N nas panelas físicas).

### Seção C: Campanha do Forno e Desgaste de Cadinhos (Crucible)
8. **Qual é a vida útil típica estimada de um cadinho?** (Em número de corridas ou dias de trabalho).
9. **Como é avaliada a espessura/desgaste do cadinho hoje?** (Medição física com paquímetro/gabarito ou apenas inspeção visual de trincas?).
10. **Quais são os principais eventos de manutenção do cadinho?** (Ex: instalação de cadinho novo, reparo de refratário, descarte por fim de vida útil).
11. **Quem é responsável por aprovar a troca de um cadinho?**

### Seção D: Rotina e Dispositivos
12. **Como o operador interage com o apontamento de dados?**
    - Ele consegue digitar as informações em um tablet/celular posicionado perto do forno (considerando calor, poeira e luvas), ou o ideal é que a digitação ocorra via computador fixo após o encerramento do lote?
13. **Existe um modelo padrão (planilha ou ficha de papel) usado atualmente?** (Obter uma imagem ou cópia desse registro é fundamental para desenharmos as telas do sistema).

---

## 🟡 3. Novas Perguntas em Aberto (Próxima Rodada)

As seguintes dúvidas técnicas e de escopo ainda precisam ser respondidas ou mapeadas:

1. **Liberdade de Usuários no Sistema**: Qual será o nível de permissão de cada perfil? (Ex: Operador pode apenas ler/digitar leituras do seu turno? Supervisor pode alterar parâmetros e visualizar relatórios históricos? Admin pode cadastrar novos pirômetros?).
2. **Fluxo da Planilha Atual**: Qual é o caminho que os dados percorrem hoje nas planilhas? (Quem digita a planilha, onde ela fica salva, quem a analisa e com que frequência?).
3. **Integração com GitHub para Cadinhos**: Para o controle de desgaste dos cadinhos via Issues do GitHub:
   - A equipe de operação terá acesso ao GitHub para ler/criar issues, ou os gestores farão essa interface manual/automatizada?
   - Deseja que criemos um template de issue no repositório (`.github/ISSUE_TEMPLATE/`) específico para o controle de campanha de forno?
4. **Infraestrutura e Espectrômetros**: Como trataremos a conectividade dos PCs dos espectrômetros? (Esta questão foi postergada para a Fase 2, mas fica registrada para acompanhamento de viabilidade técnica).
