# Perguntas abertas — validar antes de codar o modelo de dados

## Sobre os pirômetros e códigos

1. Para cada um dos 4 pirômetros: qual é, hoje, a lista real de códigos
   (0–99) que o operador usa e o que cada um significa? (ex.: planilha ou
   procedimento escrito que já exista informalmente.)
2. PIR-03 e PIR-04 (ferro cinzento e nodular) são dois aparelhos físicos
   diferentes ou o mesmo pirômetro usado ora para uma liga, ora para outra?
3. Existe uma faixa de temperatura esperada (mín/máx) documentada por
   etapa/liga hoje (mesmo que informalmente, no caderno do operador)? Isso
   viraria `temp_min_esperada`/`temp_max_esperada`.
4. Quando uma nova centrífuga (aço, ou em areia) entrar em produção, o
   pirômetro dela vai ser um dos 4 existentes realocado, ou um aparelho novo?

## Sobre operação e rastreabilidade

5. Existe hoje algum identificador de "corrida" ou "lote" de fundição (número
   de panela, ordem de produção, etc.) que devêssemos amarrar à leitura? Ou a
   fase 1 é só "leitura solta com timestamp"?
6. Quem vai operar o sistema: só o operador que mede no pirômetro, ou
   também a chefe/supervisão para consultar relatórios?
7. O formulário de apontamento deve ser preenchido no momento da medição
   (celular/tablet perto do forno) ou depois, num PC fixo?

## Sobre infraestrutura

8. O banco de dados que a chefe já tem acesso — qual é (SQL Server, Access,
   MySQL, outro)? Isso decide se aproveitamos a infra existente ou subimos
   banco novo.
9. Existe already uma rede cabeada/Wi-Fi cobrindo os 4 pontos dos
   pirômetros, ou isso também precisa ser resolvido?

## Sobre espectrômetros (fase 2)

10. Por que os PCs dos espectrômetros não têm rede — bloqueio de TI, exigência
    do fabricante, ou nunca foi cabeado?
11. Qual o formato de saída do resultado da análise (arquivo local, impressão,
    só tela)?
