# Real-World Usage Examples

> ⚠️ **DEVELOPMENT BRANCH**  
> Version: v2.0.0-dev | Status: Development Only | Last Updated: March 17, 2026  
> **This branch contains features not yet in the main branch.**

Practical scenarios showing how to use Zero-Shield CLI for common security operations.

**Important:** All resource IDs in these examples (like `i-0123456789abcdef0`, `sg-041a97ba55afb006e`) are placeholders. Replace them with your actual AWS resource IDs when following these examples.

## Incident Response Scenarios

### **Scenario 1: Suspicious Instance Investigation**

**Situation:** GuardDuty alert about unusual API calls from instance `i-0123456789abcdef0`

```bash
# Start Zero-Shield
python3 zero_shield_cli.py

# 1. Set the suspicious instance as target
> /target i-0123456789abcdef0
[*] Target resolved to instance: i-0123456789abcdef0

# 2. Get detailed instance information
> inspect this instance
[ACTION:INSPECT:i-0123456789abcdef0]
[OBSERVE]: Instance: i-0123456789abcdef0 | Name: WebServer-Prod | State: running
VPC: vpc-0fa1a386cc9ed95b7 | Subnet: subnet-02ce73a728f3cfaf7
Type: t3.medium | Public IP: 3.239.105.195 | Private IP: 172.31.9.39
Security Groups: sg-041a97ba55afb006e (WebServer-SG)
IAM Role: EC2-WebServer-Role

# 3. Check what permissions this instance has
> what IAM permissions does this instance have?
[ACTION:IAM_CHECK:i-0123456789abcdef0]
[OBSERVE]: IAM Role: EC2-WebServer-Role
Attached Policies: AmazonS3ReadOnlyAccess, CloudWatchAgentServerPolicy
Trust Policy: Allows EC2 service to assume this role

# 4. Analyze security group rules
> check its security group rules
[ACTION:SG_RULES:sg-041a97ba55afb006e]
[OBSERVE]: Security Group: sg-041a97ba55afb006e (WebServer-SG)
INBOUND RULES:
✓ HTTP (80) from 0.0.0.0/0 - PUBLIC ACCESS
✓ HTTPS (443) from 0.0.0.0/0 - PUBLIC ACCESS
⚠ SSH (22) from 0.0.0.0/0 - RISKY: SSH open to internet

# 5. Check recent GuardDuty findings
> show me recent guardduty findings
[ACTION:GUARDDUTY_FINDINGS]
[OBSERVE]: GuardDuty Findings (Last 24 hours):
[HIGH] UnauthorizedAPICall - Instance i-0123456789abcdef0
 └ Unusual S3 API calls detected at 2026-03-15 10:30 UTC

# 6. Check CloudTrail for recent activity
> show me recent cloudtrail events for this instance
[ACTION:CLOUDTRAIL]
[OBSERVE]: CloudTrail Events (Last 6 hours):
[2026-03-15 10:30] EC2-WebServer-Role - ListBuckets (S3)
[2026-03-15 10:31] EC2-WebServer-Role - GetObject (s3://sensitive-data-bucket/*)

# 7. DECISION: Instance is compromised - accessing sensitive S3 data
> this instance is compromised, isolate it immediately
[ACTION:QUARANTINE:i-0123456789abcdef0]
[HITL] CRITICAL ACTION: Quarantine i-0123456789abcdef0?
 This will ISOLATE the instance by changing its security group.
 The instance will lose all network connectivity except essential AWS services.
 To confirm, type the instance ID: i-0123456789abcdef0
Enter instance ID to confirm: i-0123456789abcdef0
[*] Instance i-0123456789abcdef0 quarantined successfully
[*] Security group changed to: sg-quarantine-zone
```

**Result:** Compromised instance isolated in under 2 minutes

---

### **Scenario 2: IAM Security Audit**

**Situation:** Monthly security review - check for IAM vulnerabilities

