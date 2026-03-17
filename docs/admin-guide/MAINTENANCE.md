# Maintenance Guide

> ⚠️ **DEVELOPMENT BRANCH**  
> Version: v2.0.0-dev | Status: Development Only | Not Production Ready

**Last Updated:** March 17, 2026  
**Version:** v2.0.0-dev

## Overview

This guide covers routine maintenance procedures for Zero-Shield CLI, including session file cleanup, Knowledge Graph pruning, dependency updates, and version upgrades.

---

## Session File Cleanup

### When to Clean

- Session files exceed size thresholds (see MONITORING.md)
- Performance degradation observed
- After major incident response (fresh start)
- Monthly routine maintenance

### Cleanup Procedure

```bash
# 1. Backup current session files
mkdir -p backups/$(date +%Y%m%d)
cp session_state.json backups/$(date +%Y%m%d)/
cp session_kg.json backups/$(date +%Y%m%d)/

# 2. Review file sizes
du -h session_*.json

# 3. Delete session files
rm session_state.json session_kg.json

# 4. Restart Zero-Shield (creates fresh encrypted files)
python3 zero_shield_cli.py

# 5. Verify new files created
ls -lh session_*.json
```

### Automated Cleanup Script

```bash
#!/bin/bash
# cleanup_sessions.sh

BACKUP_DIR="backups/$(date +%Y%m%d)"
MAX_SIZE_KB=1024  # 1 MB threshold

# Check session_kg.json size
KG_SIZE=$(du -k session_kg.json | cut -f1)

if [ $KG_SIZE -gt $MAX_SIZE_KB ]; then
    echo "Knowledge Graph exceeds threshold ($KG_SIZE KB > $MAX_SIZE_KB KB)"
    
    # Backup
    mkdir -p $BACKUP_DIR
    cp session_state.json $BACKUP_DIR/
    cp session_kg.json $BACKUP_DIR/
    
    # Clean
    rm session_state.json session_kg.json
    
    echo "Session files cleaned. Backups in $BACKUP_DIR"
else
    echo "Session files within normal size ($KG_SIZE KB)"
fi
```

---

## Knowledge Graph Pruning

### Manual Pruning

```python
# prune_kg.py
import json
import os
from datetime import datetime, timedelta

# Load KG
with open('session_kg.json', 'r') as f:
    kg = json.load(f)

# Remove entries older than 30 days
cutoff = datetime.now() - timedelta(days=30)
pruned_kg = {
    k: v for k, v in kg.items()
    if datetime.fromisoformat(v.get('timestamp', '2000-01-01')) > cutoff
}

# Save pruned KG
with open('session_kg.json', 'w') as f:
    json.dump(pruned_kg, f)

print(f"Pruned {len(kg) - len(pruned_kg)} entries")
```

### Automated Pruning

```bash
# Add to crontab for monthly pruning
0 0 1 * * /path/to/prune_kg.py
```

---

## Dependency Updates

### Check for Updates

```bash
# List outdated packages
pip list --outdated

# Check specific dependencies
pip show openai boto3 python-dotenv httpx
```

### Update Procedure

**IMPORTANT:** Test in non-production environment first.

```bash
# 1. Backup current environment
pip freeze > requirements.backup.txt

# 2. Update dependencies
pip install --upgrade openai boto3 python-dotenv httpx

# 3. Test Zero-Shield
python3 zero_shield_cli.py
# Run basic commands to verify functionality

# 4. Run test suite
python3 tests/test_security_fixes.py
python3 tests/test_comprehensive_e2e.py

# 5. If tests pass, update requirements.txt
pip freeze | grep -E "openai|boto3|python-dotenv|httpx" > requirements.new.txt

# 6. If tests fail, rollback
pip install -r requirements.backup.txt
```

### Security Updates

```bash
# Check for security vulnerabilities
pip install safety
safety check

# Update vulnerable packages immediately
pip install --upgrade <vulnerable-package>
```

---

## Version Upgrades

### Upgrade Procedure

```bash
# 1. Backup current installation
cp -r zero-shield-cli zero-shield-cli.backup

# 2. Backup session files
cp session_state.json session_state.json.backup
cp session_kg.json session_kg.json.backup

# 3. Pull latest version
git fetch origin
git checkout <new-version-tag>

# 4. Update dependencies
pip install -r requirements.txt

# 5. Test new version
python3 zero_shield_cli.py --version
python3 tests/test_security_fixes.py

# 6. Verify session files compatible
python3 zero_shield_cli.py
# Check if session files load correctly

# 7. If issues, rollback
cd ../zero-shield-cli.backup
cp session_*.json.backup ../zero-shield-cli/
```

### Breaking Changes

Check CHANGELOG.md for breaking changes before upgrading.

**v2.0.0-dev → v2.1.0 (hypothetical):**
- Session file format may change
- New IAM permissions may be required
- Configuration file updates needed

---

## Log Rotation

### Manual Log Rotation

```bash
# Rotate logs weekly
mv zero_shield.log zero_shield.log.$(date +%Y%m%d)
gzip zero_shield.log.$(date +%Y%m%d)

# Keep last 4 weeks
find . -name "zero_shield.log.*.gz" -mtime +28 -delete
```

### Automated Log Rotation (logrotate)

