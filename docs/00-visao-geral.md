# Sistema de Monitoramento de Fornos e Pirômetros — Rei Auto Parts

## Contexto do negócio

A Rei Auto Parts funde peças (cardans e derivados: luvas/luveiras, acoplamentos, ponteiras)
em três frentes principais de processo, cada uma com sua própria metalurgia e forma de molde:

| Setor | Material(is) | Processo | Molde | Observações |
|---|---|---|---|---|
| Fundição Centrífuga (Aço) | SAE 1045 | Centrifugação | Coquilha de aço | Linha consolidada; também em desenvolvimento uma nova centrífuga em aço |
| Fundição de Aço (ligas) | 1052, 8640, 4130, 4330 | Fundição em molde | Areia | Centrífuga em areia também em desenvolvimento |
| Fundição de Ferro | Ferro fundido cinzento e nodular | — | — | 2 pirômetros aqui |

Total: **4 pirômetros** hoje (1 na centrífuga de aço 1045, 1 na fundição de aço-liga,
2 na fundição de ferro), com expectativa de **crescer** (novas centrífugas em
desenvolvimento, possíveis pirômetros adicionais).

Além disso, o gestor pediu, num segundo momento, alguma solução para os
**espectrômetros** (ver [03-espectrometros.md](03-espectrometros.md)) — mais desafiador porque
os PCs conectados a eles hoje não têm acesso à rede.

## Objetivo do sistema (fase 1)

Digitalizar e padronizar o registro das medições de temperatura feitas pelos
pirômetros em cada etapa do processo de fundição, permitindo:

1. Rastreabilidade por corrida/panela/lote de fundição (quem mediu, quando, em que etapa, que temperatura).
2. Liberação formal de forno (registrar o momento em que a fundição foi autorizada a vazar).
3. Base de dados histórica para depois cruzar com qualidade de peça, consumo de energia, tempo de ciclo etc.
4. Estrutura que **não trava** quando aparecer o 5º, 6º pirômetro (novas linhas em desenvolvimento).

## Por que isso é mais que "cadastrar leituras de pirômetro"

O desafio real, levantado nesta conversa, é de **modelagem**: os pirômetros são
aparelhos genéricos que só sabem mostrar um **código numérico de 0 a 99** escolhido
pelo operador antes da medição. O significado desse código (ex.: "0 = liberação de
forno") é **convenção de processo**, não uma propriedade do equipamento — e cada
setor tem seu próprio procedimento e faixas de temperatura. Ver detalhes e decisão
em [01-pirometros.md](01-pirometros.md).

## Documentos deste diretório

- [01-pirometros.md](01-pirometros.md) — levantamento dos 4 pirômetros, o problema da codificação 0–99, e o modelo de dados escolhido.
- [02-arquitetura.md](02-arquitetura.md) — proposta de arquitetura do sistema (app web local + banco de dados).
- [03-espectrometros.md](03-espectrometros.md) — notas sobre o pedido futuro de integração com espectrômetros e o problema de PCs sem rede.
- [04-perguntas-abertas.md](04-perguntas-abertas.md) — lista de perguntas para validar com o chefe/operadores antes de fechar o modelo de dados.

## Decisões já tomadas (confirmadas com o Otávio em 2026-07-18)

- **Codificação 0–99**: cada pirômetro terá sua **própria tabela de códigos**
  (código → etapa/significado → faixa de temperatura esperada), cadastrável no
  sistema — não um código universal fixo igual para todos.
- **Formato inicial**: aplicativo web local, rodando a partir do PC da chefe
  (que hoje já tem acesso a um banco de dados), acessível pela rede da fábrica,
  com banco de dados próprio.
