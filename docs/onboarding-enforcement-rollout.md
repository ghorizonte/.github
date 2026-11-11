# Protecao preventiva de onboarding de repositorios (proposta de implantacao)

**Status: nao ativado.** Este repositorio disponibiliza um workflow de validacao
somente-leitura. Nenhuma regra organizacional foi criada ou modificada nesta PR.
A ativacao exige uma revisao separada do ruleset e um ensaio controlado.

## Incidente que motivou a mudanca

Em 10/11/2026, a primeira PR de ghorizonte/robo criou
.github/CODEOWNERS. Como o arquivo ainda nao existia na base main,
uma aprovacao de outro colaborador foi suficiente para integrar a PR
apesar de a politica corporativa reservar a mudanca para @edsoness-hub.
A reconciliacao posterior nao elimina essa janela.

## Duas protecoes diferentes, ambas necessarias

1. **Criacao autorizada.** Usar o provisionador corporativo
   gh-automation/.github/workflows/create-corporate-repository.yml para
   criar o repositorio ja com baseline. Avaliar a Repository Policy do
   Enterprise para restringir a criacao aos atores corporativos
   autorizados. A configuracao simples de Member privileges tambem
   restringe GitHub Apps e **pode quebrar o provisionador**; nao a
   desligar sem confirmar uma excecao funcional para GH_PROVISIONER.
   Proprietarios da organizacao continuam podendo criar repositorios,
   portanto a conformidade de suas criacoes tambem precisa ser auditada.

2. **Protecao independente de CODEOWNERS.** No ruleset organizacional
   "GH - Protecao Branch Principal", configurar Required reviewers para
   a equipe corporativa de aprovadores de governanca, exigindo uma
   aprovacao quando a PR alterar:
   - .github/CODEOWNERS, CODEOWNERS, docs/CODEOWNERS;
   - .github/workflows/** e .github/risk-policy*.json;
   - AGENTS.md, CLAUDE.md, DEVIN.md, AI-DEVELOPMENT-GOVERNANCE.md;
   - infra/**, deploy/**, deployment/**, terraform/**;
   - outras regras CRITICAL aprovadas na matriz corporativa.

   Esse recurso do GitHub Enterprise requer **uma equipe**, nao um
   usuario individual. Antes de ativar, criar ou validar uma equipe
   de governanca com apenas os aprovadores autorizados, contendo
   @edsoness-hub, e garantir permissao write/maintain/admin em cada
   repositorio abrangido. **Nao usar admins ou tech-leads sem verificar
   seus integrantes.** Os Required reviewers nao dependem de existir
   CODEOWNERS na branch base e fecham a lacuna da primeira PR.

## Workflow organizacional de conformidade (esta proposta)

Origem publica: ghorizonte/.github/.github/workflows/corporate-onboarding-gate.yml

- Executa apenas leitura em pull_request e merge_group; nao faz checkout
  nem executa codigo do repositorio alvo.
- Valida o **SHA do merge candidato**, nao apenas a branch base.
- Exige .github/CODEOWNERS com o bloco final corporativo, owners de
  arquivos criticos e equipe risk-reviewers nos repositorios operacionais.
- Repositorios administradores (.github, gh-automation e
  repo-template-corporativo) mantem seu modelo separado de CODEOWNERS.
- Falha fechada diante de arquivo ausente, API indisponivel, politica
  alterada, token invalido ou ref inexistente.
- O workflow NAO comprova sozinho todas as obrigacoes do onboarding:
  nao substitui controle de criacao, revisor especifico, matriz de
  times, ambientes, CI funcional ou Merge Queue.
- Nao usa tokens privilegiados, secrets corporativos nem dependencias
  de codigo nao revisado do alvo.

## Rollout seguro em etapas

A. Integrar esta PR na ghorizonte/.github mediante aprovacao humana.
   Confirmar que os testes isolados passaram. Nao ativar regras nesse momento.

B. Inventariar em todos os repositorios operacionais CODEOWNERS e
   readiness, excluindo formalmente templates/arquivados/vazios.
   A integracao de CODEOWNERS via PR em repositorios existentes
   continua respeitando revisao humana; nao fazer push direto na main.

C. Criar e auditar a equipe especifica de aprovadores. Ensaiar no
   ruleset de um repositorio piloto (sem bypass) a alteracao inicial
   de CODEOWNERS e exigir a aprovacao da equipe. Preservar os campos
   atuais do ruleset ao atualiza-lo.

D. Propor a configuracao do workflow requerido pela organizacao em
   modo Evaluate; fonte publica da ghorizonte/.github, branch main,
   arquivo corporate-onboarding-gate.yml, branch destino padrao.
   Verificar eventos pull_request e merge_group e nao adicionar
   cancel-in-progress. Investigar novos repositorios sem bootstrap
   e casos de isolamento/forks antes de alterar para Active.

E. Confirmar que o provisionador consegue **criar um repositorio de
   teste vazio e inicializar a main** sob a regra proposta; o GitHub
   documenta que required workflows podem exigir bypass durante a
   criacao de repositorios. Nao conceder bypass geral a equipes
   humanas nem permitir bypass de PRs normais.

F. Ativar Required reviewers e o workflow requerido
   progressivamente por escopo; so ampliar apos testar um PR
   conforme, um PR nao conforme, o caso de CODEOWNERS inaugural,
   Merge Queue/merge_group e rollback documentado.

## Evidencias minimas para homologacao

- PR inaugural com CODEOWNERS correto e aprovacao de usuario
  nao autorizado permanece bloqueada.
- Apos aprovacao por membro da equipe aprovada, o caso de
  bootstrap pode integrar sem relaxar required status checks.
- PR sem CODEOWNERS, com footer removido ou com dono corporativo
  trocado e bloqueada pelo workflow requerido.
- O gate roda sobre merge_group na fila.
- Criador corporativo permanece operacional.
- Nao ha mudanca inadvertida nos 19 checks da aplicacao Cloone,
  nos checks verificar por repositorio, ou na classificacao de risco.

## Referencias

- https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/governing-how-people-use-repositories-in-your-organization
- https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/restricting-repository-creation-in-your-organization
- https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization
