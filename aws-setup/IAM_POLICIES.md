# AWS IAM Setup Guide

This guide helps you configure AWS IAM permissions for Zero-Shield CLI with detailed explanations of what each permission does and why it's needed.

## Policy Levels Overview

Zero-Shield offers three permission levels to match your security requirements:

| Policy Level | Use Case | Risk Level | Capabilities |
|--------------|----------|------------|--------------|
| **Minimal** | Investigation only | Low | Read-only access, no modifications |
| **Standard** | Most operations | Medium | + Quarantine, SG modifications |
| **Full** | Complete functionality | Higher | + IAM key deactivation, all features |

---

## Minimal Policy (Read-Only Investigation)

**Use Case:** Security investigation, compliance auditing, cost analysis 
**Risk:** Very Low - No modification capabilities 
**Recommended for:** Initial testing, compliance teams, read-only analysts

### What This Policy Allows
- List and inspect EC2 instances, security groups, VPCs
- View IAM users, roles, and access keys (no modifications)
- Read S3 bucket policies and public access settings
- View CloudWatch logs and metrics
- Check GuardDuty findings and KMS key status

### What This Policy CANNOT Do
- Quarantine instances or modify security groups
- Deactivate IAM access keys
- Modify any AWS resources

### JSON Policy
```json
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Sid": "EC2ReadOnlyAccess",
 "Effect": "Allow",
 "Action": [
 "ec2:DescribeInstances",
 "ec2:DescribeSecurityGroups",
 "ec2:DescribeVpcs",
 "ec2:DescribeSubnets",
 "ec2:DescribeVolumes",
 "ec2:DescribeSnapshots",
 "ec2:DescribeKeyPairs",
 "ec2:DescribeNetworkAcls",
 "ec2:GetConsoleOutput"
 ],
 "Resource": "*",
 "Condition": {
 "StringEquals": {
 "aws:RequestedRegion": ["us-east-1", "us-west-2", "eu-west-1"]
 }
 }
 },
 {
 "Sid": "IAMReadOnlyAccess",
 "Effect": "Allow",
 "Action": [
 "iam:ListUsers",
 "iam:ListRoles",
 "iam:ListAccessKeys",
 "iam:GetUser",
 "iam:GetLoginProfile",
 "iam:ListMFADevices"
 ],
 "Resource": "*"
 },
 {
 "Sid": "StorageReadOnlyAccess",
 "Effect": "Allow",
 "Action": [
 "s3:ListAllMyBuckets",
 "s3:GetBucketPolicy",
 "s3:GetBucketAcl",
 "s3:GetBucketPublicAccessBlock",
 "rds:DescribeDBInstances",
 "dynamodb:ListTables",
 "dynamodb:DescribeTable",
 "elasticfilesystem:DescribeFileSystems"
 ],
 "Resource": "*"
 },
 {
 "Sid": "MonitoringReadOnlyAccess",
 "Effect": "Allow",
 "Action": [
 "logs:DescribeLogGroups",
 "logs:DescribeLogStreams",
 "logs:GetLogEvents",
 "cloudwatch:DescribeAlarms",
 "cloudwatch:GetMetricStatistics",
 "cloudtrail:LookupEvents"
 ],
 "Resource": "*"
 },
 {
 "Sid": "SecurityServicesReadOnly",
 "Effect": "Allow",
 "Action": [
 "guardduty:ListDetectors",
 "guardduty:ListFindings",
 "guardduty:GetFindings",
 "kms:ListKeys",
 "kms:DescribeKey",
 "kms:GetKeyRotationStatus",
 "wafv2:ListWebACLs"
 ],
 "Resource": "*"
 },
 {
 "Sid": "CostAnalysisAccess",
 "Effect": "Allow",
 "Action": [
 "ce:GetCostAndUsage",
 "pricing:GetProducts"
 ],
 "Resource": "*"
 },
 {
 "Sid": "LambdaReadOnlyAccess",
 "Effect": "Allow",
 "Action": [
 "lambda:ListFunctions",
 "lambda:GetFunction"
 ],
 "Resource": "*"
 }
 ]
}
```

---

