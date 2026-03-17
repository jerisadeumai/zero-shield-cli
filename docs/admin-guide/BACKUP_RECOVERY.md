# Backup and Recovery Guide

> ⚠️ **DEVELOPMENT BRANCH**  
> Version: v2.0.0-dev | Status: Development Only | Not Production Ready

**Last Updated:** March 17, 2026  
**Version:** v2.0.0-dev

## Overview

This guide covers backup strategies, disaster recovery procedures, and session state restoration for Zero-Shield CLI.

---

## Backup Strategy

### What to Backup

| Item | Priority | Frequency | Retention |
|------|----------|-----------|-----------|
| session_state.json | HIGH | Daily | 7 days |
| session_kg.json | HIGH | Daily | 30 days |
| .env (encrypted) | CRITICAL | On change | Indefinite |
| zero_shield.log | MEDIUM | Weekly | 4 weeks |
| Custom scripts | LOW | On change | Indefinite |

### Backup Locations

**Local Backups:**
- `/backups/zero-shield/` (local filesystem)
- Encrypted external drive

**Remote Backups:**
- S3 bucket with versioning enabled
- Encrypted cloud storage (AWS Backup, Azure Backup)

---

## Session State Backup

### Manual Backup

```bash
# Create backup directory
mkdir -p backups/$(date +%Y%m%d_%H%M%S)

# Backup session files
cp session_state.json backups/$(date +%Y%m%d_%H%M%S)/
cp session_kg.json backups/$(date +%Y%m%d_%H%M%S)/

# Verify backup
ls -lh backups/$(date +%Y%m%d_%H%M%S)/
```

### Automated Backup Script

```bash
#!/bin/bash
# backup_sessions.sh

BACKUP_ROOT="/backups/zero-shield"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup session files
if [ -f session_state.json ]; then
    cp session_state.json $BACKUP_DIR/
    echo "✓ Backed up session_state.json"
fi

if [ -f session_kg.json ]; then
    cp session_kg.json $BACKUP_DIR/
    echo "✓ Backed up session_kg.json"
fi

# Compress backup
tar -czf $BACKUP_DIR.tar.gz -C $BACKUP_ROOT $TIMESTAMP
rm -rf $BACKUP_DIR

# Upload to S3 (optional)
if [ -n "$S3_BACKUP_BUCKET" ]; then
    aws s3 cp $BACKUP_DIR.tar.gz \
        s3://$S3_BACKUP_BUCKET/zero-shield/$TIMESTAMP.tar.gz \
        --server-side-encryption AES256
    echo "✓ Uploaded to S3"
fi

# Cleanup old local backups (keep 7 days)
find $BACKUP_ROOT -name "*.tar.gz" -mtime +7 -delete

echo "Backup complete: $BACKUP_DIR.tar.gz"
```

### Schedule Automated Backups

```bash
# Add to crontab for daily backups at 2 AM
0 2 * * * /path/to/backup_sessions.sh >> /var/log/zero-shield-backup.log 2>&1
```

---

## Knowledge Graph Backup

### Full KG Backup

```bash
# Backup with metadata
cat > kg_backup_metadata.json <<EOF
{
  "backup_date": "$(date -Iseconds)",
  "kg_size_bytes": $(stat -f%z session_kg.json),
  "kg_entries": $(python3 -c "import json; print(len(json.load(open('session_kg.json'))))")
}
EOF

# Create backup archive
tar -czf kg_backup_$(date +%Y%m%d).tar.gz \
    session_kg.json \
    kg_backup_metadata.json
```

### Incremental KG Backup

```python
# incremental_kg_backup.py
import json
from datetime import datetime

# Load current and previous KG
with open('session_kg.json', 'r') as f:
    current_kg = json.load(f)

try:
    with open('session_kg.previous.json', 'r') as f:
        previous_kg = json.load(f)
except FileNotFoundError:
    previous_kg = {}

# Find new/changed entries
delta = {
    k: v for k, v in current_kg.items()
    if k not in previous_kg or previous_kg[k] != v
}

# Save delta
with open(f'kg_delta_{datetime.now().strftime("%Y%m%d")}.json', 'w') as f:
    json.dump(delta, f, indent=2)

# Update previous KG
with open('session_kg.previous.json', 'w') as f:
    json.dump(current_kg, f)

print(f"Incremental backup: {len(delta)} new/changed entries")
```

