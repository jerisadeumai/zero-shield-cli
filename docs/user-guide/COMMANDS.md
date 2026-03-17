# Zero-Shield CLI Command Reference

> ⚠️ **DEVELOPMENT BRANCH**  
> Version: v2.0.0-dev | Status: Development Only | Last Updated: March 17, 2026  
> **This branch contains features not yet in the main branch.**

Complete reference for all AWS actions and system commands available in Zero-Shield CLI.

**Specification Compliance:** This command reference is validated against the [comprehensive specification](.kiro/specs/zero-shield-cli-comprehensive-spec/) with 50 requirements, 44 correctness properties, and 152 tests (97.4% pass rate). All 32 AWS actions are formally specified and property-tested.

**Note:** All example resource IDs (like `i-0123456789abcdef0`, `sg-041a97ba55afb006e`) are placeholders. Replace them with your actual AWS resource IDs.

## System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/switch` | Change LLM model | `/switch` → select from 5 models |
| `/status` | Show system status | `/status` → quotas, cooldowns, active target |
| `/target <id>` | Set active resource | `/target i-0123456789abcdef0` |
| `/clear` | Clear chat history | `/clear` → fresh conversation |
| `/export` | Export Knowledge Graph | `/export` → save investigation data |
| `/reset` | Reset all state | `/reset` → clear everything, start fresh |
| `/help` | Show help | `/help` → command reference |
| `exit` | Exit Zero-Shield | `exit` → quit application |

---

## AWS Actions by Service

### EC2 & Networking (9 Actions)

#### **LIST** - List EC2 Instances
**Natural Language:** `"What instances are currently running?"`, `"Show me all EC2 instances"`
**Action Format:** `[ACTION:LIST]`
**Returns:** Instance ID, Name, State, Type, Public/Private IPs, Security Groups

**Example Output:**
```
[OBSERVE]: EC2 Instances Found:
[1] i-0123456789abcdef0 WebServer-Prod (RUNNING) | t3.medium | 3.239.105.195
[2] i-0987654321fedcba0 Database-Main (STOPPED) | r5.large | No Public IP
```

#### **INSPECT** - Detailed Instance Information 
**Natural Language:** `"Inspect instance i-0123456789abcdef0"`, `"Tell me about this instance"`
**Action Format:** `[ACTION:INSPECT:i-0123456789abcdef0]`
**Returns:** Complete instance metadata, VPC, subnet, security groups, IAM role

**Example Output:**
```
Instance: i-0123456789abcdef0 | Name: WebServer-Prod | State: running
VPC: vpc-0fa1a386cc9ed95b7 | Subnet: subnet-02ce73a728f3cfaf7
Type: t3.medium | AMI: ami-0abcdef1234567890
Public IP: 3.239.105.195 | Private IP: 172.31.9.39
Security Groups: sg-041a97ba55afb006e (WebServer-SG)
IAM Role: EC2-WebServer-Role
```

#### **SG_RULES** - Security Group Rules Analysis
**Natural Language:** `"Check security group rules"`, `"What ports are open?"`
**Action Format:** `[ACTION:SG_RULES:sg-041a97ba55afb006e]`
**Returns:** Inbound/outbound rules, risk assessment, public exposure analysis

**Example Output:**
```
Security Group: sg-041a97ba55afb006e (WebServer-SG)
INBOUND RULES:
✓ HTTP (80) from 0.0.0.0/0 - PUBLIC ACCESS
✓ HTTPS (443) from 0.0.0.0/0 - PUBLIC ACCESS 
⚠ SSH (22) from 0.0.0.0/0 - RISKY: SSH open to internet
OUTBOUND RULES:
✓ All traffic to 0.0.0.0/0 - Standard web server config
```

#### **VPC_INFO** - VPC Configuration Details
**Natural Language:** `"What VPC is this in?"`, `"Show me VPC information"`
**Action Format:** `[ACTION:VPC_INFO:vpc-0fa1a386cc9ed95b7]`
**Returns:** VPC CIDR, subnets, route tables, internet gateway status

