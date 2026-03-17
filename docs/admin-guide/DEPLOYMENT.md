# Deployment Guide

> ⚠️ **DEVELOPMENT BRANCH**  
> Version: v2.0.0-dev | Status: Development Only | Last Updated: March 17, 2026  
> **This branch contains features not yet in the main branch.**

**Last Updated:** March 17, 2026  
**Version:** v2.0.0-dev

## Overview

This guide covers production deployment strategies for Zero-Shield CLI across multiple environments.

## Supported Environments

### 1. AWS CloudShell (Recommended)
- Native IAM role integration
- No credential management required
- Persistent storage between sessions
- Pre-installed Python 3.9+

### 2. Local Development
- Full control over environment
- Requires manual credential configuration
- Suitable for testing and development

### 3. EC2 Instance
- Production-grade deployment
- IAM role-based authentication
- Persistent operation

---

## Pre-Deployment Checklist

- [ ] Python 3.9+ installed
- [ ] AWS credentials configured (IAM user or role)
- [ ] GitHub Personal Access Token obtained
- [ ] Quarantine security group created (for remediation actions)
- [ ] IAM policies attached (see aws-setup/IAM_POLICIES.md)

---

## CloudShell Deployment

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd zero-shield-cli

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp environments/cloudshell/.env.example .env
nano .env  # Edit with your GITHUB_TOKEN and QUARANTINE_SG_ID

# Run
python3 zero_shield_cli.py
```

### CloudShell-Specific Configuration

**Session Persistence:**
- Session files persist in `/home/cloudshell-user/`
- Files are encrypted using GITHUB_TOKEN as key
- Automatic cleanup after 120 days of inactivity

**IAM Role:**
- CloudShell inherits IAM role from your AWS user
- No AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY needed
- Verify permissions match required IAM policies

---

## Local Deployment

### Prerequisites
```bash
# Verify Python version
python3 --version  # Must be 3.9+

# Install dependencies
pip install -r requirements.txt
```

### Configuration
```bash
# Copy local environment template
cp environments/local/.env.example .env

# Edit configuration
nano .env
```

**Required .env variables:**
```bash
GITHUB_TOKEN=ghp_your_token_here
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1
QUARANTINE_SG_ID=sg-...
```

### Running
```bash
python3 zero_shield_cli.py
```

---

## EC2 Instance Deployment

### Instance Requirements
- **Instance Type:** t3.micro or larger
- **OS:** Amazon Linux 2023 or Ubuntu 22.04
- **IAM Role:** Attach Zero-Shield IAM policies
- **Security Group:** Allow outbound HTTPS (443)

### Setup Script
```bash
#!/bin/bash
# Install Python 3.9+
sudo yum install python3.9 -y  # Amazon Linux
# OR
sudo apt install python3.9 -y  # Ubuntu

# Clone repository
git clone <repository-url>
cd zero-shield-cli

# Install dependencies
pip3.9 install -r requirements.txt

# Configure environment
cp environments/local/.env.example .env
nano .env  # Add GITHUB_TOKEN and QUARANTINE_SG_ID

# Run
python3.9 zero_shield_cli.py
```

### Systemd Service (Optional)
```ini
[Unit]
Description=Zero-Shield CLI
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/zero-shield-cli
ExecStart=/usr/bin/python3.9 /home/ec2-user/zero-shield-cli/zero_shield_cli.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## Multi-Environment Strategy

### Development → Staging → Production

**Development:**
- Local workstation
- Minimal IAM policy (zero-shield-minimal.json)
- Test with non-production AWS account

**Staging:**
- EC2 instance or CloudShell
- Standard IAM policy (zero-shield-standard.json)
- Mirror production environment

**Production:**
- CloudShell (recommended) or dedicated EC2
- Full IAM policy (zero-shield-full.json)
- Production AWS account with audit logging

---

## Infrastructure Requirements

### Compute
- **CPU:** 1 vCPU minimum
- **Memory:** 512 MB minimum (1 GB recommended)
- **Storage:** 100 MB for application + session files

