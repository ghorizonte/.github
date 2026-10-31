# Governanca Corporativa de Agentes de IA para Desenvolvimento

Versao: 1.2
Status: Padrao corporativo
Escopo oficial: Codex, Claude e Devin

## Objetivo

Estabelecer regras obrigatorias para uso de agentes de IA em desenvolvimento de software no Grupo Horizonte, preservando segregacao de funcoes, seguranca, rastreabilidade, controle de mudancas e autonomia proporcional ao risco.

## Principios

1. IA pode produzir codigo, analisar, testar, documentar e preparar mudancas.
2. A autonomia de aprovacao deve ser proporcional ao risco da mudanca.
3. Durante o shadow mode, toda aprovacao continua humana, inclusive para PRs classificados como LOW.
4. Autonomia futura para LOW somente pode ser habilitada apos homologacao explicita da politica corporativa.
5. MEDIUM, HIGH e CRITICAL permanecem sujeitos a aprovacao humana.
6. A identidade que executa trabalho tecnico deve ser separada, sempre que tecnicamente possivel, da identidade humana que revisa e aprova.
7. Ferramenta aprovada nao implica acesso irrestrito a repositorios, dados, ambientes, secrets ou configuracoes.
8. Toda automacao deve operar com menor privilegio e dentro do escopo explicitamente autorizado.
9. Enquanto o controle temporario de autoridade estiver vigente, somente `@edsoness-hub` pode autorizar a adocao de mudancas na politica corporativa de governanca ou em seus mecanismos executaveis.

## Classificacao corporativa de risco

Todo Pull Request deve ser classificavel em um dos seguintes niveis:

- LOW: mudancas exclusivamente documentais ou de impacto comprovadamente baixo.
- MEDIUM: mudancas funcionais localizadas, testes ou alteracoes que exigem revisao contextual.
- HIGH: autenticacao, autorizacao, seguranca, banco, migrations, schema, financeiro ou grande volume de mudanca.
- CRITICAL: CI/CD, workflows, CODEOWNERS, governanca, infraestrutura, deployment, secrets ou controles de acesso privilegiado.

Regras obrigatorias:

- regras deterministicas estabelecem o risco minimo;
- uma IA pode elevar o risco, mas nunca reduzir o piso definido pelas regras;
- na duvida, o risco sobe;
- classificacao de risco nao autoriza um agente a aprovar o proprio trabalho;
- alteracoes de rulesets, CODEOWNERS, permissoes, bypasses, secrets ou controles de seguranca exigem autorizacao explicita;
- enquanto o controle temporario de autoridade estiver vigente, mudancas em `AI-DEVELOPMENT-GOVERNANCE.md`, `AGENTS.md`, `CLAUDE.md`, `DEVIN.md`, `.github/CODEOWNERS`, politicas de risco e mecanismos centrais de governanca somente podem ser adotadas com aprovacao de `@edsoness-hub`; outros humanos e agentes podem propor e revisar tecnicamente essas mudancas, mas nao substituem essa autorizacao;
- durante o shadow mode, o classificador e informativo e nao altera os requisitos existentes de merge.

A politica executavel de cada repositorio fica em `.github/risk-policy.json`. Repositorios podem adicionar regras mais restritivas, mas nao reduzir o baseline corporativo sem excecao formal.

## Regras obrigatorias para agentes

Antes de alterar qualquer arquivo, o agente deve ler as instrucoes do repositorio aplicaveis ao seu contexto.

### Git e branches

- Trabalhar exclusivamente em branch de tarefa.
- Nao fazer push direto em `main`, `master` ou `develop` quando essas branches forem protegidas.
- Nao fazer force-push, rebase destrutivo, amend ou reescrita de historico em branch alheia.
- Nao excluir branch remota de outra pessoa ou de PR aberto.
- Manter o escopo da branch limitado a tarefa solicitada.

### Pull Requests