## ⚖ Standard Policy (Recommended)

**Use Case:** Most security operations including incident response 
**Risk:** Medium - Can quarantine instances and modify security groups 
**Recommended for:** Security analysts, incident responders, DevSecOps teams

### Additional Capabilities (Beyond Minimal)
- **Quarantine instances** by modifying their security groups
- **Modify security group rules** for emergency access control
- **Instance attribute modifications** for security hardening

### What This Policy CANNOT Do
- Deactivate IAM access keys (requires Full policy)
- Terminate or stop instances
- Delete resources

### JSON Policy
```json
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Sid": "InheritMinimalPolicy",
 "Effect": "Allow",
 "Action": [
 "ec2:DescribeInstances",
 "ec2:DescribeSecurityGroups",
 "ec2:DescribeVpcs",
 "ec2:DescribeSubnets",
 "ec2:DescribeVolumes",
 "ec2:DescribeSnapshots",
 "ec2:DescribeKeyPairs",
 "ec2:DescribeNetworkAcls",
 "ec2:GetConsoleOutput",
 "iam:ListUsers",
 "iam:ListRoles",
 "iam:ListAccessKeys",
 "iam:GetUser",
 "iam:GetLoginProfile",
 "iam:ListMFADevices",
 "s3:ListAllMyBuckets",
 "s3:GetBucketPolicy",
 "s3:GetBucketAcl",
 "s3:GetBucketPublicAccessBlock",
 "rds:DescribeDBInstances",
 "dynamodb:ListTables",
 "dynamodb:DescribeTable",
 "elasticfilesystem:DescribeFileSystems",
 "logs:DescribeLogGroups",
 "logs:DescribeLogStreams",
 "logs:GetLogEvents",
 "cloudwatch:DescribeAlarms",
 "cloudwatch:GetMetricStatistics",
 "cloudtrail:LookupEvents",
 "guardduty:ListDetectors",
 "guardduty:ListFindings",
 "guardduty:GetFindings",
 "kms:ListKeys",
 "kms:DescribeKey",
 "kms:GetKeyRotationStatus",
 "wafv2:ListWebACLs",
 "ce:GetCostAndUsage",
 "pricing:GetProducts",
 "lambda:ListFunctions",
 "lambda:GetFunction"
 ],
 "Resource": "*"
 },
 {
 "Sid": "InstanceQuarantineCapability",
 "Effect": "Allow",
 "Action": [
 "ec2:ModifyInstanceAttribute"
 ],
 "Resource": "arn:aws:ec2:*:*:instance/*",
 "Condition": {
 "StringEquals": {
 "ec2:Attribute": "groupSet"
 }
 }
 },
 {
 "Sid": "SecurityGroupModification",
 "Effect": "Allow",
 "Action": [
 "ec2:AuthorizeSecurityGroupIngress",
 "ec2:RevokeSecurityGroupIngress",
 "ec2:AuthorizeSecurityGroupEgress",
 "ec2:RevokeSecurityGroupEgress"
 ],
 "Resource": "arn:aws:ec2:*:*:security-group/*",
 "Condition": {
 "StringLike": {
 "ec2:GroupName": ["*quarantine*", "*emergency*", "*incident*"]
 }
 }
 }
 ]
}
```

---

## � Full Policy (Complete Functionality)

**Use Case:** Complete incident response including IAM key deactivation 
**Risk:** Higher - Can deactivate IAM access keys 
**Recommended for:** Senior security engineers, incident response leads

### Additional Capabilities (Beyond Standard)
- **Deactivate IAM access keys** for compromised accounts
- **Full security group modifications** without name restrictions
- **Complete incident response** capabilities

### Security Considerations
- This policy can deactivate IAM access keys, potentially locking out users
- Requires careful handling and should be limited to trusted personnel
- Consider using temporary credentials or assume-role patterns

