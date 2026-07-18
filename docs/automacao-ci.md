# Automação: CI, Issues e PRs

Este repositório fecha o ciclo "problema → issue → PR → resolução automática"
usando só recursos nativos do GitHub Actions/GitHub, sem serviço externo.

## Fluxo

1. **CI roda em toda PR e push** para `develop`/`main`
   (`.github/workflows/ci.yml`): build, lint, type check, testes.
2. **Se o CI falhar num push direto a `develop` ou `main`**, o workflow
   `.github/workflows/issue-on-failure.yml` abre automaticamente uma Issue
   com o link do run que falhou, label `bug` e `ci-failure`. Ele evita
   duplicar: se já existe uma issue aberta com a mesma label para aquele
   workflow, não cria outra.
3. **Um agente (humano ou IA) resolve a issue** criando uma branch a partir de
   `develop` (`fix/*` ou `bugfix/*`, conforme [git-workflow.md](git-workflow.md))
   e abrindo PR.
4. **A PR deve conter `Closes #<numero-da-issue>`** no corpo (campo já existe
   no `.github/PULL_REQUEST_TEMPLATE.md`). Ao mergear a PR, o GitHub fecha a
   issue automaticamente — não é preciso nenhuma action extra para isso, é
   comportamento nativo do GitHub para as palavras-chave `Closes`/`Fixes`/`Resolves`.

## Por que não automatizar o fechamento com uma Action própria

Fechar issues via `Closes #N` no corpo do PR já é nativo do GitHub (funciona
assim que o PR é mergeado na branch padrão do repositório, ou em qualquer
branch se configurado). Criar uma Action para isso seria reinventar algo que
já funciona de graça e sem manutenção. O único ponto que precisa de automação
de fato é a **abertura** da issue quando algo quebra — isso sim não existe
pronto, por isso o `issue-on-failure.yml`.

## Extensões futuras (não implementadas ainda)

- Rodar `issue-on-failure` também para falhas em PR (hoje só cobre push direto
  em `develop`/`main`, que é quando algo quebrou a branch de integração).
- Auto-atribuir a issue a quem fez o commit que quebrou o build.
- Fechar automaticamente issues de dependência desatualizada via Dependabot
  (o Dependabot já faz isso nativamente quando configurado com
  `.github/dependabot.yml`, caso seja necessário no futuro).
