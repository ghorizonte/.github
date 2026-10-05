# Horizonte AI Development Governance

Version: 1.0
Status: Corporate standard
Scope: software development and repository operations performed with approved AI agents, including ChatGPT/Codex, Claude and Devin.

## Principles

1. AI agents are execution assistants, not approval authorities.
2. Human accountability is preserved for review, approval and production-impacting decisions.
3. Least privilege applies to users, apps, tokens, repositories and environments.
4. Repository and branch protections take precedence over agent instructions.
5. AI must not bypass controls to make a change appear successful.

## Mandatory operating rules

- Work only in a task branch.
- Do not push directly to `main`, `master` or another protected branch.
- Do not merge a pull request.
- Do not approve the agent's own work.
- Do not weaken, disable, quarantine or bypass tests, checks, rulesets, CODEOWNERS, branch protection or security controls merely to obtain a green result.
- Do not alter organization/repository permissions, rulesets, secrets, credentials or security settings unless the task explicitly authorizes that specific change.
- Never place passwords, tokens, private keys, certificates, connection strings or production credentials in prompts, files, commits, logs or PR descriptions.
- Run the applicable tests/checks and report what was and was not validated.
- Report residual risks and untested scenarios honestly.
- Do not rewrite another contributor's published history without explicit authorization.
- Do not use force-push on shared branches.

## Pull request identity

When a task is ready for review:

- Do not open the PR with the connected human identity when the corporate bot flow is available.
- Request PR creation through the corporate workflow in `ghorizonte/gh-automation`.
- The expected PR author is `ghorizonte-automation[bot]`.
- The bot must not merge or approve the PR.
- A human reviewer with the appropriate repository role must review and approve the change.
- If the agent cannot trigger the corporate PR workflow, leave the branch ready and explicitly report that the PR must be created through the corporate bot flow. Do not silently fall back to a human-authored PR.

## Approved AI agents in current scope

- ChatGPT / Codex
- Claude
- Devin

Approval of an AI tool does not grant unrestricted access to repositories, data, systems or environments. Each tool remains limited by the connected identity, app installation, repository scope, secrets policy and GitHub protections.

## Required repository controls

Repositories onboarded to the corporate standard should, as applicable, include:

- protected production branch;
- pull request requirement;
- at least one human approval;
- CODEOWNERS review;
- stale approval dismissal;
- review-thread resolution;
- no force-push;
- no protected-branch deletion;
- required CI checks where available;
- PR template;
- agent instruction files aligned with this policy.

## Legacy / ratchet rule

Legacy debt may be baselined when immediate full remediation is impractical. The baseline does not authorize new debt. New violations above the registered baseline should fail the applicable gate unless a documented, reviewed exception is approved.

## Enforcement

Critical controls must not rely solely on an AI agent reading this document. They should also be enforced by GitHub rulesets, branch protection, required checks, CODEOWNERS, scoped app permissions and corporate workflows.