#### **EC2_VOLUMES** - EBS Volumes and Snapshots
**Natural Language:** `"Show me EBS volumes"`, `"What storage is attached?"`
**Action Format:** `[ACTION:EC2_VOLUMES]`
**Returns:** Volume IDs, sizes, encryption status, attachment info

#### **EC2_KEYPAIRS** - SSH Key Pair Inventory
**Natural Language:** `"List SSH key pairs"`, `"What keys are available?"`
**Action Format:** `[ACTION:EC2_KEYPAIRS]`
**Returns:** Key pair names, fingerprints, creation dates

#### **NETWORK_ACLS** - Network ACL Rules
**Natural Language:** `"Check network ACLs"`, `"Show me subnet-level security"`
**Action Format:** `[ACTION:NETWORK_ACLS]`
**Returns:** NACL rules, subnet associations, allow/deny patterns

#### **QUARANTINE** - Isolate Compromised Instance
**Natural Language:** `"This instance is compromised, isolate it"`, `"Quarantine this instance"`
**Action Format:** `[ACTION:QUARANTINE:i-0123456789abcdef0]`
**Security:** Requires HITL confirmation - must type full instance ID
**Effect:** Moves instance to quarantine security group (blocks all traffic)

#### **MODIFY_SG** - Change Instance Security Groups
**Natural Language:** `"Change security groups"`, `"Move to different security group"`
**Action Format:** `[ACTION:MODIFY_SG:i-0123456789abcdef0:sg-newgroupid]`
**Security:** Requires HITL confirmation - must type full instance ID

---

### IAM (5 Actions)

#### **IAM_USERS** - List IAM Users with MFA Status
**Natural Language:** `"Show me IAM users"`, `"Who doesn't have MFA enabled?"`
**Action Format:** `[ACTION:IAM_USERS]`
**Returns:** Username, MFA status, last activity, access key age

**Example Output:**
```
IAM Users Found:
[1] john.doe - MFA: ✓ Enabled | Last Activity: 2 days ago | Keys: 1 active
[2] service-account - MFA: ✗ Not Enabled | Last Activity: 1 hour ago | Keys: 2 active
⚠ WARNING: service-account has no MFA - security risk
```

#### **IAM_ROLES** - List IAM Roles and Trust Policies
**Natural Language:** `"Show me IAM roles"`, `"What roles exist?"`
**Action Format:** `[ACTION:IAM_ROLES]`
**Returns:** Role names, trust relationships, attached policies

#### **IAM_ACCESS_KEYS** - Audit Access Key Ages
**Natural Language:** `"Show me old access keys"`, `"Which keys need rotation?"`
**Action Format:** `[ACTION:IAM_ACCESS_KEYS]`
**Returns:** Key IDs, ages, last used dates, rotation recommendations

#### **IAM_CHECK** - Instance IAM Profile Analysis
**Natural Language:** `"What IAM role does this instance have?"`, `"Check instance permissions"`
**Action Format:** `[ACTION:IAM_CHECK:i-0123456789abcdef0]`
**Returns:** Attached IAM role, policies, effective permissions

#### **DEACTIVATE_ACCESS_KEY** - Disable Compromised Keys
**Natural Language:** `"Deactivate this access key"`, `"Disable compromised key"`
**Action Format:** `[ACTION:DEACTIVATE_ACCESS_KEY:AKIAIOSFODNN7EXAMPLE]`
**Security:** Requires HITL confirmation - must type full access key ID
**Effect:** Sets access key status to "Inactive"

---

### Storage & Database (5 Actions)

#### **S3_BUCKETS** - List S3 Buckets with Public Access Status
**Natural Language:** `"Show me S3 buckets"`, `"Which buckets are public?"`
**Action Format:** `[ACTION:S3_BUCKETS]`
**Returns:** Bucket names, public access status, encryption, versioning

