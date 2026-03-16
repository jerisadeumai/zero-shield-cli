# Troubleshooting Guide

**Last Updated:** March 15, 2026  
**Version:** v2.0.0-dev

## Common Issues and Solutions

---

## API Rate Limiting Issues

### Symptoms
```
[!] Rate limit approaching (80% quota used)
[ERROR] AWS API throttling detected
ThrottlingException: Rate exceeded
```

### Causes
- Too many API calls in short time
- Shared AWS account with other applications
- Insufficient service quotas

### Solutions

**1. Implement exponential backoff (already built-in):**
Zero-Shield automatically retries with backoff. Wait for cooldown period.

**2. Request quota increase:**
```bash
# Check current quotas
aws service-quotas list-service-quotas \
    --service-code ec2 \
    --query 'Quotas[?QuotaName==`EC2-VPC Elastic IPs`]'

# Request increase
aws service-quotas request-service-quota-increase \
    --service-code ec2 \
    --quota-code L-0263D0A3 \
    --desired-value 100
```

**3. Reduce query frequency:**
- Use Knowledge Graph cache (session_kg.json) instead of repeated API calls
- Batch operations when possible

---

## Session Corruption Recovery

### Symptoms
```
[ERROR] Failed to load session state
[ERROR] JSON decode error
Session file corrupted
```

### Diagnosis
```bash
# Check if files are valid JSON
python3 -c "import json; json.load(open('session_state.json'))"
python3 -c "import json; json.load(open('session_kg.json'))"
```

### Solutions

**1. Restore from backup:**
```bash
# If you have backups
cp session_state.json.backup session_state.json
cp session_kg.json.backup session_kg.json
```

**2. Delete and rebuild:**
```bash
# Backup corrupted files for analysis
mv session_state.json session_state.json.corrupted
mv session_kg.json session_kg.json.corrupted

# Restart Zero-Shield (creates fresh files)
python3 zero_shield_cli.py
```

**3. Manual repair (advanced):**
```bash
# Decrypt and inspect
python3 -c "
import os, json
from zero_shield_cli import _xor_decrypt

with open('session_state.json', 'rb') as f:
    decrypted = _xor_decrypt(f.read(), os.getenv('GITHUB_TOKEN'))
    print(decrypted.decode('utf-8'))
"
```

---

## AWS Credential Problems

### Symptoms
```
[ERROR] AWS credentials invalid
botocore.exceptions.NoCredentialsError
botocore.exceptions.ClientError: An error occurred (UnauthorizedOperation)
```

### Diagnosis
```bash
# Test AWS credentials
aws sts get-caller-identity

# Check IAM permissions
aws iam get-user
aws iam list-attached-user-policies --user-name $(aws sts get-caller-identity --query 'Arn' --output text | cut -d'/' -f2)
```

### Solutions

**1. Verify .env configuration:**
```bash
# Check .env file
cat .env | grep -E "AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_DEFAULT_REGION"

# Ensure no extra spaces or quotes
# CORRECT: AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
# WRONG: AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
```

**2. Refresh credentials (CloudShell):**
```bash
# CloudShell credentials expire after 12 hours
# Simply restart CloudShell session
```

**3. Verify IAM policies:**
```bash
# Check attached policies
aws iam list-attached-user-policies --user-name ZeroShield-CLI-Agent

# Verify policy document
aws iam get-policy-version \
    --policy-arn arn:aws:iam::ACCOUNT_ID:policy/ZeroShield-Standard-Policy \
    --version-id v1
```

**4. Test specific permissions:**
```bash
# Test EC2 permissions
aws ec2 describe-instances --max-results 1

# Test IAM permissions
aws iam list-users --max-items 1

# Test S3 permissions
aws s3 ls
```

---

## LLM Model Failures

### Symptoms
```
[ERROR] LLM API error (retrying...)
openai.OpenAIError: Connection timeout
Model not available
```

### Diagnosis
```bash
# Test GitHub Models API
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     https://models.inference.ai.azure.com/models

# Check token validity
echo $GITHUB_TOKEN | wc -c  # Should be ~40-50 characters
```

### Solutions

**1. Verify GitHub token:**
```bash
# Check token in .env
grep GITHUB_TOKEN .env

# Test token manually
curl -H "Authorization: Bearer ghp_YOUR_TOKEN" \
     https://models.inference.ai.azure.com/models
```

**2. Switch to different model:**
```python
# In Zero-Shield REPL, try different model
# Available: gpt-4o-mini, Llama-3.3-70B-Instruct, Phi-4, DeepSeek-V3, gpt-4o
```

**3. Check network connectivity:**
```bash
# Test HTTPS connectivity
curl -I https://models.inference.ai.azure.com

# Check DNS resolution
nslookup models.inference.ai.azure.com

# Test from different network
```

**4. Rate limiting:**
GitHub Models API has rate limits. Wait 60 seconds and retry.

---

## Performance Degradation

### Symptoms
- Slow response times (> 10 seconds)
- High memory usage
- Unresponsive REPL

### Diagnosis
```bash
# Check process memory
ps aux | grep zero_shield_cli.py

# Check session file sizes
du -h session_*.json

# Monitor system resources
top -p $(pgrep -f zero_shield_cli.py)
```

### Solutions

