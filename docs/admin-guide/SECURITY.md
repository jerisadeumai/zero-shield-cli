# Security Administration Guide

**Last Updated:** March 15, 2026  
**Version:** v2.0.0-dev  
**Specification:** [Security Requirements](.kiro/specs/zero-shield-cli-comprehensive-spec/requirements.md)

## Overview

Zero-Shield CLI implements multiple security layers validated by formal specification. This guide covers security administration, IAM management, credential rotation, audit logging, and security group quarantine management.

**Security Requirements:** The security architecture is formally specified in Requirements 11-13 and 17 of the [comprehensive specification](.kiro/specs/zero-shield-cli-comprehensive-spec/requirements.md):
- **Requirement 11:** 5-layer credential redaction (10 acceptance criteria)
- **Requirement 12:** Prompt injection prevention (10 acceptance criteria)
- **Requirement 13:** Human-in-the-Loop confirmations (10 acceptance criteria)
- **Requirement 17:** XOR encryption for session files (10 acceptance criteria)

All security features are validated by property-based tests with 100% pass rate.

---

## Security Architecture

### 5-Layer Security Model

1. **Credential Redaction** - 5-layer pattern matching for AWS keys, secrets, tokens, JWT (Requirement 11)
2. **Input Sanitization** - Allowlist-based `_sanitize_aws_tag()` prevents prompt injection (Requirement 12)
3. **XOR Encryption** - Session files encrypted using GITHUB_TOKEN as key (Requirement 17)
4. **HITL Confirmations** - Human-in-the-Loop for destructive actions (requires full resource ID re-entry) (Requirement 13)
5. **File Permissions** - Restricted to owner only (0600 on Unix)

---

## IAM Role Management

### Required IAM Policies

See `aws-setup/IAM_POLICIES.md` for complete policy documentation.

**Policy Tiers:**
1. **zero-shield-minimal.json** - Read-only investigation (safe for testing)
2. **zero-shield-standard.json** - Standard operations (recommended)
3. **zero-shield-full.json** - Complete functionality (production)

### IAM User Setup

```bash
# Create IAM user
aws iam create-user --user-name ZeroShield-CLI-Agent

# Create user group
aws iam create-group --group-name ZeroShield-Agents

# Add user to group
aws iam add-user-to-group \
    --user-name ZeroShield-CLI-Agent \
    --group-name ZeroShield-Agents

# Attach policies to group
aws iam attach-group-policy \
    --group-name ZeroShield-Agents \
    --policy-arn arn:aws:iam::ACCOUNT_ID:policy/ZeroShield-Standard-Policy
```

### IAM Role for EC2

```bash
# Create trust policy
cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "ec2.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF

# Create role
aws iam create-role \
    --role-name ZeroShield-EC2-Role \
    --assume-role-policy-document file://trust-policy.json

# Attach policy
aws iam attach-role-policy \
    --role-name ZeroShield-EC2-Role \
    --policy-arn arn:aws:iam::ACCOUNT_ID:policy/ZeroShield-Standard-Policy
```

---

## Credential Rotation Procedures

### GitHub Token Rotation

**Frequency:** Every 90 days (recommended)

```bash
# 1. Generate new token at https://github.com/settings/tokens
# Scopes: None required (used only for GitHub Models API)

# 2. Update .env file
nano .env
# Replace GITHUB_TOKEN=ghp_old with GITHUB_TOKEN=ghp_new

# 3. Restart Zero-Shield
# Session files will be re-encrypted with new token

# 4. Verify
python3 zero_shield_cli.py
# Test LLM inference to confirm new token works

# 5. Revoke old token
# Go to https://github.com/settings/tokens and delete old token
```

### AWS Access Key Rotation

**Frequency:** Every 90 days (required by security policy)

```bash
# 1. Create new access key
aws iam create-access-key --user-name ZeroShield-CLI-Agent

# 2. Update .env file
nano .env
# Replace AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

# 3. Test new credentials
aws sts get-caller-identity

# 4. Delete old access key
aws iam delete-access-key \
    --user-name ZeroShield-CLI-Agent \
    --access-key-id AKIA_OLD_KEY_ID
```

---

## Audit Log Review

### CloudTrail Integration

Zero-Shield actions are logged to CloudTrail automatically.

**Key Events to Monitor:**
- `ec2:ModifyInstanceAttribute` (quarantine actions)
- `ec2:AuthorizeSecurityGroupIngress` (SG modifications)
- `iam:DeactivateAccessKey` (credential deactivation)
- `ec2:TerminateInstances` (instance termination)

### CloudTrail Query

```bash
# Find all Zero-Shield actions in last 24 hours
aws cloudtrail lookup-events \
    --lookup-attributes AttributeKey=Username,AttributeValue=ZeroShield-CLI-Agent \
    --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S) \
    --max-results 50
```

### Audit Log Analysis

```bash
# Export CloudTrail logs
aws cloudtrail lookup-events \
    --lookup-attributes AttributeKey=Username,AttributeValue=ZeroShield-CLI-Agent \
    --output json > zero_shield_audit.json

# Analyze actions
jq '.Events[] | {time: .EventTime, action: .EventName, resource: .Resources[0].ResourceName}' \
    zero_shield_audit.json
```