---

## Configuration Backup

### Backup .env File (ENCRYPTED ONLY!)

**CRITICAL:** Never backup .env to unencrypted storage!

```bash
# Encrypt .env with GPG
gpg --encrypt --recipient admin@example.com .env

# Backup encrypted file
cp .env.gpg backups/env_backup_$(date +%Y%m%d).gpg

# Upload to S3 (encrypted)
aws s3 cp .env.gpg \
    s3://zero-shield-secure-backups/env_backup_$(date +%Y%m%d).gpg \
    --server-side-encryption aws:kms \
    --ssekms-key-id arn:aws:kms:REGION:ACCOUNT:key/KEY_ID
```

### Restore .env File

```bash
# Download from S3
aws s3 cp s3://zero-shield-secure-backups/env_backup_YYYYMMDD.gpg .

# Decrypt
gpg --decrypt env_backup_YYYYMMDD.gpg > .env

# Set permissions
chmod 600 .env

# Verify
cat .env | grep -E "GITHUB_TOKEN|AWS_ACCESS_KEY_ID"
```

---

## S3 Backup Strategy

### Setup S3 Backup Bucket

```bash
# Create backup bucket
aws s3 mb s3://zero-shield-backups --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket zero-shield-backups \
    --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
    --bucket zero-shield-backups \
    --server-side-encryption-configuration '{
      "Rules": [{
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        }
      }]
    }'

# Set lifecycle policy (delete after 90 days)
aws s3api put-bucket-lifecycle-configuration \
    --bucket zero-shield-backups \
    --lifecycle-configuration '{
      "Rules": [{
        "Id": "DeleteOldBackups",
        "Status": "Enabled",
        "Expiration": {"Days": 90}
      }]
    }'
```

### Upload Backups to S3

```bash
# Upload session files
aws s3 sync backups/ s3://zero-shield-backups/ \
    --exclude "*" \
    --include "*.tar.gz" \
    --server-side-encryption AES256
```

---

## Disaster Recovery Procedures

### Scenario 1: Session File Corruption

**Symptoms:**
- JSON decode errors
- Session files unreadable
- Zero-Shield fails to start

**Recovery:**
```bash
# 1. Stop Zero-Shield
pkill -f zero_shield_cli.py

# 2. Backup corrupted files
mv session_state.json session_state.json.corrupted
mv session_kg.json session_kg.json.corrupted

# 3. Restore from latest backup
cp backups/YYYYMMDD_HHMMSS/session_state.json .
cp backups/YYYYMMDD_HHMMSS/session_kg.json .

# 4. Verify file integrity
python3 -c "import json; json.load(open('session_state.json'))"
python3 -c "import json; json.load(open('session_kg.json'))"

# 5. Restart Zero-Shield
python3 zero_shield_cli.py
```

### Scenario 2: Complete System Failure

**Symptoms:**
- EC2 instance terminated
- CloudShell session expired
- Local system crash

**Recovery:**
```bash
# 1. Provision new environment
# (See docs/admin-guide/DEPLOYMENT.md)

# 2. Install Zero-Shield
git clone <repository-url>
cd zero-shield-cli
pip install -r requirements.txt

# 3. Restore configuration
# Download encrypted .env from S3
aws s3 cp s3://zero-shield-secure-backups/env_backup_LATEST.gpg .
gpg --decrypt env_backup_LATEST.gpg > .env
chmod 600 .env

# 4. Restore session files
# Download from S3
aws s3 cp s3://zero-shield-backups/YYYYMMDD_HHMMSS.tar.gz .
tar -xzf YYYYMMDD_HHMMSS.tar.gz
cp YYYYMMDD_HHMMSS/session_*.json .

# 5. Verify and start
python3 zero_shield_cli.py
```

### Scenario 3: Credential Compromise

**Symptoms:**
- Unauthorized AWS actions detected
- Credentials leaked

