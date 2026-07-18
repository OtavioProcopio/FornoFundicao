# Fluxo de Git

Mesmo padrão usado nos projetos RGM (rgm-backend, rgm-frontend, rgm-infra).

## Branches principais

- `main` — sempre em estado estável/publicável. Só recebe merge vindo de `develop`
  (ou hotfix), nunca commit direto.
- `develop` — branch de integração. Todo trabalho novo nasce a partir dela e
  volta pra ela via PR.

## Branches de trabalho

Prefixo indica o tipo de mudança (usado também para label automático de PR):

| Prefixo | Uso |
|---|---|
| `feat/` | Nova funcionalidade |
| `fix/` | Correção de bug |
| `hotfix/` | Correção urgente direto relacionada a produção |
| `chore/` | Configuração, dependências, manutenção |
| `docs/` | Documentação |
| `refactor/` | Refatoração sem mudança de comportamento |
| `perf/` | Melhoria de performance |
| `test/` | Adição ou correção de testes |

Exemplo: `feat/cadastro-pirometro`, `docs/levantamento-codigos-pir01`.

## Convenção de commits

Commits seguem o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<escopo opcional>): <descrição curta>
```

Exemplos:
- `docs: adiciona levantamento de codigos do PIR-01`
- `feat(pirometros): cadastro de tabela de codigos por pirometro`
- `fix(leituras): corrige validacao de faixa de temperatura`

## Fluxo de Pull Request

1. Criar branch a partir de `develop` com o prefixo adequado.
2. Abrir PR contra `develop` (nunca direto contra `main`).
3. CI precisa passar (quando houver pipeline de build/test).
4. Pelo menos 1 aprovação antes do merge.
5. `main` só recebe `develop` quando uma versão for de fato liberada
   (release), seguindo o mesmo padrão de tag `vX.Y.Z` usado no RGM.

## Proteção de branch (a configurar no GitHub quando houver CI)

- `main`: exige PR + aprovação, sem push direto, sem force-push.
- `develop`: exige PR + aprovação, sem push direto, sem force-push.

Ver `.github/PULL_REQUEST_TEMPLATE.md` para o checklist usado em cada PR.