```bash
# 1. List all IAM users and check MFA status
> show me all iam users and their mfa status
[ACTION:IAM_USERS]
[OBSERVE]: IAM Users Found:
[1] john.doe - MFA: ✓ Enabled | Last Activity: 2 days ago | Keys: 1 active
[2] jane.smith - MFA: ✓ Enabled | Last Activity: 5 days ago | Keys: 0 active 
[3] service-account - MFA: ✗ Not Enabled | Last Activity: 1 hour ago | Keys: 2 active
[4] old-contractor - MFA: ✗ Not Enabled | Last Activity: 90 days ago | Keys: 1 active

# 2. Check for old access keys that need rotation
> show me access keys that need rotation
[ACTION:IAM_ACCESS_KEYS]
[OBSERVE]: Access Key Analysis:
[CRITICAL] AKIAIOSFODNN7EXAMPLE (old-contractor) - Age: 180 days - ROTATE NOW
[WARNING] AKIAJEXAMPLEKEY12345 (service-account) - Age: 95 days - Rotate soon
[OK] AKIABCDEFGHIJKLMNOP (john.doe) - Age: 30 days - Recently rotated

# 3. Deactivate the old contractor's key immediately
> deactivate access key AKIAIOSFODNN7EXAMPLE
[ACTION:DEACTIVATE_ACCESS_KEY:AKIAIOSFODNN7EXAMPLE]
[HITL] CRITICAL ACTION: Deactivate access key AKIAIOSFODNN7EXAMPLE?
 This will IMMEDIATELY disable the access key for user: old-contractor
 All applications using this key will lose access.
 To confirm, type the access key ID: AKIAIOSFODNN7EXAMPLE
Enter access key ID to confirm: AKIAIOSFODNN7EXAMPLE
[*] Access key AKIAIOSFODNN7EXAMPLE deactivated successfully

# 4. Check what IAM roles exist and their trust policies
> show me iam roles and their trust relationships
[ACTION:IAM_ROLES]
[OBSERVE]: IAM Roles Found:
[1] EC2-WebServer-Role - Trusted by: ec2.amazonaws.com
[2] Lambda-Execution-Role - Trusted by: lambda.amazonaws.com
[3] CrossAccount-Admin-Role - Trusted by: arn:aws:iam::123456789012:root
 ⚠ WARNING: Cross-account trust - review regularly
```

**Result:** Identified and fixed 2 security issues in 3 minutes

---

### **Scenario 3: S3 Security Assessment**

**Situation:** Data breach concern - audit S3 bucket security

```bash
# 1. List all S3 buckets and check public access
> show me all s3 buckets and their public access status
[ACTION:S3_BUCKETS]
[OBSERVE]: S3 Buckets Found:
[1] my-private-data - ✓ Private | Encryption: KMS | Versioning: Enabled
[2] website-assets - ⚠ PUBLIC READ | Encryption: None | Versioning: Disabled
[3] backup-storage - ✓ Private | Encryption: AES256 | Versioning: Enabled
[4] temp-uploads - ⚠ PUBLIC READ/WRITE | Encryption: None | Versioning: Disabled

# 2. Check the concerning public bucket policy
> show me the bucket policy for temp-uploads
[ACTION:S3_BUCKET_POLICY:temp-uploads]
[OBSERVE]: Bucket Policy for temp-uploads:
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 "Principal": "*",
 "Action": ["s3:GetObject", "s3:PutObject"],
 "Resource": "arn:aws:s3:::temp-uploads/*"
 }
 ]
}
⚠ CRITICAL: Bucket allows public read AND write access!

# 3. Get more details about website-assets bucket
> show me the bucket policy for website-assets 
[ACTION:S3_BUCKET_POLICY:website-assets]
[OBSERVE]: Bucket Policy for website-assets:
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow", 
 "Principal": "*",
 "Action": "s3:GetObject",
 "Resource": "arn:aws:s3:::website-assets/*"
 }
 ]
}
✓ OK: Public read-only access for website assets (expected)
```

**Result:** Identified critical security issue with temp-uploads bucket

---

### **Scenario 4: Cost Optimization Investigation**

**Situation:** Unexpected AWS bill increase - investigate costs