**Recovery:**
```bash
# 1. Immediately deactivate compromised credentials
aws iam update-access-key \
    --user-name ZeroShield-CLI-Agent \
    --access-key-id AKIA_COMPROMISED \
    --status Inactive

# 2. Create new credentials
aws iam create-access-key --user-name ZeroShield-CLI-Agent

# 3. Update .env file
nano .env
# Replace AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

# 4. Re-encrypt session files with new credentials
# (Session files use GITHUB_TOKEN, not AWS credentials)

# 5. Delete compromised credentials
aws iam delete-access-key \
    --user-name ZeroShield-CLI-Agent \
    --access-key-id AKIA_COMPROMISED

# 6. Review CloudTrail for unauthorized actions
aws cloudtrail lookup-events \
    --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=AKIA_COMPROMISED
```

---

## Recovery Testing

### Test Recovery Procedure (Monthly)

```bash
#!/bin/bash
# test_recovery.sh

echo "=== Recovery Test $(date) ==="

# 1. Create test backup
cp session_state.json session_state.json.test
cp session_kg.json session_kg.json.test

# 2. Simulate corruption
echo "corrupted" > session_state.json
echo "corrupted" > session_kg.json

# 3. Attempt recovery
cp session_state.json.test session_state.json
cp session_kg.json.test session_kg.json

# 4. Verify recovery
if python3 -c "import json; json.load(open('session_state.json'))" 2>/dev/null; then
    echo "✓ Recovery successful"
else
    echo "✗ Recovery failed"
    exit 1
fi

# 5. Cleanup
rm session_*.json.test

echo "=== Recovery test complete ==="
```

### Recovery Time Objective (RTO)

| Scenario | Target RTO | Steps |
|----------|------------|-------|
| Session corruption | < 5 minutes | Restore from local backup |
| System failure | < 30 minutes | Provision new system + restore from S3 |
| Credential compromise | < 15 minutes | Rotate credentials + update config |

### Recovery Point Objective (RPO)

| Data | Target RPO | Backup Frequency |
|------|------------|------------------|
| Session state | < 24 hours | Daily |
| Knowledge Graph | < 24 hours | Daily |
| Configuration | 0 (no data loss) | On change |

---

## Backup Verification

### Verify Backup Integrity

```bash
#!/bin/bash
# verify_backup.sh

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    exit 1
fi

# Extract to temp directory
TEMP_DIR=$(mktemp -d)
tar -xzf $BACKUP_FILE -C $TEMP_DIR

# Verify JSON integrity
for file in $TEMP_DIR/*/session_*.json; do
    if python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
        echo "✓ $(basename $file) valid"
    else
        echo "✗ $(basename $file) corrupted"
        rm -rf $TEMP_DIR
        exit 1
    fi
done

# Cleanup
rm -rf $TEMP_DIR

echo "Backup verification complete"
```

### Automated Backup Verification

```bash
# Add to crontab for weekly verification
0 3 * * 0 /path/to/verify_backup.sh /backups/zero-shield/latest.tar.gz
```

---

## Backup Retention Policy

### Local Backups

- **Daily backups:** Keep 7 days
- **Weekly backups:** Keep 4 weeks
- **Monthly backups:** Keep 3 months

### S3 Backups

- **Daily backups:** Keep 30 days
- **Weekly backups:** Keep 12 weeks
- **Monthly backups:** Keep 12 months

### Cleanup Script

```bash
#!/bin/bash
# cleanup_old_backups.sh

BACKUP_ROOT="/backups/zero-shield"

# Delete local backups older than 7 days
find $BACKUP_ROOT -name "*.tar.gz" -mtime +7 -delete

# Delete S3 backups older than 90 days (handled by lifecycle policy)
# No action needed - S3 lifecycle policy handles this
```

---

## Emergency Contacts

### Escalation Path

1. **Primary:** DevSecOps Team Lead
2. **Secondary:** Security Operations Manager
3. **Escalation:** CISO

### Contact Information

Store securely in encrypted password manager.

---

## Next Steps

- Setup monitoring: `docs/admin-guide/MONITORING.md`
- Review security: `docs/admin-guide/SECURITY.md`
- Configure maintenance: `docs/admin-guide/MAINTENANCE.md`
