#!/usr/bin/env python3
"""Read-only onboarding gate for an organization-required GitHub workflow.

Checks the candidate merge SHA, never checks out or executes target repository code.
This gate enforces corporate CODEOWNERS ownership only. Repository creation privileges,
human approval and application CI must be enforced by independent organization rules.
"""
import argparse
import base64
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ORG = "ghorizonte"
AUTHORITY = "@edsoness-hub"
MARKER_START = "# BEGIN GH GOVERNANCE OWNERS v2"
MARKER_END = "# END GH GOVERNANCE OWNERS v2"
GOVERNANCE_REPOS = frozenset({".github", "gh-automation", "repo-template-corporativo"})
REQUIRED = frozenset({
    "*secrets*",
    "/.github/CODEOWNERS",
    "/.github/workflows/*",
    "/.github/workflows/**",
    "/.github/risk-policy*.json",
    "/AGENTS.md",
    "/CLAUDE.md",
    "/DEVIN.md",
    "/CODEOWNERS",
    "/docs/CODEOWNERS",
    "/AI-DEVELOPMENT-GOVERNANCE.md",
    "/deploy/*",
    "/deployment/*",
    "/infra/*",
    "/terraform/*",
})


def check_owners(repo, contents):
    """Return policy errors; check the last, authoritative corporate footer."""
    if not re.fullmatch(r"ghorizonte/[A-Za-z0-9_.-]+", repo):
        return ["INVALID_REPOSITORY"]
    if not isinstance(contents, str) or not contents.strip():
        return ["CODEOWNERS_MISSING"]
    lines = [line.strip() for line in contents.replace("\r\n", "\n").splitlines()]
    operational = repo.split("/", 1)[1].lower() not in GOVERNANCE_REPOS

    if not operational:
        if "/.github/CODEOWNERS " + AUTHORITY not in lines:
            return ["GOVERNANCE_CODEOWNERS_AUTHORITY_MISSING"]
        return []

    errors = []
    if lines.count(MARKER_START) != 1 or lines.count(MARKER_END) != 1:
        return ["CORPORATE_FOOTER_MISSING_OR_AMBIGUOUS"]
    begin, end = lines.index(MARKER_START), lines.index(MARKER_END)
    if begin >= end or any(line and not line.startswith("#") for line in lines[end + 1:]):
        return ["CORPORATE_FOOTER_NOT_AUTHORITATIVE"]
    body = [line for line in lines[begin + 1:end] if line and not line.startswith("#")]
    effective = {}
    for line in body:
        fields = line.split("#", 1)[0].split()
        if not fields:
            continue
        if len(fields) != 2 or fields[1] != AUTHORITY:
            errors.append("UNEXPECTED_CORPORATE_OWNER_RULE")
            continue
        effective[fields[0]] = fields[1]
    for path in sorted(REQUIRED):
        if effective.get(path) != AUTHORITY:
            errors.append("MISSING_PROTECTED_PATH:" + path)
    if not any(line.startswith("* ") and "@ghorizonte/risk-reviewers" in line.split() for line in lines[:begin]):
        errors.append("OPERATIONAL_RISK_REVIEWER_MISSING")
    return errors


def fetch_codeowners(repository, sha, token):
    if not re.fullmatch(r"ghorizonte/[A-Za-z0-9_.-]+", repository):
        raise ValueError("INVALID_REPOSITORY")
    if not re.fullmatch("[0-9a-f]{40}", sha):
        raise ValueError("INVALID_COMMIT_SHA")
    if not token:
        raise ValueError("TOKEN_MISSING")
    path = quote(".github/CODEOWNERS", safe="/")
    url = f"https://api.github.com/repos/{repository}/contents/{path}?ref={sha}"
    request = Request(url, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "gh-corporate-onboarding-gate",
    })
    try:
        with urlopen(request, timeout=25) as response:
            data = json.load(response)
    except HTTPError as exc:
        if exc.code == 404:
            return ""
        raise RuntimeError("GITHUB_API_HTTP_" + str(exc.code)) from None
    except URLError:
        raise RuntimeError("GITHUB_API_UNAVAILABLE") from None
    if data.get("type") != "file" or data.get("encoding") != "base64" or data.get("size", 0) > 3000000:
        raise RuntimeError("UNSUPPORTED_CODEOWNERS_RESPONSE")
    try:
        return base64.b64decode(data["content"], validate=False).decode("utf-8")
    except (ValueError, KeyError, UnicodeError):
        raise RuntimeError("INVALID_CODEOWNERS_CONTENT") from None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--sha", required=True)
    args = parser.parse_args()
    try:
        content = fetch_codeowners(args.repository, args.sha, os.environ.get("GH_TOKEN", ""))
        errors = check_owners(args.repository, content)
    except (RuntimeError, ValueError) as exc:
        errors = [str(exc)]
    outcome = {
        "repository": args.repository,
        "sha": args.sha,
        "status": "PASS" if not errors else "BLOCK",
        "reasons": errors,
    }
    print(json.dumps(outcome, ensure_ascii=True, sort_keys=True))
    if errors:
        print("::error::Corporate onboarding gate failed: " + ", ".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