**Example Output:**
```
S3 Buckets Found:
[1] my-private-bucket - ✓ Private | Encryption: AES256 | Versioning: Enabled
[2] public-website-assets - ⚠ PUBLIC READ | Encryption: None | Versioning: Disabled
[3] backup-storage - ✓ Private | Encryption: KMS | Versioning: Enabled
```

#### **S3_BUCKET_POLICY** - Get Bucket Policies and ACLs
**Natural Language:** `"Show me bucket policy"`, `"What permissions does this bucket have?"`
**Action Format:** `[ACTION:S3_BUCKET_POLICY:my-bucket-name]`
**Returns:** Bucket policy JSON, ACL settings, public access analysis

#### **RDS_INSTANCES** - List RDS Database Instances
**Natural Language:** `"Show me databases"`, `"What RDS instances are running?"`
**Action Format:** `[ACTION:RDS_INSTANCES]`
**Returns:** DB identifiers, engine types, sizes, public accessibility

#### **DYNAMODB_TABLES** - List DynamoDB Tables
**Natural Language:** `"Show me DynamoDB tables"`, `"What NoSQL databases exist?"`
**Action Format:** `[ACTION:DYNAMODB_TABLES]`
**Returns:** Table names, item counts, read/write capacity, encryption

#### **EFS_FILESYSTEMS** - List EFS Filesystems
**Natural Language:** `"Show me EFS filesystems"`, `"What shared storage exists?"`
**Action Format:** `[ACTION:EFS_FILESYSTEMS]`
**Returns:** Filesystem IDs, sizes, mount targets, encryption status

---

### Security Services (3 Actions)

#### **GUARDDUTY_FINDINGS** - High/Medium Severity Findings
**Natural Language:** `"Show me GuardDuty findings"`, `"What threats were detected?"`
**Action Format:** `[ACTION:GUARDDUTY_FINDINGS]`
**Returns:** Finding types, severity levels, affected resources, timestamps

**Example Output:**
```
GuardDuty Findings (Last 24 hours):
[HIGH] UnauthorizedAPICall - Instance i-0123456789abcdef0
 └ Unusual API calls from this instance at 2026-03-15 10:30 UTC
[MEDIUM] Recon:EC2/PortProbeUnprotectedPort - Instance i-0987654321fedcba0 
 └ Port scanning detected from 203.0.113.1 at 2026-03-15 09:15 UTC
```

#### **KMS_KEYS** - List KMS Keys with Rotation Status
**Natural Language:** `"Show me KMS keys"`, `"Which keys need rotation?"`
**Action Format:** `[ACTION:KMS_KEYS]`
**Returns:** Key IDs, aliases, rotation status, usage

#### **WAF_WEBACLS** - List WAFv2 Web ACLs
**Natural Language:** `"Show me WAF rules"`, `"What web application firewalls exist?"`
**Action Format:** `[ACTION:WAF_WEBACLS]`
**Returns:** WebACL names, associated resources, rule counts

---

### Monitoring & Logging (3 Actions)

#### **CLOUDWATCH_LOGS** - Stream Log Events
**Natural Language:** `"Show me CloudWatch logs"`, `"What's in the application logs?"`
**Action Format:** `[ACTION:CLOUDWATCH_LOGS:log-group-name]`
**Returns:** Recent log events, timestamps, log streams

#### **CLOUDWATCH_ALARMS** - List CloudWatch Alarms
**Natural Language:** `"Show me CloudWatch alarms"`, `"What alerts are configured?"`
**Action Format:** `[ACTION:CLOUDWATCH_ALARMS]`
**Returns:** Alarm names, states, metrics, thresholds

#### **EC2_METRICS** - CPU and Network Metrics
**Natural Language:** `"Show me CPU usage"`, `"What's the network traffic?"`
**Action Format:** `[ACTION:EC2_METRICS:i-0123456789abcdef0]`
**Returns:** CPU utilization, network in/out, disk I/O

---

### Audit & Cost (3 Actions)

