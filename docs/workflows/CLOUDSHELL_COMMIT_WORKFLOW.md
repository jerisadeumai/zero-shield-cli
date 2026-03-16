# CloudShell Commit Workflow

**Purpose:** Step-by-step guide for committing and pushing changes from AWS CloudShell to GitHub.

**Branch:** agent-v2-dev  
**Last Updated:** March 15, 2026

---

## Prerequisites

Before starting, ensure you have:
- AWS CloudShell session active
- Git configured with your credentials
- Repository cloned and up to date

---

## Single Commit Workflow

This workflow consolidates all AWS resource count synchronization changes into a single, well-documented commit.

### Step 1: Verify Current Status

```bash
# Check current branch
git branch

# Should show: * agent-v2-dev

# Check git status
git status

# Review what files have changed
```

### Step 2: Stage All Changes

```bash
# Stage modified files
git add zero_shield_cli.py
git add docs/user-guide/COMMANDS.md
git add validation/TEST_REPORTS.md
git add validation/reports/02-forensic-complete.md
git add validation/reports/04-line-by-line-audit.md
git add validation/reports/09-final-sync-audit.md
git add COMMIT_MESSAGE.md
git add CLOUDSHELL_COMMIT_WORKFLOW.md
git add GIT_PUSH_STRATEGY.md

# Verify staged files
git status
```

### Step 3: Create Commit

```bash
# Commit with comprehensive message
git commit -m "fix: synchronize AWS resource counts across all documentation (32 actions, 14 services)

Complete synchronization audit revealed and fixed AWS resource count discrepancies.

FIXES:
- Updated startup banner: 50+ tools → 32 AWS actions
- Updated COMMANDS.md footer: 33 AWS actions → 32 AWS actions  
- Updated validation reports: All 33 references → 32
- Enhanced _client() function: Made all 14 services explicit

ARCHITECTURAL IMPROVEMENTS:
- Replaced ambiguous else clause with explicit service listing
- Added ValueError for unsupported services (fail-fast pattern)
- Updated docstring to document all 14 AWS services clearly
- Improved audit compliance and maintainability

VERIFICATION:
- PowerShell count confirms: 32 tool functions
- Code analysis confirms: 14 AWS services
- Zero syntax errors
- 100% documentation synchronization achieved

FILES MODIFIED:
- zero_shield_cli.py (startup banner, _client function)
- docs/user-guide/COMMANDS.md (footer)
- validation/TEST_REPORTS.md (AWS counts)
- validation/reports/02-forensic-complete.md (AWS counts)
- validation/reports/04-line-by-line-audit.md (AWS counts)
- validation/reports/09-final-sync-audit.md (NEW - comprehensive audit)

SECURITY:
All security boundaries remain intact:
- 5-layer credential redaction
- Allowlist-based prompt injection prevention
- Enhanced HITL confirmations
- XOR encrypted state files
- Parameter validation

See validation/reports/09-final-sync-audit.md for complete audit report."
```

### Step 4: Verify Commit

```bash
# View commit details
git log -1

# View commit diff
git show HEAD

# Verify commit message
git log -1 --pretty=format:"%B"
```

### Step 5: Push to Remote

```bash
# Push to agent-v2-dev branch
git push origin agent-v2-dev

# If push is rejected (remote has changes):
git pull --rebase origin agent-v2-dev
git push origin agent-v2-dev
```

---

## Post-Push Verification

### Verify on GitHub

1. Navigate to: https://github.com/jerisadeumai/zero-shield-cli
2. Switch to `agent-v2-dev` branch
3. Verify commit appears in history
4. Check files were updated correctly

### Verify Locally

```bash
# Confirm push succeeded
git log origin/agent-v2-dev -1

# Verify local and remote are in sync
git status

# Should show: "Your branch is up to date with 'origin/agent-v2-dev'"
```

---

## Troubleshooting

### Issue: "Permission denied (publickey)"

```bash
# Configure Git credentials
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Use HTTPS instead of SSH
git remote set-url origin https://github.com/jerisadeumai/zero-shield-cli.git

# Push with credentials
git push origin agent-v2-dev
```

### Issue: "Updates were rejected"

```bash
# Remote has changes you don't have locally
git pull --rebase origin agent-v2-dev

# Resolve any conflicts if they occur
# Then push again
git push origin agent-v2-dev
```

### Issue: "Merge conflicts"

```bash
# View conflicted files
git status

# Edit conflicted files to resolve
# Look for conflict markers: <<<<<<<, =======, >>>>>>>

# After resolving, stage files
git add <conflicted-file>

# Continue rebase
git rebase --continue

# Push changes
git push origin agent-v2-dev
```

---

## Best Practices

### Commit Message Guidelines

- **Title:** Clear, concise description (50 chars max)
- **Body:** Detailed explanation of changes
- **Format:** Use conventional commits (fix:, feat:, docs:, etc.)
- **References:** Link to issues or PRs when applicable

### Before Committing

- [ ] Run syntax checks: `python3 -m py_compile zero_shield_cli.py`
- [ ] Verify no debug code remains
- [ ] Check all file paths are correct
- [ ] Ensure documentation is updated
- [ ] Review diff: `git diff`

### After Pushing

- [ ] Verify commit on GitHub
- [ ] Check CI/CD pipeline (if configured)
- [ ] Update project board or issues
- [ ] Notify team members if needed

---

## Quick Reference

```bash
# Complete workflow in one go
git add .
git commit -m "fix: your commit message here"
git push origin agent-v2-dev

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# View commit history
git log --oneline -10

# View specific file history
git log --follow -- path/to/file
```

---

## Additional Resources

- **Git Documentation:** https://git-scm.com/doc
- **Conventional Commits:** https://www.conventionalcommits.org/
- **GitHub Flow:** https://guides.github.com/introduction/flow/

---

**Principal Architect:** Jeri L3D | JeriSadeuM  
**Repository:** https://github.com/jerisadeumai/zero-shield-cli  
**Branch:** agent-v2-dev