### JSON Policy
```json
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Sid": "InheritStandardPolicy",
 "Effect": "Allow",
 "Action": [
 "ec2:DescribeInstances",
 "ec2:DescribeSecurityGroups",
 "ec2:DescribeVpcs",
 "ec2:DescribeSubnets",
 "ec2:DescribeVolumes",
 "ec2:DescribeSnapshots",
 "ec2:DescribeKeyPairs",
 "ec2:DescribeNetworkAcls",
 "ec2:GetConsoleOutput",
 "ec2:ModifyInstanceAttribute",
 "iam:ListUsers",
 "iam:ListRoles",
 "iam:ListAccessKeys",
 "iam:GetUser",
 "iam:GetLoginProfile",
 "iam:ListMFADevices",
 "s3:ListAllMyBuckets",
 "s3:GetBucketPolicy",
 "s3:GetBucketAcl",
 "s3:GetBucketPublicAccessBlock",
 "rds:DescribeDBInstances",
 "dynamodb:ListTables",
 "dynamodb:DescribeTable",
 "elasticfilesystem:DescribeFileSystems",
 "logs:DescribeLogGroups",
 "logs:DescribeLogStreams",
 "logs:GetLogEvents",
 "cloudwatch:DescribeAlarms",
 "cloudwatch:GetMetricStatistics",
 "cloudtrail:LookupEvents",
 "guardduty:ListDetectors",
 "guardduty:ListFindings",
 "guardduty:GetFindings",
 "kms:ListKeys",
 "kms:DescribeKey",
 "kms:GetKeyRotationStatus",
 "wafv2:ListWebACLs",
 "ce:GetCostAndUsage",
 "pricing:GetProducts",
 "lambda:ListFunctions",
 "lambda:GetFunction"
 ],
 "Resource": "*"
 },
 {
 "Sid": "FullSecurityGroupAccess",
 "Effect": "Allow",
 "Action": [
 "ec2:AuthorizeSecurityGroupIngress",
 "ec2:RevokeSecurityGroupIngress",
 "ec2:AuthorizeSecurityGroupEgress",
 "ec2:RevokeSecurityGroupEgress"
 ],
 "Resource": "arn:aws:ec2:*:*:security-group/*"
 },
 {
 "Sid": "IAMAccessKeyManagement",
 "Effect": "Allow",
 "Action": [
 "iam:UpdateAccessKey"
 ],
 "Resource": "arn:aws:iam::*:user/*",
 "Condition": {
 "StringEquals": {
 "iam:AccessKeyAge": "90"
 }
 }
 }
 ]
}
```

---

## Quarantine Security Group Setup

Zero-Shield can quarantine compromised instances by moving them to a restrictive security group.

### Create Quarantine Security Group

```bash
# Create the security group
aws ec2 create-security-group \
 --group-name ZeroShield-Quarantine \
 --description "Quarantine zone for compromised instances - blocks all traffic"

# Note the security group ID (sg-xxxxxxxxx)
# Add this to your .env file as QUARANTINE_SG_ID
```

### Recommended Quarantine Rules

The quarantine security group should have **NO inbound rules** and very restrictive outbound rules:

```bash
# Get the security group ID
SG_ID="sg-your-quarantine-sg-id"

# Remove default outbound rule (allows all traffic)
aws ec2 revoke-security-group-egress \
 --group-id $SG_ID \
 --protocol all \
 --port all \
 --cidr 0.0.0.0/0

# Add minimal outbound rules (optional - for logging/monitoring)
# Allow HTTPS to AWS services for CloudWatch logs
aws ec2 authorize-security-group-egress \
 --group-id $SG_ID \
 --protocol tcp \
 --port 443 \
 --cidr 0.0.0.0/0

# Allow DNS resolution
aws ec2 authorize-security-group-egress \
 --group-id $SG_ID \
 --protocol udp \
 --port 53 \
 --cidr 0.0.0.0/0
```

---

## � CloudShell vs Local Credentials

### AWS CloudShell (Recommended)
**Advantages:**
- Inherits your AWS console IAM role automatically
- No credential management needed
- Always uses your current AWS session permissions
- Automatically rotates with your session

**Environment file (.env):**
```env
# CloudShell - AWS credentials inherited automatically
GITHUB_TOKEN=your_github_token_here
QUARANTINE_SG_ID=sg-your_quarantine_group_id_here

# AWS credentials NOT needed - inherited from CloudShell session
```