#### **CLOUDTRAIL** - Management Events Lookup
**Natural Language:** `"Show me CloudTrail events"`, `"Who made changes recently?"`
**Action Format:** `[ACTION:CLOUDTRAIL]`
**Returns:** Recent API calls, user names, source IPs, timestamps

**Example Output:**
```
CloudTrail Events (Last 6 hours):
[2026-03-15 14:30] john.doe@company.com - ModifyInstanceAttribute (i-0123456789abcdef0)
 └ Source: 203.0.113.50 | User Agent: aws-cli/2.1.34
[2026-03-15 13:45] service-account - CreateSecurityGroup (sg-0newgroupid)
 └ Source: 10.0.1.100 | User Agent: Boto3/1.26.137
```

#### **COST_INSIGHT** - EC2 Instance Cost Estimation
**Natural Language:** `"What does this instance cost?"`, `"Estimate monthly cost"`
**Action Format:** `[ACTION:COST_INSIGHT:i-0123456789abcdef0]`
**Returns:** Hourly rate, monthly estimate, cost breakdown

#### **COST_EXPLORER** - 7-Day Spend Breakdown
**Natural Language:** `"Show me recent spending"`, `"What's my AWS bill?"`
**Action Format:** `[ACTION:COST_EXPLORER]`
**Returns:** Daily costs, service breakdown, spending trends

---

### Serverless (1 Action)

#### **LAMBDA_FUNCTIONS** - List Lambda Functions
**Natural Language:** `"Show me Lambda functions"`, `"What serverless functions exist?"`
**Action Format:** `[ACTION:LAMBDA_FUNCTIONS]`
**Returns:** Function names, runtimes, memory, last modified

---

## Command Patterns & Tips

### **Targeting Resources**
```bash
# Set active target first
/target i-0123456789abcdef0

# Then use context-aware commands
inspect instance # Uses active target
check its security groups # Uses active target 
what vpc is it in? # Uses active target

# Or specify directly
inspect instance i-0123456789abcdef0
```

### **Natural Language Flexibility**
```bash
# These all work the same way:
"Show me running instances"
"List EC2 instances" 
"What instances are currently running?"
"Display all virtual machines"
```

### **Model-Specific Behavior**
- **Phi-4:** Most compliant, best for rule audits
- **GPT-4o:** Most capable, handles complex scenarios
- **Llama-3.3-70B:** Best reasoning, good for investigations
- **DeepSeek-V3:** Deep analysis, good for root cause
- **gpt-4o-mini:** Fastest, good for simple queries

### **OODA Loop Understanding**
Every command follows the OODA pattern:
```
[ORIENT]: Understanding your request...
[DECIDE]: Determining best action...
[ACT]: Executing [ACTION:COMMAND]
[OBSERVE]: Results from AWS API...
```

### **Error Handling**
- **"Access Denied"** → Check IAM permissions
- **"Resource not found"** → Verify resource ID/region
- **"Rate limited"** → Wait for cooldown period
- **"Invalid target"** → Use `/target` to set valid resource

---

## Security Commands (HITL Required)

These commands require Human-in-the-Loop confirmation:

### **QUARANTINE** 
- **Prompt:** `"Type the instance ID to confirm quarantine:"`
- **Must type:** Full instance ID (e.g., `i-0123456789abcdef0`)
- **Effect:** Moves instance to quarantine security group

### **MODIFY_SG**
- **Prompt:** `"Type the instance ID to confirm security group change:"`
- **Must type:** Full instance ID
- **Effect:** Changes instance security groups

### **DEACTIVATE_ACCESS_KEY**
- **Prompt:** `"Type the access key ID to confirm deactivation:"`
- **Must type:** Full access key ID (e.g., `AKIAIOSFODNN7EXAMPLE`)
- **Effect:** Deactivates IAM access key

---

## Need Help?

- **Missing permissions?** See [IAM Setup Guide](../../aws-setup/IAM_POLICIES.md)
- **Want examples?** Check [Usage Examples](EXAMPLES.md)

---

**Master all 32 AWS actions with natural language!**