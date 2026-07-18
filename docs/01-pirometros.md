# Pirômetros — levantamento e modelo de dados

## Inventário atual (4 pirômetros)

| ID sugerido | Localização / Setor | Material | Processo | Molde | Status |
|---|---|---|---|---|---|
| PIR-01 | Centrífuga de Aço | SAE 1045 | Centrifugação | Coquilha (aço) | Em produção; nova centrífuga em aço em desenvolvimento |
| PIR-02 | Fundição de Aço (ligas) | 1052, 8640, 4130, 4330 | Fundição em molde | Areia | Em produção; centrífuga em areia em desenvolvimento |
| PIR-03 | Fundição de Ferro | Ferro fundido cinzento | — | — | Em produção |
| PIR-04 | Fundição de Ferro | Ferro fundido nodular | — | — | Em produção |

> Confirmar com o chefe/operadores se PIR-03 e PIR-04 são fisicamente dois
> aparelhos distintos ou o mesmo pirômetro usado para as duas ligas de ferro
> em momentos diferentes — isso muda o cadastro (ver [04-perguntas-abertas.md](04-perguntas-abertas.md)).

## O problema central: código 0–99 não tem significado fixo

O pirômetro só oferece ao operador uma faixa de **0 a 99** para "rotular" cada
medição antes de medir. O aparelho não sabe nada sobre metalurgia — o
significado do número é inteiramente definido pelo **procedimento do setor**.

Exemplo hipotético levantado na conversa:
- Operador seleciona **0** no pirômetro → mede → o `0` aparece associado à leitura.
- Isso pode ser interpretado, por convenção da fábrica, como **"liberação de forno"**.

Cada setor (centrífuga de aço 1045, fundição de aço-liga, fundição de ferro)
tem etapas e faixas de temperatura diferentes. Forçar todos os pirômetros a
usarem o mesmo dicionário de códigos (ex.: "0 sempre é liberação de forno, em
qualquer pirômetro") seria arbitrário e frágil — quebra assim que um setor
precisar de uma etapa que os outros não têm, ou tiver uma ordem de etapas diferente.

### Decisão: tabela de códigos por pirômetro

Em vez de um dicionário global fixo, cada pirômetro tem sua **própria tabela de
códigos cadastrada no sistema**:

```
pirometro (id, nome, setor, material_alvo, processo, molde, ativo)
codigo_pirometro (id, pirometro_id, codigo [0-99], etapa_nome, descricao,
                   temp_min_esperada, temp_max_esperada, ordem_no_processo, ativo)
leitura (id, pirometro_id, codigo_pirometro_id, temperatura_lida,
         operador_id, timestamp, corrida_id/lote_id, observacao)
```

Vantagens dessa modelagem:

- **Resiliente a pirômetros novos**: cadastrar um pirômetro novo (ex. a
  centrífuga em aço em desenvolvimento, ou a centrífuga em areia) é só inserir
  uma linha em `pirometro` + sua tabela de códigos — nenhuma mudança de código
  do sistema.
- **Cada setor mantém seu próprio vocabulário**: código `0` pode significar
  "liberação de forno" no PIR-01 e "início de vazamento" no PIR-03, sem conflito,
  porque o significado está amarrado ao `pirometro_id`, não é global.
- **Validação automática por faixa**: se o operador mede um valor fora de
  `temp_min_esperada`/`temp_max_esperada` para aquele código, o sistema pode
  alertar (ex.: para 1045 a liberação de forno tem uma faixa; para 8640 outra).
  Isso só é possível porque a faixa é por código+pirômetro, não fixa no sistema.
- **Auditoria e relatório por etapa**: dá pra responder "quantas liberações de
  forno houve essa semana na centrífuga de aço" filtrando por
  `pirometro_id + etapa_nome`, mesmo que o código numérico seja diferente em
  cada pirômetro.

### O que NÃO fazer

- Não gravar apenas o número 0–99 cru sem o `pirometro_id` junto — o mesmo
  número em pirômetros diferentes tem significado diferente, então sem essa
  referência o dado histórico vira ambíguo/inútil.
- Não fixar no código-fonte da aplicação uma lista fechada de pirômetros —
  isso é dado, deve estar no banco, não no código (é o motivo de existir a
  tabela `pirometro`).

## Cadastro inicial de códigos (a preencher com os operadores/chefe)

Ainda não temos, desta conversa, o detalhe de quais etapas cada setor usa (ex.:
quais números o operador usa hoje informalmente, e o que cada um significa).
Isso precisa ser levantado antes de popular `codigo_pirometro`. Ver
[04-perguntas-abertas.md](04-perguntas-abertas.md).