**1. Prune Knowledge Graph:**
```bash
# Backup and delete KG
cp session_kg.json session_kg.json.backup
rm session_kg.json

# Restart (KG will rebuild)
python3 zero_shield_cli.py
```

**2. Clear session state:**
```bash
# Delete session files
rm session_state.json session_kg.json

# Restart fresh
python3 zero_shield_cli.py
```

**3. Increase system resources:**
- Upgrade to larger EC2 instance type
- Increase CloudShell timeout
- Add swap space (Linux)

---

## Installation Issues

### Python Version Mismatch

**Symptoms:**
```
SyntaxError: invalid syntax
ModuleNotFoundError: No module named 'typing'
```

**Solution:**
```bash
# Check Python version
python3 --version  # Must be 3.9+

# Use specific Python version
python3.9 zero_shield_cli.py
```

### Dependency Installation Failures

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement openai==2.24.0
pip install failed
```

**Solution:**
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Install individually if needed
pip install openai==2.24.0
pip install boto3==1.42.1
pip install python-dotenv==1.2.1
pip install httpx>=0.24.0
```

---

## Network Connectivity Issues

### Symptoms
```
[ERROR] Connection timeout
requests.exceptions.ConnectionError
Unable to reach AWS endpoints
```

### Diagnosis
```bash
# Test AWS endpoint connectivity
curl -I https://ec2.us-east-1.amazonaws.com

# Test GitHub Models API
curl -I https://models.inference.ai.azure.com

# Check DNS resolution
nslookup ec2.us-east-1.amazonaws.com
```

### Solutions

**1. Verify security group rules (EC2):**
```bash
# Check outbound rules
aws ec2 describe-security-groups \
    --group-ids sg-YOUR_SG_ID \
    --query 'SecurityGroups[0].IpPermissionsEgress'

# Ensure HTTPS (443) is allowed outbound
```

**2. Check network ACLs:**
```bash
# List network ACLs
aws ec2 describe-network-acls \
    --filters Name=vpc-id,Values=vpc-YOUR_VPC_ID
```

**3. Verify proxy settings:**
```bash
# Check proxy environment variables
echo $HTTP_PROXY
echo $HTTPS_PROXY

# Unset if not needed
unset HTTP_PROXY HTTPS_PROXY
```

---

## File Permission Errors

### Symptoms
```
[ERROR] Permission denied: session_state.json
PermissionError: [Errno 13]
```

### Solutions
```bash
# Fix file permissions
chmod 600 session_state.json session_kg.json

# Fix ownership
chown $USER:$USER session_*.json

# Verify
ls -la session_*.json
# Expected: -rw------- 1 user user
```

---

## Quarantine Action Failures

### Symptoms
```
[ERROR] Failed to quarantine instance
UnauthorizedOperation: You are not authorized to perform this operation
```

### Diagnosis
```bash
# Verify QUARANTINE_SG_ID in .env
grep QUARANTINE_SG_ID .env

# Check if SG exists
aws ec2 describe-security-groups --group-ids sg-YOUR_QUARANTINE_SG_ID

# Verify IAM permissions
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::ACCOUNT_ID:user/ZeroShield-CLI-Agent \
    --action-names ec2:ModifyInstanceAttribute \
    --resource-arns arn:aws:ec2:*:ACCOUNT_ID:instance/*
```

### Solutions

**1. Create quarantine SG:**
```bash
# See docs/admin-guide/SECURITY.md for setup instructions
```

**2. Update IAM policy:**
Ensure policy includes `ec2:ModifyInstanceAttribute` permission.

**3. Verify SG in same VPC:**
Quarantine SG must be in same VPC as target instance.

---

## Debugging Tips

### Enable Verbose Logging

```python
# Add to zero_shield_cli.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Capture Full Stack Traces

```bash
# Run with Python debugger
python3 -m pdb zero_shield_cli.py

# Or capture exceptions
python3 zero_shield_cli.py 2>&1 | tee debug.log
```

### Test Individual Components

```python
# Test AWS connectivity
python3 -c "import boto3; print(boto3.client('ec2').describe_instances(MaxResults=1))"

# Test LLM API
python3 -c "from openai import OpenAI; client = OpenAI(base_url='https://models.inference.ai.azure.com', api_key='YOUR_TOKEN'); print(client.models.list())"

# Test session file encryption
python3 -c "from zero_shield_cli import _xor_encrypt, _xor_decrypt; print('Encryption test: OK')"
```

---

## Getting Help

### Collect Diagnostic Information

```bash
# System information
uname -a
python3 --version
pip list | grep -E "openai|boto3|python-dotenv|httpx"

# AWS configuration
aws sts get-caller-identity
aws configure list

# Zero-Shield version
grep "VERSION =" zero_shield_cli.py

# Recent logs
tail -100 zero_shield.log
```

### Report Issues

Include in bug reports:
1. Zero-Shield version (v2.0.0-dev)
2. Python version
3. Operating system
4. Error message (full stack trace)
5. Steps to reproduce
6. Diagnostic information (above)

---

## Next Steps

- Review security: `docs/admin-guide/SECURITY.md`
- Setup monitoring: `docs/admin-guide/MONITORING.md`
- Configure maintenance: `docs/admin-guide/MAINTENANCE.md`