```bash
# 1. Check recent spending trends
> show me my aws spending for the last 7 days
[ACTION:COST_EXPLORER]
[OBSERVE]: 7-Day Cost Breakdown:
Total: $1,247.83 (↑ 45% from previous week)
By Service:
- EC2: $892.15 (71.5%) - ↑ 67% increase
- RDS: $234.50 (18.8%) - ↓ 5% decrease 
- S3: $89.23 (7.2%) - ↑ 12% increase
- Other: $31.95 (2.5%) - ↑ 8% increase

# 2. List all running instances to find cost drivers
> list all ec2 instances
[ACTION:LIST]
[OBSERVE]: EC2 Instances Found:
[1] i-0123456789abcdef0 WebServer-Prod (RUNNING) | t3.medium
[2] i-0987654321fedcba0 Database-Main (RUNNING) | r5.2xlarge 
[3] i-0abcdef123456789 ML-Training-01 (RUNNING) | p3.8xlarge ⚠ EXPENSIVE
[4] i-0fedcba987654321 ML-Training-02 (RUNNING) | p3.8xlarge ⚠ EXPENSIVE

# 3. Check cost for the expensive ML instances
> /target i-0abcdef123456789
> what does this instance cost per month?
[ACTION:COST_INSIGHT:i-0abcdef123456789]
[OBSERVE]: Cost Analysis for i-0abcdef123456789:
Instance Type: p3.8xlarge
Hourly Rate: $12.24
Daily Cost: $293.76
Monthly Estimate: $8,813.28
⚠ WARNING: This is a high-cost instance type

# 4. Check when these instances were launched
> inspect instance i-0abcdef123456789
[ACTION:INSPECT:i-0abcdef123456789]
[OBSERVE]: Instance: i-0abcdef123456789 | Name: ML-Training-01 | State: running
Launch Time: 2026-03-10 09:00:00 UTC (5 days ago)
Type: p3.8xlarge | AMI: ami-ml-training-v2.1
⚠ Instance has been running for 5 days continuously

# 5. Check CloudTrail to see who launched these instances
> show me recent cloudtrail events
[ACTION:CLOUDTRAIL]
[OBSERVE]: CloudTrail Events (Recent):
[2026-03-10 09:00] data-scientist@company.com - RunInstances (p3.8xlarge)
 └ Launched 2x p3.8xlarge instances for ML training
 └ Source: 203.0.113.25 | User Agent: aws-cli/2.1.34
```

**Result:** Found $17,626/month in unexpected ML training costs

---

### **Scenario 5: Network Security Analysis**

**Situation:** Security team wants to audit network configurations

```bash
# 1. List all security groups to get overview
> show me all security groups
[ACTION:LIST] # (This will include security groups in the snapshot)
[OBSERVE]: Security Groups:
[1] sg-041a97ba55afb006e (WebServer-SG) - 3 instances
[2] sg-0487c7ca0d112e716 (Database-SG) - 1 instance 
[3] sg-02324a1784a6ce615 (default) - 0 instances
[4] sg-0newgroupid (Admin-Access) - 2 instances

# 2. Check the admin access security group rules
> /target sg-0newgroupid
> check security group rules for admin access
[ACTION:SG_RULES:sg-0newgroupid]
[OBSERVE]: Security Group: sg-0newgroupid (Admin-Access)
INBOUND RULES:
⚠ SSH (22) from 0.0.0.0/0 - CRITICAL: SSH open to internet
⚠ RDP (3389) from 0.0.0.0/0 - CRITICAL: RDP open to internet
⚠ All traffic from 10.0.0.0/8 - RISKY: Broad internal access
OUTBOUND RULES:
✓ All traffic to 0.0.0.0/0 - Standard outbound access

# 3. Check VPC configuration
> what vpc are these instances in?
[ACTION:VPC_INFO:vpc-0fa1a386cc9ed95b7]
[OBSERVE]: VPC: vpc-0fa1a386cc9ed95b7 (Main-VPC)
CIDR: 10.0.0.0/16
Subnets:
- subnet-02ce73a728f3cfaf7 (Public) - 10.0.1.0/24 - 2 instances
- subnet-0987654321fedcba (Private) - 10.0.2.0/24 - 1 instance
Internet Gateway: igw-0123456789abcdef0 ✓ Attached
Route Tables: 2 (public/private routing configured)

# 4. Check network ACLs for additional security
> show me network acl rules
[ACTION:NETWORK_ACLS]
[OBSERVE]: Network ACLs:
[1] acl-default (Default) - Associated with all subnets
 INBOUND: Allow All (100) - 0.0.0.0/0
 OUTBOUND: Allow All (100) - 0.0.0.0/0
⚠ WARNING: Default NACL allows all traffic - consider restricting
```

