# Espectrômetros (pedido futuro do chefe)

## O pedido

O chefe também pediu, à parte, algo relacionado à medição/registro dos
espectrômetros (análise de composição química do metal fundido).

## O desafio identificado

Os PCs conectados aos espectrômetros **não têm acesso à rede**. Isso é comum em
equipamentos de laboratório mais antigos ou por política de segurança do
fabricante do equipamento. Isso impede a abordagem óbvia (app web acessando
banco central em tempo real a partir desse PC).

## Alternativas (para avaliar quando chegar a hora, não é escopo agora)

1. **Exportação manual + importação**: o espectrômetro normalmente grava um
   relatório (PDF/CSV/TXT) localmente. Um operador copia esse arquivo (pendrive,
   ou pasta compartilhada se houver *qualquer* rede local isolada) para
   importar no sistema depois. Mais simples, sem mexer na rede do equipamento.
2. **Rede segregada com uma via de saída controlada**: colocar esses PCs numa
   VLAN isolada com um único ponto de saída (ex. uma pasta de rede só de
   escrita, ou um serviço local que sincroniza periodicamente) — requer aval
   de TI/segurança e entender por que a rede foi bloqueada originalmente
   (pode ser exigência do fabricante do espectrômetro).
3. **Digitação manual do resultado**: se o volume de análises for baixo,
   pode não valer a pena a complexidade de integração — só cadastrar o
   resultado da análise no mesmo sistema, manualmente, como se faz hoje com
   os pirômetros.

## Recomendação

Tratar como **fase 2, projeto separado**. Antes de desenhar qualquer solução,
levantar: por que o PC não tem rede (bloqueio de TI, exigência do
fabricante, ou simplesmente nunca foi cabeado), qual o formato de saída do
espectrômetro (arquivo, impressão, tela apenas), e qual o volume de análises
por dia.
