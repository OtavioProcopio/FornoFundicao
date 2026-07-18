# Arquitetura proposta (fase 1 — pirômetros)

## Formato: aplicativo web local

Decisão confirmada: app web rodando localmente na rede da fábrica, com banco
de dados. A chefe já tem um PC que "oferece conexão a um banco de dados" —
vale confirmar (ver perguntas abertas) se isso é um SQL Server / Access / outro
já instalado, para decidir se aproveitamos ou subimos um banco novo (ex.
PostgreSQL) num serviço simples.

Proposta de componentes, do mais simples para o mais completo — começar pelo nível 1:

1. **Nível 1 (MVP)**: formulário web simples (rodando num PC/servidor da rede
   local) onde o operador escolhe o pirômetro, escolhe o código (0–99, já
   traduzido para o nome da etapa daquele pirômetro), digita a temperatura
   lida, e salva. Lista/relatório simples de leituras do dia por pirômetro.
2. **Nível 2**: amarrar cada leitura a uma "corrida" ou "lote" de fundição
   (para saber depois qual peça saiu de qual conjunto de medições).
3. **Nível 3**: alertas automáticos quando a temperatura sai da faixa esperada
   para aquele código/etapa; dashboards por setor/turno/operador.

## Por que começar simples

O pedido original do chefe foi só "um sistema para os pirômetros". Não expandir
escopo (cardans, espectrômetros, CLPs) até o nível 1 estar rodando e validado
com os operadores. Resiliência a novos pirômetros já está coberta pelo modelo
de dados (tabela `pirometro` + `codigo_pirometro`), não precisa de
complexidade extra de infraestrutura para isso.

## Rede e acesso

- 4 pirômetros hoje, sem indicação de que os próprios aparelhos tenham saída
  de rede/API — a leitura hoje é manual (operador lê o mostrador do
  pirômetro e digita em algum lugar). Confirmar isso antes de imaginar
  integração automática (alguns pirômetros industriais têm saída RS-485/4-20mA/
  Modbus, mas isso é outro projeto).
- O sistema, nesta fase, é primariamente um **formulário de apontamento
  manual** + banco de dados + relatórios. Não pressupor leitura automática do
  instrumento.

## CLPs dos fornos (nota, não escopo da fase 1)

O usuário mencionou que os fornos têm CLPs e que talvez dê pra conectá-los à
rede e puxar dados deles. Isso é tecnicamente viável (a maioria dos CLPs
industriais fala Modbus TCP/RTU, Profinet, ou tem gateway OPC-UA), mas é um
projeto à parte, com riscos de segurança/operação (rede de automação
normalmente é segregada da rede de escritório por boas razões). Não misturar
com a entrega dos pirômetros — registrar como possível fase futura.