---

## Security Group Quarantine Management

### Quarantine SG Setup

```bash
# Create quarantine security group
aws ec2 create-security-group \
    --group-name ZeroShield-Quarantine \
    --description "Quarantine SG for compromised instances" \
    --vpc-id vpc-XXXXXXXX

# Get SG ID
QUARANTINE_SG_ID=$(aws ec2 describe-security-groups \
    --filters Name=group-name,Values=ZeroShield-Quarantine \
    --query 'SecurityGroups[0].GroupId' \
    --output text)

# Add to .env
echo "QUARANTINE_SG_ID=$QUARANTINE_SG_ID" >> .env
```

### Quarantine SG Rules

**Recommended Configuration:**
- **Inbound:** DENY ALL (no rules)
- **Outbound:** DENY ALL (remove default allow-all rule)

```bash
# Remove default outbound rule
aws ec2 revoke-security-group-egress \
    --group-id $QUARANTINE_SG_ID \
    --ip-permissions IpProtocol=-1,IpRanges=[{CidrIp=0.0.0.0/0}]
```

### Monitoring Quarantined Instances

```bash
# List instances in quarantine SG
aws ec2 describe-instances \
    --filters Name=instance.group-id,Values=$QUARANTINE_SG_ID \
    --query 'Reservations[].Instances[].[InstanceId,State.Name,LaunchTime]' \
    --output table
```

---

## Session File Encryption

### Encryption Details

- **Algorithm:** XOR encryption
- **Key:** GITHUB_TOKEN environment variable
- **Files:** session_state.json, session_kg.json
- **Permissions:** 0600 (owner read/write only)

### Verify Encryption

```bash
# Check file permissions
ls -la session_*.json
# Expected: -rw------- (600)

# Verify files are encrypted (not plaintext JSON)
head -c 100 session_state.json
# Should show binary/encrypted data, not readable JSON

# Test decryption (Zero-Shield does this automatically)
python3 zero_shield_cli.py
# If GITHUB_TOKEN is correct, files decrypt successfully
```

### Re-encrypt Session Files

```bash
# After GITHUB_TOKEN rotation, re-encrypt files
python3 -c "
import os, json, tempfile
from zero_shield_cli import _xor_encrypt, _xor_decrypt

# Read and re-encrypt session_state.json
with open('session_state.json', 'rb') as f:
    data = _xor_decrypt(f.read(), os.getenv('OLD_GITHUB_TOKEN'))
encrypted = _xor_encrypt(data, os.getenv('GITHUB_TOKEN'))

# Write atomically
temp = tempfile.NamedTemporaryFile(mode='wb', delete=False)
temp.write(encrypted)
temp.close()
os.replace(temp.name, 'session_state.json')
os.chmod('session_state.json', 0o600)
"
```

---

## Security Incident Response

### Compromised Credentials

**If AWS credentials are compromised:**
```bash
# 1. Immediately deactivate access key
aws iam update-access-key \
    --user-name ZeroShield-CLI-Agent \
    --access-key-id AKIA_COMPROMISED \
    --status Inactive

# 2. Review CloudTrail for unauthorized actions
aws cloudtrail lookup-events \
    --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=AKIA_COMPROMISED

# 3. Create new access key and rotate
# (See Credential Rotation section above)

# 4. Delete compromised key
aws iam delete-access-key \
    --user-name ZeroShield-CLI-Agent \
    --access-key-id AKIA_COMPROMISED
```

**If GitHub token is compromised:**
```bash
# 1. Revoke token immediately at https://github.com/settings/tokens
# 2. Generate new token
# 3. Update .env file
# 4. Re-encrypt session files (see above)
```

### Session File Corruption

```bash
# If session files are corrupted or compromised:
# 1. Backup current files
cp session_state.json session_state.json.compromised
cp session_kg.json session_kg.json.compromised

# 2. Delete corrupted files
rm session_state.json session_kg.json

# 3. Restart Zero-Shield (will create fresh encrypted files)
python3 zero_shield_cli.py
```

---

## Security Best Practices

1. **Principle of Least Privilege** - Use minimal IAM policy for your use case
2. **Credential Rotation** - Rotate every 90 days minimum
3. **Audit Logging** - Enable CloudTrail in all regions
4. **Session File Protection** - Never commit session files to git
5. **HITL Confirmations** - Never bypass human confirmation for destructive actions
6. **Network Isolation** - Run in private subnet when possible
7. **MFA Enforcement** - Require MFA for IAM users
8. **Regular Reviews** - Audit IAM policies and CloudTrail logs monthly

---

## Compliance Considerations

### Data Residency
- Session files stored locally (not transmitted)
- LLM inference via GitHub Models API (Microsoft Azure)
- AWS API calls remain in your AWS region

### Audit Requirements
- CloudTrail provides complete audit trail
- Session files contain investigation history
- All actions require human confirmation

### Access Control
- IAM policies enforce least privilege
- Session files encrypted at rest
- No shared credentials between users

---

## Next Steps

- Setup monitoring: `docs/admin-guide/MONITORING.md`
- Configure maintenance: `docs/admin-guide/MAINTENANCE.md`
- Review troubleshooting: `docs/admin-guide/TROUBLESHOOTING.md`
