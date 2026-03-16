# OpSec Guide — GitLab & GitHub CI/CD
### Credentials, Multi-SIEM Targets, and Pipeline Security

---

## Table of Contents

1. [How Credentials Work in CI/CD](#1-how-credentials-work-in-cicd)
2. [GitLab — Setting CI/CD Variables](#2-gitlab--setting-cicd-variables)
3. [GitLab — Pipeline Stages](#3-gitlab--pipeline-stages)
4. [GitHub — Setting Secrets](#4-github--setting-secrets)
5. [GitHub — Workflow Stages](#5-github--workflow-stages)
6. [Multi-SIEM Targets](#6-multi-siem-targets)
7. [Protecting Branches](#7-protecting-branches)
8. [Token Rotation Policy](#8-token-rotation-policy)
9. [Security Checklist](#9-security-checklist)

---

## 1. How Credentials Work in CI/CD

`settings.py` is listed in `.gitignore` — it will **never exist on a CI/CD runner**.
The runner has no `.env` file either. All credentials come exclusively from
CI/CD variables injected at runtime.

`config.py` handles this automatically when `AUTH_MODE=env` is set:

```
GitLab / GitHub variable store (encrypted at rest)
  SPLUNK_HOST  = myorg.splunkcloud.com
  SPLUNK_TOKEN = eyJr...
         │
         │  Injected as environment variables at job start
         ▼
Runner executes: python main.py --rules rules.csv --time 2h
  config.py reads os.getenv("SPLUNK_HOST") — finds the injected value
  settings.py is never read (does not exist on runner)
```

The pipeline sets `AUTH_MODE: env` in the `default:` block so this is
automatic for every job.

---

## 2. GitLab — Setting CI/CD Variables

**Settings → CI/CD → Variables → Add variable**

### Single SIEM target

| Key | Value | Options |
|-----|-------|---------|
| `SPLUNK_HOST` | `myorg.splunkcloud.com` | Masked ✓  Protected ✓ |
| `SPLUNK_TOKEN` | `eyJr...` | Masked ✓  Protected ✓ |

### Multiple SIEM targets

Add one set per environment. The pipeline uses `SIEM_TARGET` to select
which pair to use — no code changes required.

| Key | Value | Options |
|-----|-------|---------|
| `SPLUNK_HOST_PROD` | `prod.splunkcloud.com` | Masked ✓  Protected ✓ |
| `SPLUNK_TOKEN_PROD` | `eyJr... (prod)` | Masked ✓  Protected ✓ |
| `SPLUNK_HOST_STAGING` | `staging.splunkcloud.com` | Masked ✓  Protected ✓ |
| `SPLUNK_TOKEN_STAGING` | `eyJr... (staging)` | Masked ✓  Protected ✓ |
| `SPLUNK_HOST_LAB` | `lab.splunkcloud.com` | Masked ✓  Protected ✓ |
| `SPLUNK_TOKEN_LAB` | `eyJr... (lab)` | Masked ✓  Protected ✓ |

### Optional variables

| Key | Default | Purpose |
|-----|---------|---------|
| `SPLUNK_VERIFY_SSL` | `true` | Set `false` for lab/self-signed certs |
| `SPLUNK_JOB_MAX_WAIT` | `120` | Seconds to wait for search completion |
| `TIME_RANGE` | `30m` | Default time window for all searches |
| `RULES_FILE` | `rules.csv` | Path to the rules file in the repo |

**Masked** — value never appears in job logs even if accidentally printed.
**Protected** — variable only available to jobs on protected branches/tags.

---

## 3. GitLab — Pipeline Stages

The pipeline file `.gitlab-ci.yml` is at the project root. It defines two stages:

### Stage 1: `validate` — runs on every push

```
validate_rules
```
- Reads the rules file and runs `--dry-run --validate-schema`
- No Splunk connection needed — purely local analysis
- Fails the pipeline if any rule has a forbidden command or broken syntax
- Runs on every branch, every push, every merge request

### Stage 2: `search` — runs on protected branches only

Four jobs, each targeting a different SIEM environment:

| Job | Trigger | SIEM_TARGET |
|-----|---------|-------------|
| `search_default` | Auto on `main`/`master` | *(uses SPLUNK_HOST directly)* |
| `search_prod` | Manual on `main`, auto on tags | `prod` |
| `search_staging` | Manual on `main`, auto on `staging/*` | `staging` |
| `search_lab` | Manual on `main`, auto on `lab/*` | `lab` |

Results are saved as pipeline artifacts (downloadable from the GitLab UI)
and automatically expired after 7–30 days depending on the environment.

---

## 4. GitHub — Setting Secrets

**Settings → Secrets and variables → Actions → New repository secret**

Same variable names as GitLab. Secrets are encrypted, never shown in logs,
and not accessible to pull requests from forks.

For organisation-wide secrets (shared across multiple repos):
**Organisation Settings → Secrets and variables → Actions**

---

## 5. GitHub — Workflow Stages

The workflow file `.github/workflows/splunk_search.yml` defines two jobs:

### Job 1: `validate` — runs on every push and pull request
- No credentials needed
- Runs `--dry-run --validate-schema` on the rules file
- Blocks merge if validation fails

### Job 2: `search` — runs after validate passes, on main/master only
- Requires `SPLUNK_HOST` and `SPLUNK_TOKEN` secrets
- Also accepts named target secrets (`SPLUNK_HOST_PROD`, etc.)
- Supports manual trigger via **Actions → Run workflow** with inputs:
  - `siem_target` — which environment to target
  - `time_range` — time window (e.g. `2h`, `7d`)
  - `rules_file` — path to the rules file
  - `dry_run` — validate only, do not submit

---

## 6. Multi-SIEM Targets

The `SIEM_TARGET` variable selects which credential pair to use.
`config.py` resolves it like this:

```
SIEM_TARGET=prod   →  reads SPLUNK_HOST_PROD  and SPLUNK_TOKEN_PROD
SIEM_TARGET=lab    →  reads SPLUNK_HOST_LAB   and SPLUNK_TOKEN_LAB
(not set)          →  reads SPLUNK_HOST       and SPLUNK_TOKEN
```

To run against a specific target manually from your terminal:

```bash
export SIEM_TARGET=staging
export SPLUNK_HOST_STAGING=staging.splunkcloud.com
export SPLUNK_TOKEN_STAGING=eyJr...
python main.py --rules rules.csv --time 2h
```

To run against a specific target in a GitLab pipeline job, add:

```yaml
variables:
  SIEM_TARGET: "staging"
```

to the job definition. The named credential variables
(`SPLUNK_HOST_STAGING`, `SPLUNK_TOKEN_STAGING`) must be set in the
GitLab CI/CD variable store.

---

## 7. Protecting Branches

### GitLab
Settings → Repository → Protected branches → Add

| Branch | Push | Merge |
|--------|------|-------|
| `main` | Maintainers only | Developers + Maintainers |
| `master` | Maintainers only | Developers + Maintainers |

### GitHub
Settings → Branches → Add rule → Branch name: `main`

Enable:
- Require a pull request before merging
- Require status checks to pass (select the `validate` job)

---

## 8. Token Rotation Policy

Rotate tokens every 90 days:

1. Generate a new token in Splunk Web: Settings → Tokens → New Token
2. Update the variable in GitLab/GitHub variable store
3. Update your local `settings.py` if used
4. Verify the pipeline runs cleanly with the new token
5. Revoke the old token in Splunk Web

Set a calendar reminder when you create the token.

---

## 9. Security Checklist

Before pushing to the repository:

- [ ] `git status` — `settings.py` and `.env` are NOT listed
- [ ] `.gitlab-ci.yml` contains no hardcoded credentials
- [ ] All `SPLUNK_TOKEN_*` variables are set as **Masked** in GitLab
- [ ] All `SPLUNK_TOKEN_*` variables are set as **Protected** in GitLab
- [ ] `main` branch is protected (requires PR/review before merge)
- [ ] Token expiry date is in your calendar
- [ ] `search_results/` is in `.gitignore` (results may contain sensitive data)