**Result:** Identified critical network security issues requiring immediate attention

---

## Advanced Workflows

### **Multi-Model Investigation**

Use different models for different tasks:

```bash
# Use Phi-4 for compliance checking (most rule-compliant)
> /switch
[Select Phi-4]
> check if our security groups comply with company policy

# Switch to GPT-4o for complex analysis
> /switch 
[Select GPT-4o]
> analyze the security implications of these findings and recommend remediation steps

# Use DeepSeek-V3 for deep root cause analysis
> /switch
[Select DeepSeek-V3] 
> what could be the root cause of these unusual api calls?
```

### **Persistent Investigation Context**

Zero-Shield remembers your investigation across sessions:

```bash
# Day 1: Initial investigation
> /target i-suspicious-instance
> inspect instance
> check security groups
> exit

# Day 2: Continue investigation (context preserved)
> python3 zero_shield_cli.py
[*] Session restored from encrypted state
[*] Active target: i-suspicious-instance
> show me new guardduty findings since yesterday
> what's changed with this instance?
```

### **Batch Analysis**

Analyze multiple resources efficiently:

```bash
# Check multiple instances
> /target i-0123456789abcdef0
> inspect instance
> /target i-0987654321fedcba0 
> inspect instance
> /target i-0abcdef123456789
> inspect instance

# Compare security postures
> based on all the instances i've shown you, which one has the worst security posture?
```

---

## Emergency Response Playbook

### **Immediate Threat Response (< 2 minutes)**

```bash
# 1. Identify threat
> show me high severity guardduty findings

# 2. Target affected resource
> /target [resource-id-from-finding]

# 3. Gather intel
> inspect this resource
> check its security groups
> show me recent cloudtrail events

# 4. Isolate if compromised
> this resource is compromised, quarantine it immediately
```

### **Post-Incident Analysis (5-10 minutes)**

```bash
# 1. Timeline analysis
> show me cloudtrail events for the last 24 hours

# 2. Scope assessment 
> show me all resources in the same vpc
> check if other instances have similar security groups

# 3. Impact analysis
> what iam permissions did the compromised resource have?
> show me s3 buckets it could access

# 4. Cost impact
> estimate the cost impact of this incident
```

---

## � Pro Tips

### **Efficient Targeting**
```bash
# Use partial IDs (Zero-Shield auto-completes)
> /target i-0123456 # Resolves to full ID

# Use resource names
> /target WebServer-Prod # Finds by name tag

# Use aliases
> /target database # Fuzzy matches "Database-Main"
```

### **Context Switching**
```bash
# Clear context for new investigation
> /target none
> /clear

# Export findings before switching
> /export investigation-2026-03-15.json
```

### **Model Selection Strategy**
- **Quick checks:** gpt-4o-mini (fastest)
- **Rule compliance:** Phi-4 (most compliant)
- **Complex analysis:** GPT-4o (most capable)
- **Deep investigation:** DeepSeek-V3 (best reasoning)
- **Enterprise scenarios:** Llama-3.3-70B (best for business context)

---

## Need More Examples?

- **Specific use case not covered?** [Open an issue](https://github.com/jerisadeumai/zero-shield-cli/issues)
- **Want to contribute examples?** See [Contributing Guide](../../CONTRIBUTING.md)
- **Need help with commands?** Check [Command Reference](COMMANDS.md)

---

**Master incident response with AI-powered security operations! **