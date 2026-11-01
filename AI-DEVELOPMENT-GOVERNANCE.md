# Governanca Corporativa de Agentes de IA para Desenvolvimento

Versao: 1.5
Status: Padrao corporativo
Escopo oficial: Codex, Claude e Devin

## Objetivo

Estabelecer regras obrigatorias para uso de agentes de IA em desenvolvimento de software no Grupo Horizonte, preservando segregacao de funcoes, seguranca, rastreabilidade, controle de mudancas e autonomia proporcional ao risco.

## Principios

1. IA pode produzir codigo, analisar, testar, documentar e preparar mudancas.
2. A autonomia de aprovacao e proporcional ao risco da mudanca.
3. No piloto corporativo, PRs LOW e MEDIUM podem receber autorizacao tecnica automatica nos repositorios operacionais elegiveis.
4. HIGH e CRITICAL permanecem sujeitos a aprovacao humana valida no head atual.
5. A autorizacao automatica deve ser emitida por identidade tecnica revisora separada da identidade produtora do PR.
6. Ferramenta aprovada nao implica acesso irrestrito a repositorios, dados, ambientes, secrets ou configuracoes.
7. Toda automacao deve operar com menor privilegio e dentro do escopo explicitamente autorizado.
8. Enquanto o controle temporario de autoridade estiver vigente, somente `@edsoness-hub` pode autorizar a adocao de mudancas na politica corporativa de governanca ou em seus mecanismos executaveis.

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
- LOW e MEDIUM podem receber autorizacao automatica apenas quando todos os requisitos do piloto forem atendidos;
- HIGH e CRITICAL nunca recebem autorizacao automatica;
- a autorizacao automatica nao substitui CI, required checks, protecoes de branch, resolucao de conversas, CODEOWNERS, rulesets ou merge train;
- repositorios de governanca corporativa permanecem fora da autoaprovacao.

A politica executavel de risco fica em `.github/risk-policy.json` / `.github/risk-policy-v2.json`, conforme o fluxo implantado. Repositorios podem adicionar regras mais restritivas, mas nao reduzir o baseline corporativo sem excecao formal.

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
- Informar testes executados, cenarios nao testados, classificacao de risco quando disponivel e riscos residuais.

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

## Ferramentas no escopo oficial

- Codex: `AGENTS.md` e a instrucao operacional primaria.
- Claude: `CLAUDE.md` deve carregar as mesmas regras do `AGENTS.md`.
- Devin: deve obedecer ao mesmo baseline; configuracoes especificas podem adicionar contexto, mas nunca reduzir controles.

## Fonte e sincronizacao

A fonte controlada desta politica e o repositorio privado `ghorizonte/repo-template-corporativo`.

Repositorios corporativos devem manter, no minimo:

- `AGENTS.md`
- `CLAUDE.md`
- `DEVIN.md`
- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- politica de risco aplicavel
- workflow classificador aplicavel
- documentacao de governanca de risco

O `ghorizonte/gh-automation` deve verificar e sincronizar esses artefatos durante onboarding e regularizacao.

## Pilot mode

Enquanto o modo corporativo estiver configurado como `pilot`:

1. o classificador registra LOW, MEDIUM, HIGH ou CRITICAL;
2. LOW e MEDIUM podem receber aprovacao automatica nos repositorios operacionais elegiveis, exceto os explicitamente excluidos pela policy;
3. HIGH e CRITICAL exigem aprovacao humana;
4. a identidade revisora automatica deve ser diferente do autor tecnico do PR;
5. a aprovacao automatica so vale para o `head_sha` classificado; novo push exige nova classificacao e nova aprovacao;
6. nenhum fluxo pode usar bypass para contornar required checks, CODEOWNERS, rulesets, protecoes de branch ou merge train;
7. repositorios de governanca e exclusoes explicitas permanecem fora da autoaprovacao.

## Matriz corporativa de acesso a repositorios

A matriz versionada em `.github/repository-access-policy.json` e a fonte controlada para permissoes padrao de times nos repositorios da organizacao `ghorizonte`.

Baseline:

- `admins`: Admin;
- `tech-leads`: Maintain;
- `developers`: Write;
- `risk-reviewers`: Write nos repositorios operacionais elegiveis.

Excecoes Zonte Labs:

- `zontelabs-tech-leads` substitui `tech-leads`, mantendo Maintain;
- `zontelabs-developers` substitui `developers`, mantendo Write.

O reconciliador `ghorizonte/gh-automation:.github/workflows/reconcile-repository-access.yml` roda periodicamente e por disparo manual. Ele:

- adiciona times baseline ausentes;
- corrige permissoes divergentes, inclusive reduzindo `tech-leads` de Admin para Maintain quando houver drift;
- remove apenas times genericos explicitamente substituidos por override;
- nao remove outros times ou colaboradores fora do baseline;
- remove `risk-reviewers` dos repositorios de governanca;
- ignora repositorios arquivados, forks e exclusoes declaradas na policy.

A GitHub App usada pelo reconciliador deve permanecer instalada em todos os repositorios da organizacao e possuir, no minimo, as permissoes solicitadas pelo workflow: Administration write, Members read e Contents read. Assim, repositorios novos, importados ou copiados para `ghorizonte` passam a convergir automaticamente ao baseline na proxima reconciliacao, desde que pertençam a organizacao e nao estejam excluidos pela policy.

## Regra de encerramento da tarefa

Uma tarefa executada por agente so e considerada pronta para revisao quando:

1. o escopo solicitado estiver concluido;
2. os checks aplicaveis tiverem sido executados;
3. cenarios nao testados e riscos residuais estiverem declarados;
4. a branch estiver publicada;
5. o PR for solicitado pelo fluxo corporativo de bot, ou o agente informar que nao conseguiu aciona-lo.

Durante o piloto, LOW e MEDIUM podem seguir pela autorizacao automatica definida na policy; HIGH e CRITICAL continuam dependentes de aprovacao humana.