```bash
# /etc/logrotate.d/zero-shield
/path/to/zero-shield-cli/zero_shield.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
    create 0600 user user
}
```

---

## Backup Strategy

### What to Backup

1. **Session files** - session_state.json, session_kg.json
2. **Configuration** - .env file (encrypted storage only!)
3. **Custom scripts** - Any automation scripts
4. **Logs** - Recent log files for audit trail

### Backup Procedure

```bash
#!/bin/bash
# backup_zero_shield.sh

BACKUP_DIR="/backups/zero-shield/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup session files
cp session_state.json $BACKUP_DIR/
cp session_kg.json $BACKUP_DIR/

# Backup configuration (ENCRYPTED ONLY!)
# NEVER backup .env to unencrypted storage
gpg --encrypt --recipient admin@example.com .env
cp .env.gpg $BACKUP_DIR/

# Backup logs
cp zero_shield.log $BACKUP_DIR/

# Compress backup
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup complete: $BACKUP_DIR.tar.gz"
```

### Backup to S3

```bash
# Upload encrypted backup to S3
aws s3 cp backups/zero-shield/$(date +%Y%m%d).tar.gz \
    s3://zero-shield-backups/$(date +%Y%m%d).tar.gz \
    --server-side-encryption AES256
```

### Backup Retention

- **Daily backups:** Keep 7 days
- **Weekly backups:** Keep 4 weeks
- **Monthly backups:** Keep 12 months

---

## Health Checks

### Daily Health Check

```bash
#!/bin/bash
# daily_health_check.sh

echo "=== Zero-Shield Health Check $(date) ==="

# 1. Check session files exist
if [ -f session_state.json ] && [ -f session_kg.json ]; then
    echo "✓ Session files present"
else
    echo "✗ Session files missing"
    exit 1
fi

# 2. Check file permissions
PERMS=$(stat -c %a session_state.json)
if [ "$PERMS" == "600" ]; then
    echo "✓ File permissions correct"
else
    echo "✗ File permissions incorrect ($PERMS)"
fi

# 3. Check file sizes
STATE_SIZE=$(du -k session_state.json | cut -f1)
KG_SIZE=$(du -k session_kg.json | cut -f1)
echo "  session_state.json: ${STATE_SIZE}KB"
echo "  session_kg.json: ${KG_SIZE}KB"

if [ $KG_SIZE -gt 1024 ]; then
    echo "⚠ Knowledge Graph large (${KG_SIZE}KB > 1MB)"
fi

# 4. Test AWS credentials
if aws sts get-caller-identity &>/dev/null; then
    echo "✓ AWS credentials valid"
else
    echo "✗ AWS credentials invalid"
    exit 1
fi

# 5. Test GitHub token
if curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    https://models.inference.ai.azure.com/models | grep -q "models"; then
    echo "✓ GitHub token valid"
else
    echo "✗ GitHub token invalid"
    exit 1
fi

echo "=== Health check complete ==="
```

### Automated Health Monitoring

```bash
# Add to crontab for daily checks
0 9 * * * /path/to/daily_health_check.sh | mail -s "Zero-Shield Health Check" admin@example.com
```

---

## Performance Optimization

### Optimize Knowledge Graph

```python
# optimize_kg.py
import json

# Load KG
with open('session_kg.json', 'r') as f:
    kg = json.load(f)

# Remove duplicate entries
optimized_kg = {}
for key, value in kg.items():
    # Deduplicate based on resource ID
    resource_id = value.get('resource_id')
    if resource_id not in optimized_kg:
        optimized_kg[resource_id] = value

# Save optimized KG
with open('session_kg.json', 'w') as f:
    json.dump(optimized_kg, f, indent=2)

print(f"Optimized: {len(kg)} → {len(optimized_kg)} entries")
```

### Clear Python Cache

```bash
# Remove Python bytecode cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

---

## Scheduled Maintenance Windows

### Monthly Maintenance

**First Sunday of each month, 2:00 AM:**

1. Backup session files
2. Prune Knowledge Graph
3. Rotate logs
4. Check for dependency updates
5. Run health checks
6. Review CloudTrail audit logs

### Quarterly Maintenance

**First Sunday of Jan/Apr/Jul/Oct, 2:00 AM:**

1. Full backup to S3
2. Rotate AWS credentials
3. Rotate GitHub token
4. Update dependencies
5. Review IAM policies
6. Test disaster recovery procedure

---

## Maintenance Checklist

### Daily
- [ ] Monitor session file sizes
- [ ] Check error logs
- [ ] Verify AWS/GitHub credentials valid

### Weekly
- [ ] Backup session files
- [ ] Rotate logs
- [ ] Review CloudTrail events

### Monthly
- [ ] Prune Knowledge Graph
- [ ] Check for dependency updates
- [ ] Run full test suite
- [ ] Review IAM policies

### Quarterly
- [ ] Rotate credentials
- [ ] Update dependencies
- [ ] Test disaster recovery
- [ ] Review security posture

---

## Next Steps

- Setup monitoring: `docs/admin-guide/MONITORING.md`
- Configure backups: `docs/admin-guide/BACKUP_RECOVERY.md`
- Review security: `docs/admin-guide/SECURITY.md`
