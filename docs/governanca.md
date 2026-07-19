# 🛡️ Governança do Projeto — Forno Fundição

Este documento estabelece as diretrizes de governança obrigatórias para o projeto **Forno Fundição**. O cumprimento destas políticas é exigido de todos os colaboradores humanos e agentes autônomos (IAs) para garantir a integridade do negócio, segurança industrial e qualidade do software.

---

## 👥 1. Políticas para Pessoas (Humanos e Gestores da Rei Auto Parts)

*   **Aprovação de Escopo (PO-First)**:
    *   Toda alteração de funcionalidade, modelo de dados ou fluxo operacional exige aprovação explícita dos Product Owners (Otávio/Gemini PO).
    *   Desenvolvedores não devem expandir o escopo do código com base em suposições (ex: tentar integrar CLP ou espectrômetro antes da Fase 2).
*   **Decisão de Campo (Operação)**:
    *   Os operadores no forno são a autoridade máxima sobre a leitura física. Se a temperatura estiver fora da faixa esperada, o sistema gera um **alerta visual**, mas **nunca bloqueia** o salvamento do registro.
*   **Rede e TI da Fábrica**:
    *   Nenhuma conexão física ou lógica ad-hoc (ex: pontes de rede locais, roteadores Wi-Fi provisórios) pode ser feita para conectar espectrômetros ou CLPs à rede corporativa sem aprovação formal e presencial da equipe de Segurança de TI.
*   **Gestão de Processos e Operações (Exclusivo para Gestores)**:
    *   **Rastreabilidade de Corridas e Lotes**: O sistema deve permitir a associação de leituras de pirômetros a uma "Corrida" (identificador de lote de fusão) e "Lote" (lote de produção), mesmo que o preenchimento inicial na fábrica seja feito manualmente.
    *   **Identificação de Panelas (Ladles)**: Embora não haja identificador oficial de panelas hoje, o sistema deve prever um campo de identificação de panelas (potencialmente opcional na fase 1) para permitir rastreabilidade futura.
    *   **Campanha do Forno e Desgaste de Cadinhos**: O desgaste dos cadinhos deve ser controlado para prever a campanha do forno. Inicialmente, eventos de desgaste ou troca de cadinhos serão registrados e acompanhados via **Issues no GitHub** (gestão de ciclo de vida do ativo), e posteriormente integrados ao banco de dados.
    *   **Mapeamento de Fluxos**: O fluxo de apontamento (hoje baseado em planilhas e papel) será mapeado gradualmente. As telas e formulários do sistema devem ser flexíveis para se adaptar ao processo real conforme o mapeamento avança.

---

## 🤖 2. Políticas para Agentes (IAs)

*   **Não Inventar Dependências**:
    *   Use estritamente o ambiente configurado no `.devcontainer` e no `docker-compose.yml`. É expressamente proibido instalar pacotes adicionais no host ou criar ambientes virtuais (`venv`) fora do container padrão.
*   **Ciclo de Validação Obrigatório**:
    *   Antes de propor qualquer Pull Request, o agente deve rodar obrigatoriamente a validação local completa:
        ```bash
        make validate  # roda build + format + lint + test-coverage (min 90%)
        ```
*   **Sem Acesso Direto a Dados (Clean Arch)**:
    *   Agentes nunca devem acessar a sessão do banco de dados (`SQLModel Session`) diretamente da camada de Controller/API. Todo acesso a dados deve obrigatoriamente passar por um Caso de Uso (`UseCase`) e uma Interface de Repositório (`Repository Port`).

---

## 💾 3. Governança de Dados e Schema (Banco de Dados)

*   **Sem Alterações Manuais (Zero Manual DDL)**:
    *   Toda alteração no schema do banco de dados (tabelas, colunas, índices) deve ser realizada via arquivo de migração gerado pelo Alembic (`app/migrations/versions/`).
    *   Nenhum script SQL manual deve ser executado diretamente no banco de produção.
*   **Imutabilidade de Leituras**:
    *   Registros de medição de temperatura (`Leitura`) são dados de auditoria industrial e **nunca devem ser editados ou deletados** (sem operações de UPDATE ou DELETE na tabela `leitura` via API). Correções de leituras erradas devem ser feitas registrando uma nova medição com observação justificando o erro.
*   **Desacoplamento de Equipamentos**:
    *   A lista de pirômetros não é uma constante de código. Qualquer inclusão, alteração ou exclusão de pirômetros e seus limites térmicos deve ser tratada como **dados de configuração no banco** (tabelas `pirometro` e `codigo_pirometro`), nunca como código.

---

## 🔒 4. Segurança e Segregação de Escopo

*   **Faseamento Rígido (Foco no MVP)**:
    *   O escopo atual limita-se exclusivamente a **apontamentos manuais de temperatura de pirômetros**.
    *   Implementações sobre espectrômetros ([docs/03-espectrometros.md](docs/03-espectrometros.md)) e comunicação com CLPs estão fora de cogitação e seu código correspondente não deve ser iniciado.
*   **Proteção de Credenciais**:
    *   Arquivos `.env` contendo credenciais ou chaves nunca devem ser comitados. Use sempre o [.env.example](.env.example) para documentar chaves de configuração vazias.

---

## 🧪 5. Arquitetura e Governança de Testes

*   **Segregação por Camadas**:
    *   Nenhum arquivo de teste deve ser criado no diretório raiz do aplicativo (`app/`).
    *   Todos os testes devem residir na pasta `app/tests/` e refletir exatamente a arquitetura do projeto:
        *   `app/tests/core/domain/`: Testes unitários para entidades e enums de domínio.
        *   `app/tests/core/application/`: Testes unitários para casos de uso (`use_cases`).
        *   `app/tests/adapter/controllers/`: Testes para controladores e adaptadores de API.
        *   `app/tests/adapter/repositories/`: Testes de integração/unitários para os repositórios concretos.
        *   `app/tests/infra/`: Testes para infraestrutura (banco, container DI, logs, etc.).
        *   `app/tests/api/`: Testes de integração de alto nível para os endpoints e bootstrappers da API.
*   **Padrões de Nomenclatura**:
    *   Todos os arquivos de testes devem seguir a nomenclatura `test_*.py`.
*   **Nível Mínimo de Cobertura**:
    *   A cobertura de testes deve ser mantida em, no mínimo, **90%**.
    *   O comando `make validate` (ou `make test-coverage`) deve ser executado para atestar esse percentual antes de qualquer Pull Request.
