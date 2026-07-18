# Git Flow

Fluxo baseado em Git Flow, no mesmo padrão usado nos projetos RGM e Area Verde
(referências: `rgm-backend`, `area-verde`), com integração contínua em
`develop` e estabilidade em `main`.

## Branches

- `main`: código estável, pronto para produção. Só recebe merge de `release/*`
  ou `hotfix/*`.
- `develop`: branch principal de integração. Todo trabalho novo nasce dela e
  volta pra ela via PR.
- `feature/*` / `feat/*`: novas funcionalidades.
- `fix/*` / `bugfix/*`: correções normais.
- `release/*`: preparação de versões.
- `hotfix/*`: correções urgentes, saem direto de `main`.
- `docs/*`, `chore/*`, `refactor/*`, `perf/*`, `test/*`: mesma convenção do RGM,
  usada também para o auto-label de PR (ver `.github/workflows/pr-automation.yml`).

## Funcionalidades e correções normais

Toda `feature/*`, `feat/*`, `fix/*` ou `bugfix/*` sai de `develop`:

```bash
git checkout develop
git pull origin develop
git checkout -b feat/cadastro-pirometro
```

Ao finalizar, abrir Pull Request para `develop`.

## Releases

Toda versão de entrega sai de `develop`:

```bash
git checkout develop
git pull origin develop
git checkout -b release/v0.1.0
```

Durante a release:

- corrigir bugs finais;
- atualizar documentação;
- revisar migrations (quando houver banco de dados);
- garantir que o CI passa;
- abrir PR de `release/v0.1.0` para `main`;
- abrir PR de `release/v0.1.0` para `develop`, se houve ajustes na release.

Após merge em `main`:

```bash
git checkout main
git pull origin main
git tag v0.1.0
git push origin v0.1.0
```

## Hotfixes

Hotfix sai de `main`:

```bash
git checkout main
git pull origin main
git checkout -b hotfix/corrigir-validacao-temperatura
```

Depois:

1. Corrigir o problema.
2. Abrir PR para `main`.
3. Após merge, gerar nova tag patch (ex.: `v0.1.1`).
4. Abrir PR para `develop` trazendo a correção de volta.

## Versionamento

Versionamento semântico `MAJOR.MINOR.PATCH`:

- `PATCH`: correções.
- `MINOR`: novas funcionalidades compatíveis.
- `MAJOR`: mudanças incompatíveis ou grandes quebras.

Primeira versão planejada: `v0.1.0`.

## Conventional Commits

```bash
feat: adiciona cadastro de pirometro
fix: corrige validacao de faixa de temperatura
docs: adiciona documentacao do fluxo git
test: adiciona testes do endpoint de leitura
refactor: reorganiza camada de aplicacao
chore: configura pipeline de CI
ci: adiciona workflow do GitHub Actions
```

## Pull Requests

- PRs de `feature/*`, `feat/*`, `fix/*`, `bugfix/*` vão para `develop`.
- PRs para `main` só vêm de `release/*` ou `hotfix/*` (validado automaticamente
  no CI, ver `.github/workflows/ci.yml`).
- **Toda PR que resolve uma Issue deve referenciar `Closes #<numero>` no corpo**
  (já presente no template) — isso fecha a issue automaticamente quando a PR
  é mergeada. Ver [automacao-ci.md](automacao-ci.md) para o fluxo completo de
  issue → PR → fechamento automático.

## Aprovação: fácil para `develop`, controlada para `main`

O objetivo é não travar o dia a dia: qualquer `feature/fix` para `develop` só
precisa do **CI verde** para poder ser mergeada — sem exigir aprovação manual
de outra pessoa (`required_approving_review_count: 0`). Com "Allow auto-merge"
habilitado no repositório, basta marcar a PR como auto-merge que ela mergeia
sozinha assim que o CI passar.

Já `main` segue um caminho mais controlado, no formato:

```
release/vX.Y.Z ou hotfix/*  →  tag  →  merge em main  →  CI valida
```

Ou seja: a branch de release/hotfix é testada, recebe a tag semântica, e só
então vai para `main` — o CI roda de novo em `main` como validação final
(gate de produção), mas sem exigir review humano extra, já que quem decide
"isso é uma release" é o próprio ato de abrir a PR de `release/*`/`hotfix/*`.

## Proteção de branches no GitHub

### `main`

- bloquear push direto;
- exigir Pull Request;
- exigir status checks do CI (`Build, test and validate`);
- impedir force push;
- impedir deleção da branch;
- regra operacional (também validada no CI, ver "Validate PR source for main"
  em `.github/workflows/ci.yml`): só aceita merge vindo de `release/*` ou
  `hotfix/*`.

### `develop`

- evitar push direto;
- exigir Pull Request;
- exigir CI passando (`Build, test and validate`);
- impedir force push;
- impedir deleção da branch;
- **sem exigência de aprovação humana** — o CI é o gate. Auto-merge habilitado
  no repositório para não travar o fluxo.

Essas regras já estão configuradas no repositório via branch protection do
GitHub (`main` e `develop`).