### Local Development
**Advantages:**
- Full development environment
- Can use different AWS profiles
- Better for customization and testing

**Environment file (.env):**
```env
# Local development - AWS credentials required
GITHUB_TOKEN=your_github_token_here
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_DEFAULT_REGION=us-east-1
QUARANTINE_SG_ID=sg-your_quarantine_group_id_here
```

---

## Testing Your IAM Setup

### Test Script
Create a test script to verify your permissions:

```bash
#!/bin/bash
# test-iam-permissions.sh

echo "Testing Zero-Shield IAM permissions..."

# Test EC2 access
echo "✓ Testing EC2 access..."
aws ec2 describe-instances --max-items 1 > /dev/null 2>&1
if [ $? -eq 0 ]; then
 echo " EC2 describe permissions: OK"
else
 echo " ❌ EC2 describe permissions: FAILED"
fi

# Test IAM access
echo "✓ Testing IAM access..."
aws iam list-users --max-items 1 > /dev/null 2>&1
if [ $? -eq 0 ]; then
 echo " IAM list permissions: OK"
else
 echo " ❌ IAM list permissions: FAILED"
fi

# Test S3 access
echo "✓ Testing S3 access..."
aws s3api list-buckets > /dev/null 2>&1
if [ $? -eq 0 ]; then
 echo " S3 list permissions: OK"
else
 echo " ❌ S3 list permissions: FAILED"
fi

# Test GuardDuty access
echo "✓ Testing GuardDuty access..."
aws guardduty list-detectors > /dev/null 2>&1
if [ $? -eq 0 ]; then
 echo " GuardDuty permissions: OK"
else
 echo " ❌ GuardDuty permissions: FAILED"
fi

echo "Permission test complete!"
```

### Run the Test
```bash
chmod +x test-iam-permissions.sh
./test-iam-permissions.sh
```

---

## Security Best Practices

### 1. Principle of Least Privilege
- Start with **Minimal** policy for testing
- Upgrade to **Standard** only when needed
- Use **Full** policy only for senior incident responders

### 2. Conditional Access
- Restrict by IP address if possible:
```json
"Condition": {
 "IpAddress": {
 "aws:SourceIp": ["203.0.113.0/24", "198.51.100.0/24"]
 }
}
```

### 3. Time-Based Access
- Use temporary credentials for incident response
- Consider AWS STS assume-role patterns
- Implement session timeouts

### 4. Monitoring and Auditing
- Enable CloudTrail logging for all Zero-Shield actions
- Set up CloudWatch alarms for sensitive operations
- Regular access reviews

### 5. Multi-Factor Authentication
- Require MFA for IAM users with Zero-Shield policies
- Use hardware tokens for high-privilege accounts

---

## Troubleshooting IAM Issues

### Common Error Messages

#### "Access Denied" for EC2 operations
```
Error: An error occurred (UnauthorizedOperation) when calling the DescribeInstances operation
```
**Solution:** Verify EC2 permissions in your policy, check region restrictions

#### "Access Denied" for IAM operations 
```
Error: An error occurred (AccessDenied) when calling the ListUsers operation
```
**Solution:** Add IAM permissions, ensure no resource restrictions conflict

#### "Invalid security group" for quarantine
```
Error: The specified security group "sg-xxxxxxxxx" does not exist
```
**Solution:** Create quarantine security group, update QUARANTINE_SG_ID in .env

### Debug Commands
```bash
# Check current AWS identity
aws sts get-caller-identity

# Test specific permission
aws ec2 describe-instances --dry-run

# Check policy simulation
aws iam simulate-principal-policy \
 --policy-source-arn arn:aws:iam::123456789012:user/testuser \
 --action-names ec2:DescribeInstances \
 --resource-arns "*"
```

---

## Contact & Support

- **Repository:** https://github.com/jerisadeumai/zero-shield-cli
- **Issues:** [GitHub Issues](https://github.com/jerisadeumai/zero-shield-cli/issues)
- **Project Maintainer:** Jeri L3D | JeriSadeuM
- **Copyright:** © 2026 Jeri L3D | JeriSadeuM | All Rights Reserved