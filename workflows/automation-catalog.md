# Opt-in automation catalog
Technology-neutral by default. Adopting standards does not activate workflows. Consumer selects pinned reusable workflows via small local callers, owns triggers, permissions, secrets, branch protections and parameters. Compose multiple profiles as needed; no Minecraft dependencies for unrelated projects. No implicit secrets inheritance or write grants.

## Available for review
- lifecycle-audit.yml: read-only inventory, aged branch/PR signals, surviving merged refs, open head/base dependencies, exact same-base changed-path overlaps (including renames). Optional comma-separated permanent branches and protected donors; default branch automatically protected in report. Configurable branch budget. No checkout of consumer code or write methods. Advisory only; age uses commit/PR update proxies, not exact creation/ready dates. GitHub pagination and changed-files caps fail closed. Cross-base and semantic conflicts need manual review. Template at templates/workflows/lifecycle-audit.yml; replace SHA placeholder before installing. Do not use pull_request_target to run untrusted code.

## Not yet reusable
- Branch retirement: keep execution in TMM until repository-specific owner identity, durable donor policy, exact batch/digest, nonce/replay protection, lease deletion and verification can be safely generalized and tested. No shared deletion workflow yet.
- Source assembly, full runtime builds, publication, Minecraft QA dispatch and update smoke: local project contracts; no generic automation can grant authority. Language/engine CI, standards checks, security scanning and throughput reporting are future opt-in modules, not installed capabilities.

Provenance: TMM main scripts/branch_lifecycle.py blob 0467d10364fa53b1774fdb24b1b4c1c547436641 and .github/workflows/branch-lifecycle-report.yml blob 601f20c70c5d5f6531e128abacbfd8aaf99f5c33. Removed TMM-only manifest and retirement console dependencies. Original TMM unchanged.
