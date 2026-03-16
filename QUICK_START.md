# Quick Start Guide

Get Zero-Shield CLI running in under 5 minutes.

## Platform Compatibility

Zero-Shield CLI runs on all major platforms:

| Platform | Status | Notes |
|----------|--------|-------|
| **Windows** (10+) | ✅ Full Support | ANSI colors, msvcrt terminal I/O |
| **Linux/Unix** (Ubuntu 20.04+) | ✅ Full Support | Native POSIX, termios support |
| **macOS** (12+) | ✅ Full Support | Native terminal compatibility |
| **AWS CloudShell** | ✅ Recommended | Inherits IAM credentials automatically |

**Requirements:** Python 3.9+ (architecture agnostic)

---

## Choose Your Environment

| Environment | Time | AWS Credentials | Best For |
|-------------|------|-----------------|----------|
| **AWS CloudShell** | 2 min | Inherited | Production, testing |
| **Local Development** | 5 min | Required | Development, customization |

---

## AWS CloudShell (Recommended)

**Why CloudShell?** Inherits your AWS IAM role automatically - no credential management needed.

### Step 1: Upload File
1. Open [AWS CloudShell](https://console.aws.amazon.com/cloudshell/)
2. Upload `zero_shield_cli.py` using the upload button
3. Verify: `ls -la zero_shield_cli.py`

### Step 2: Configure Environment
```bash
# If you cloned the repository:
cp environments/cloudshell/.env.example .env

# If you only uploaded the main file, create .env manually:
nano .env
```

**Required configuration:**
```env
# GitHub Models API Token (Required)
GITHUB_TOKEN=your_github_personal_access_token_here

# Quarantine Security Group (Optional but recommended)
QUARANTINE_SG_ID=sg-your_quarantine_group_id_here

# AWS credentials NOT needed - inherited from CloudShell
```

### Step 3: Run
```bash
python3 zero_shield_cli.py
```

**First run will show:**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ███████╗███████╗██████╗  ██████╗       ███████╗██╗  ██╗██╗███████╗██╗     ██████╗  ║
║  ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗      ██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗ ║
║    ███╔╝ █████╗  ██████╔╝██║   ██║█████╗███████╗███████║██║█████╗  ██║     ██║  ██║ ║
║   ███╔╝  ██╔══╝  ██╔══██╗██║   ██║╚════╝╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║ ║
║  ███████╗███████╗██║  ██║╚██████╔╝      ███████║██║  ██║██║███████╗███████╗██████╔╝ ║
║  ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝       ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝  ║
║                                                                              ║
║                    Agentic AWS Security Copilot                              ║
║                    v2.0.0-dev (security-hardened)                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

⚡ OODA Loop: Observe → Orient → Decide → Act
Copyright © 2026 Jeri L3D | JeriSadeuM | MIT License

✓ AWS credentials: Configured
✓ GitHub token: Configured
✓ Models available: 5
✓ 32 AWS actions across 14 service categories

[Select a model to begin]
```

---

## Local Development

### Step 1: Clone Repository
```bash
git clone https://github.com/jerisadeumai/zero-shield-cli.git
cd zero-shield-cli
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
cp environments/local/.env.example .env
nano .env
```

**Required configuration:**
```env
# GitHub Models API Token (Required)
GITHUB_TOKEN=your_github_personal_access_token_here

# AWS Credentials (Required for local)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_DEFAULT_REGION=us-east-1

# Quarantine Security Group (Optional)
QUARANTINE_SG_ID=sg-your_quarantine_group_id_here
```

### Step 4: Run
```bash
python3 zero_shield_cli.py
```

---

## Docker

**Note:** Docker setup is planned for future release. Currently available: CloudShell and Local development.

---

## AWS IAM Setup (Required)

Zero-Shield requires specific AWS permissions. Choose the appropriate tier:

### Tier 1: Minimal (Read-Only Investigation)
**Use Case:** Security investigation, compliance auditing  
**Risk Level:** Very Low - No write operations

```bash
# Create and attach the minimal policy
aws iam create-policy \
  --policy-name ZeroShield-Minimal \
  --policy-document file://aws-setup/policies/zero-shield-minimal.json

aws iam attach-user-policy \
  --user-name YOUR_USERNAME \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/ZeroShield-Minimal
```

### Tier 2: Standard (Quarantine Capability) - Recommended
**Use Case:** Most security operations including incident response  
**Risk Level:** Medium - Can quarantine instances

```bash
# Create and attach the standard policy
aws iam create-policy \
  --policy-name ZeroShield-Standard \
  --policy-document file://aws-setup/policies/zero-shield-standard.json

aws iam attach-user-policy \
  --user-name YOUR_USERNAME \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/ZeroShield-Standard
```

### Tier 3: Full (Complete Incident Response)
**Use Case:** Complete incident response including IAM key deactivation  
**Risk Level:** Higher - Can deactivate IAM access keys

```bash
# Create and attach the full policy
aws iam create-policy \
  --policy-name ZeroShield-Full \
  --policy-document file://aws-setup/policies/zero-shield-full.json

aws iam attach-user-policy \
  --user-name YOUR_USERNAME \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/ZeroShield-Full
```

**For CloudShell users:** Attach the policy to your console user/role instead.

---

## Getting Required Tokens

### GitHub Personal Access Token
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. **Scopes:** No scopes needed (Zero-Shield uses GitHub Models API, not repository access)
4. Copy the token - you won't see it again!

### AWS Credentials (Local/Docker only)
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Option 3: IAM roles (recommended for EC2/Lambda)
# Attach IAM role with Zero-Shield policies
```

### Quarantine Security Group (Optional but Recommended)
Create a security group for quarantining compromised instances:

```bash
# Create quarantine security group
aws ec2 create-security-group \
  --group-name ZeroShield-Quarantine \
  --description "Quarantine zone for compromised instances - blocks all traffic"

# Get the security group ID
aws ec2 describe-security-groups \
  --group-names ZeroShield-Quarantine \
  --query 'SecurityGroups[0].GroupId' \
  --output text

# Add the sg-xxxxxxxx ID to your .env file as QUARANTINE_SG_ID
```

---

## Verify Installation

### Test Basic Functionality
```bash
# Start Zero-Shield
python3 zero_shield_cli.py

# Try these commands:
> list instances
> /status
> /help
> exit
```

### Expected Output
```
[ORIENT]: The user wants to see running EC2 instances...
[DECIDE]: I'll retrieve the current list of instances...
[ACT]:
[ACTION:LIST]
[OBSERVE]: EC2 Instances Found:
[1] i-0123456789abcdef0 MyWebServer (RUNNING)
[2] i-0987654321fedcba0 DatabaseServer (STOPPED)
```

---

## Troubleshooting

### "GITHUB_TOKEN not set"
```bash
# Check .env file exists and has token
cat .env | grep GITHUB_TOKEN

# Or export directly
export GITHUB_TOKEN=your_token_here
```

### "AWS credentials not found" (Local/Docker)
```bash
# Check AWS credentials
aws sts get-caller-identity

# If fails, configure:
aws configure
```

### "No instances found"
- Verify you're in the correct AWS region
- Check IAM permissions (see [IAM Setup Guide](aws-setup/IAM_POLICIES.md))
- Ensure you have EC2 instances in your account

### "State file corrupt"
```bash
# Delete session files and restart
rm session_state.json session_kg.json
python3 zero_shield_cli.py
```

---

## Next Steps

1. **[Command Reference](docs/user-guide/COMMANDS.md)** - Learn all available commands
2. **[Set up IAM Policies](aws-setup/IAM_POLICIES.md)** - Configure proper permissions
3. **[Try Example Commands](docs/user-guide/EXAMPLES.md)** - Real-world scenarios
4. **[Architecture Overview](docs/architecture/ARCHITECTURE.md)** - Technical details

---

## Need Help?

- **AWS Setup:** [IAM Policies Guide](aws-setup/IAM_POLICIES.md)
- **GitHub Issues:** [Report a Problem](https://github.com/jerisadeumai/zero-shield-cli/issues)

---

**You're ready to secure your AWS environment with AI! **


---

**Project Maintainer:** Jeri L3D | JeriSadeuM  
**Repository:** https://github.com/jerisadeumai/zero-shield-cli  
**Copyright © 2026 Jeri L3D | JeriSadeuM | All Rights Reserved**