### Network
- **Outbound HTTPS (443):** Required for GitHub Models API
- **AWS API Endpoints:** Required for boto3 operations
- **No inbound ports required**

### IAM Permissions
See `aws-setup/IAM_POLICIES.md` for detailed policy requirements.

---

## Scaling Considerations

### Single-User Deployment
- CloudShell or local workstation
- Session files stored locally
- No horizontal scaling needed

### Team Deployment
- Multiple CloudShell sessions (one per analyst)
- Shared IAM policies via user group
- Independent session files per user

### Enterprise Deployment
- Centralized EC2 instance with SSH access
- Shared Knowledge Graph (session_kg.json)
- Centralized audit logging via CloudTrail

---

## High Availability Setup

### Active-Passive Configuration

**Primary Instance:**
- EC2 instance in primary region
- Full IAM policies attached
- Session files backed up to S3

**Standby Instance:**
- EC2 instance in secondary region
- Same IAM policies
- Restore session files from S3 on failover

### Session File Replication
```bash
# Backup session files to S3
aws s3 cp session_state.json s3://zero-shield-backup/session_state.json
aws s3 cp session_kg.json s3://zero-shield-backup/session_kg.json

# Restore on failover
aws s3 cp s3://zero-shield-backup/session_state.json .
aws s3 cp s3://zero-shield-backup/session_kg.json .
```

---

## Deployment Verification

### Post-Deployment Checks
```bash
# 1. Verify Python version
python3 --version

# 2. Verify dependencies
pip list | grep -E "openai|boto3|python-dotenv|httpx"

# 3. Verify AWS credentials
aws sts get-caller-identity

# 4. Test Zero-Shield startup
python3 zero_shield_cli.py
# Type 'exit' to quit after verification
```

### Test Suite Validation
```bash
# Run complete test suite to validate deployment
python3 -m pytest tests/ -v

# Expected output: 152 tests collected, 148 passed, 4 skipped
# Pass rate: 97.4% (4 Windows file permission tests skipped)
```

**Expected test output:**
```
================================= test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.0.0 -- python3
cachedir: .pytest_cache
rootdir: /path/to/zero-shield-cli
collected 152 tests

tests/test_action_detection.py::test_action_detection_basic PASSED                [ 5%]
tests/test_comprehensive_e2e.py::test_ec2_instance_listing PASSED                [15%]
tests/test_property_final_batch.py::TestProperty16ModelSelectionValidation::test_out_of_range_model_numbers_rejected PASSED [55%]
tests/test_security_fixes.py::test_file_permissions_unix PASSED                  [97%]
=============================== 148 passed, 4 skipped in 12.45s ===============================
```

### Smoke Tests by Category
```bash
# Test action detection (8 tests)
python3 -m pytest tests/test_action_detection.py -v

# Test security validation (35 tests)
python3 -m pytest tests/test_security_fixes.py -v

# Test comprehensive E2E (66 tests)
python3 -m pytest tests/test_comprehensive_e2e.py -v

# Test property-based validation (44 tests across 6 files)
python3 -m pytest tests/test_property_*.py -v
```

### Test Troubleshooting
```bash
# If tests fail, check common issues:

# 1. Missing dependencies
pip install -r requirements.txt

# 2. AWS credential issues
aws sts get-caller-identity

# 3. Environment configuration
cat .env | grep -E "GITHUB_TOKEN|AWS_"

# 4. File permissions (Unix/Linux)
chmod 600 .env
```

---

## Troubleshooting

See `docs/admin-guide/TROUBLESHOOTING.md` for common deployment issues.

---

## Security Best Practices

1. **Never commit .env files** - Always use .env.example templates
2. **Rotate GitHub tokens** - Every 90 days minimum
3. **Use IAM roles** - Prefer roles over access keys when possible
4. **Enable CloudTrail** - Audit all Zero-Shield actions
5. **Restrict security groups** - Quarantine SG should be highly restrictive

---

## Next Steps

- Configure monitoring: `docs/admin-guide/MONITORING.md`
- Review security: `docs/admin-guide/SECURITY.md`
- Setup maintenance: `docs/admin-guide/MAINTENANCE.md`
