# Production AWS IAM Policies

**Last Verified:** March 15, 2026  
**IAM User:** `ZeroShield-CLI-Agent` (example)  
**User Group:** `ZeroShield-Agents` (example)  
**AWS Account:** `[YOUR_AWS_ACCOUNT_ID]`

## Overview

This directory contains example production IAM policies that demonstrate the actual policy structure used in a live AWS environment. These policies follow the separation of concerns principle by splitting audit (read-only) and remediation (write) capabilities.

**IMPORTANT:** Replace `[YOUR_AWS_ACCOUNT_ID]` with your actual AWS account ID when deploying these policies.

---

## Policy Architecture

### Two-Policy Approach

Instead of the three-tier system (minimal/standard/full), production environments often use a two-policy approach:

1. **Audit Policy** - Comprehensive read-only access
2. **Remediation Policy** - Targeted write operations

This separation allows for:
- Granular permission management
- Easier compliance auditing
- Clear separation of read vs. write operations
- Flexible policy attachment (audit-only users vs. full-access users)

---

## Policy 1: ZeroShield-Audit-Policy

**File:** `ZeroShield-Audit-Policy.json`  
**Type:** Customer managed  
**Purpose:** Read-only access to all AWS resources for security investigation

### Capabilities

**EC2 & Networking:**
- Describe instances, security groups, VPCs, subnets, volumes, snapshots
- View network ACLs and key pairs
- Get console output
- View IAM instance profile associations

**IAM:**
- List users, roles, access keys, MFA devices
- View attached role policies
- Get instance profiles

**Storage:**
- List S3 buckets and view policies/ACLs
- Describe RDS instances
- List and describe DynamoDB tables
- Describe EFS file systems

**Monitoring & Logging:**
- CloudWatch logs and metrics
- CloudTrail event lookup
- EventBridge rules

**Security Services:**
- GuardDuty detectors and findings
- KMS keys and rotation status
- WAF Web ACLs
- Macie bucket descriptions

**Cost & Lambda:**
- Cost Explorer data
- List and describe Lambda functions

### Use Cases

- Security audits and compliance reviews
- Incident investigation (read-only phase)
- Cost analysis and optimization
- Resource inventory and discovery

---

## Policy 2: ZeroShield-Remediation-Policy

**File:** `ZeroShield-Remediation-Policy.json`  
**Type:** Customer managed  
**Purpose:** Write operations for incident response

### Capabilities

**Instance Quarantine:**
- `ec2:ModifyInstanceAttribute` - Change instance security group assignment
- Allows moving compromised instances to quarantine security group

**IAM Key Deactivation:**
- `iam:UpdateAccessKey` - Deactivate compromised IAM access keys
- Sets key status to 'Inactive' (does not delete)

### Use Cases

- Quarantine compromised EC2 instances
- Deactivate leaked or compromised IAM access keys
- Emergency incident response actions

### Security Considerations

**Human-in-the-Loop (HITL) Protection:**
- All write operations require typing full resource IDs
- No simple "yes/no" confirmations
- Prevents accidental modifications

**Audit Trail:**
- All actions logged in CloudTrail
- User identity, timestamp, and resource tracked

---

## Deployment Instructions

### 1. Create IAM Policies

```bash
# Create Audit Policy
aws iam create-policy \
    --policy-name ZeroShield-Audit-Policy \
    --policy-document file://aws-setup/policies/production/ZeroShield-Audit-Policy.json \
    --description "Zero-Shield read-only audit access"

# Create Remediation Policy
aws iam create-policy \
    --policy-name ZeroShield-Remediation-Policy \
    --policy-document file://aws-setup/policies/production/ZeroShield-Remediation-Policy.json \
    --description "Zero-Shield incident response write operations"
```

### 2. Create IAM User and Group

```bash
# Create user group
aws iam create-group --group-name ZeroShield-Agents

# Create IAM user
aws iam create-user --user-name ZeroShield-CLI-Agent

# Add user to group
aws iam add-user-to-group \
    --user-name ZeroShield-CLI-Agent \
    --group-name ZeroShield-Agents
```

### 3. Attach Policies to Group

```bash
# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Attach Audit Policy
aws iam attach-group-policy \
    --group-name ZeroShield-Agents \
    --policy-arn arn:aws:iam::${ACCOUNT_ID}:policy/ZeroShield-Audit-Policy

# Attach Remediation Policy
aws iam attach-group-policy \
    --group-name ZeroShield-Agents \
    --policy-arn arn:aws:iam::${ACCOUNT_ID}:policy/ZeroShield-Remediation-Policy
```

### 4. Create Access Keys

```bash
# Create access key for the user
aws iam create-access-key --user-name ZeroShield-CLI-Agent

# Save the output - you'll need AccessKeyId and SecretAccessKey for .env file
```

---

## Policy Comparison: Production vs. Three-Tier

### Production Two-Policy Approach

| Policy | Read | Quarantine | IAM Keys |
|--------|------|------------|----------|
| Audit | ✅ | ❌ | ❌ |
| Audit + Remediation | ✅ | ✅ | ✅ |

### Three-Tier Approach (Development/Testing)

| Policy | Read | Quarantine | IAM Keys |
|--------|------|------------|----------|
| Minimal | ✅ | ❌ | ❌ |
| Standard | ✅ | ✅ | ❌ |
| Full | ✅ | ✅ | ✅ |

**Recommendation:**
- **Production:** Use two-policy approach (Audit + Remediation)
- **Development/Testing:** Use three-tier approach (Minimal/Standard/Full)

---

## Verification

### Test Audit Policy

```bash
# Test read-only access
aws ec2 describe-instances --max-results 1
aws iam list-users --max-items 1
aws s3api list-buckets
aws guardduty list-detectors
```

### Test Remediation Policy

```bash
# Test quarantine capability (dry-run)
aws ec2 modify-instance-attribute \
    --instance-id i-1234567890abcdef0 \
    --groups sg-quarantine-id \
    --dry-run

# Test IAM key deactivation (dry-run)
aws iam update-access-key \
    --user-name test-user \
    --access-key-id AKIAIOSFODNN7EXAMPLE \
    --status Inactive \
    --dry-run
```

---

## Security Best Practices

1. **Separate Policies:** Keep audit and remediation policies separate for granular control
2. **Least Privilege:** Only attach remediation policy to users who need write access
3. **MFA Required:** Enforce MFA for all users with remediation policy
4. **CloudTrail Enabled:** Ensure all actions are logged
5. **Regular Reviews:** Audit policy attachments quarterly
6. **Credential Rotation:** Rotate access keys every 90 days

---

## Troubleshooting

### "Access Denied" Errors

```bash
# Check which policies are attached
aws iam list-attached-group-policies --group-name ZeroShield-Agents

# Verify policy document
aws iam get-policy-version \
    --policy-arn arn:aws:iam::ACCOUNT_ID:policy/ZeroShield-Audit-Policy \
    --version-id v1
```

### Policy Not Found

```bash
# List all customer-managed policies
aws iam list-policies --scope Local --query 'Policies[?contains(PolicyName, `ZeroShield`)]'
```

---

## Next Steps

- Review main IAM setup guide: `aws-setup/IAM_POLICIES.md`
- Configure quarantine security group: See SECURITY.md
- Setup CloudTrail logging: See MONITORING.md
- Test Zero-Shield CLI: `python3 zero_shield_cli.py`

---

**Note:** This is a template. Replace placeholder values with your actual AWS account details when deploying.