- Nao abrir Pull Request usando a identidade humana conectada quando o fluxo corporativo por bot estiver disponivel.
- Ao concluir a tarefa, solicitar a criacao do PR pelo workflow corporativo no repositorio `ghorizonte/gh-automation`, usando a identidade `ghorizonte-automation[bot]`.
- Caso o agente nao consiga acionar o workflow corporativo, deve deixar a branch pronta, informar o nome da branch e parar antes de abrir o PR com identidade humana.
- Nao fazer merge.
- Nao aprovar o proprio trabalho.
- Nao habilitar auto-merge por conta propria.
- Informar claramente no PR os testes executados, cenarios nao testados, classificacao de risco quando disponivel e riscos residuais.

### CI, testes e qualidade

- Executar os checks aplicaveis antes de considerar a tarefa concluida.
- Nao desabilitar, remover, ignorar ou colocar testes em quarentena apenas para obter CI verde.
- Nao reduzir baseline ou criterio de qualidade sem justificativa explicita e autorizacao quando exigida.
- Nao classificar uma falha como intermitente sem evidencia tecnica.
- Quando nao for possivel validar algo, declarar explicitamente a limitacao.

### Seguranca e governanca

Sem autorizacao explicita, o agente nao pode:

- alterar rulesets, branch protection, CODEOWNERS ou requisitos de aprovacao;
- alterar times, membros, papeis ou permissoes de repositorio/organizacao;
- criar, revelar, copiar ou modificar secrets, tokens, chaves privadas ou credenciais;
- conceder bypass de protecoes;
- alterar configuracoes de seguranca ou acesso privilegiado;
- executar mudancas irreversiveis em producao.

Secrets nunca devem ser inseridos em prompts, codigo, commits, logs ou arquivos versionados.

### Ambientes e producao

- Respeitar a segregacao DEV / HML / PROD definida pelo repositorio.
- Nao usar credenciais produtivas em DEV ou HML.
- Nao publicar diretamente em PROD fora do fluxo corporativo.
- Nao transformar um experimento em uso produtivo sem homologacao e aprovacao aplicaveis.

## Ferramentas no escopo oficial

### Codex

O arquivo raiz `AGENTS.md` e a instrucao operacional primaria do repositorio para Codex.

### Claude

O arquivo raiz `CLAUDE.md` deve importar ou reproduzir as regras do `AGENTS.md`, evitando divergencia entre agentes.

### Devin

Devin integra o escopo oficial corporativo e deve obedecer as mesmas regras do `AGENTS.md`. Conhecimentos, playbooks ou configuracoes especificas do Devin podem adicionar contexto do projeto, mas nao podem reduzir ou contradizer estas regras corporativas.

## Hierarquia

As regras deste padrao representam requisitos corporativos minimos. Instrucoes mais restritivas do repositorio, do sistema, de seguranca ou de um fluxo aprovado podem complementar estas regras. Instrucoes locais nao podem reduzir controles corporativos sem excecao formal aprovada.

## Fonte e sincronizacao

A fonte controlada desta politica e o repositorio privado `ghorizonte/repo-template-corporativo`.

Repositorios corporativos devem manter, no minimo:

- `AGENTS.md`
- `CLAUDE.md`
- `DEVIN.md`
- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `.github/workflows/risk-classifier.yml`
- `.github/risk-policy.json`
- `docs/governanca-risco-pr.md`

O `ghorizonte/gh-automation` deve ser usado para verificar e sincronizar esses arquivos durante onboarding e regularizacao.

## Shadow mode

Enquanto o modo corporativo estiver configurado como `shadow`:

1. o classificador registra LOW, MEDIUM, HIGH ou CRITICAL;
2. o resultado serve para aprendizado e auditoria;
3. nenhuma classificacao dispensa aprovacao humana;
4. o classificador nao deve habilitar merge, auto-merge ou bypass;
5. resultados devem ser usados para calibrar falsos LOW, falsos HIGH e regras especificas por tecnologia/dominio.

## Regra de encerramento da tarefa

Uma tarefa executada por agente so e considerada pronta para revisao quando:

1. o escopo solicitado estiver concluido;
2. os checks aplicaveis tiverem sido executados;
3. cenarios nao testados e riscos residuais estiverem declarados;
4. a branch estiver publicada;
5. o PR for solicitado pelo fluxo corporativo de bot, ou o agente informar que nao conseguiu aciona-lo.

Durante o shadow mode, a IA prepara e revisa a mudanca; a aprovacao final continua humana.
