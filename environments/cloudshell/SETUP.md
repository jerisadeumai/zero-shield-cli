# AWS CloudShell Setup Guide

> ⚠️ **DEVELOPMENT BRANCH**  
> Version: v2.0.0-dev | Status: Development Only | Last Updated: March 17, 2026  
> **Not recommended for production use. This branch contains features not yet in the main branch.**

Deploy Zero-Shield CLI in AWS CloudShell in under 2 minutes. CloudShell automatically inherits your AWS console permissions - no credential management needed!

## Why CloudShell?

 **No AWS credential setup** - inherits your console session 
 **Pre-installed Python 3.9+** - no dependency installation 
 **Secure environment** - temporary, isolated, auto-resets 
 **Internet access** - GitHub Models API works out of the box 
 **Persistent storage** - session files survive between sessions 

---

## Quick Setup (2 Minutes)

### Step 1: Open AWS CloudShell
1. Log into [AWS Console](https://console.aws.amazon.com/)
2. Click the CloudShell icon (terminal) in the top navigation bar
3. Wait for CloudShell to initialize (~30 seconds)

### Step 2: Upload Zero-Shield CLI
**Option A: Direct Upload (Recommended)**
1. Click the "Upload file" button in CloudShell
2. Select `zero_shield_cli.py` from your local machine
3. Wait for upload to complete

**Option B: Git Clone**
```bash
git clone https://github.com/jerisadeumai/zero-shield-cli.git
cd zero-shield-cli
```

**Option C: wget Download**
```bash
wget https://raw.githubusercontent.com/jerisadeumai/zero-shield-cli/agent-v2-dev/zero_shield_cli.py
```

### Step 3: Configure Environment
```bash
# Download CloudShell-specific environment template
wget https://raw.githubusercontent.com/jerisadeumai/zero-shield-cli/agent-v2-dev/environments/cloudshell/.env.example

# Copy to .env
cp .env.example .env

# Edit configuration
nano .env
```

### Dependencies Installed
The `pip install -r requirements.txt` command installs:
- **pytest>=7.0.0** - Test framework for running all 152 tests
- **hypothesis>=6.0.0** - Property-based testing library (44 tests)
- **pytest-xdist>=3.0.0** - Parallel test execution support
- Plus all core application dependencies

### About Property-Based Testing
Zero-Shield CLI includes 44 property-based tests using the Hypothesis library. These tests:
- Generate hundreds of random inputs automatically
- Verify system behavior holds universally (not just specific examples)
- Provide mathematical correctness guarantees
- Catch edge cases that unit tests miss

Property-based tests validate critical properties like:
- Session state survives encryption/decryption cycles
- Credential redaction works on all possible inputs
- AWS resource sanitization prevents all injection attacks

### Test Troubleshooting

**Common Issues:**
- **"No module named pytest"** → Run `pip install -r requirements.txt`
- **"No module named hypothesis"** → Run `pip install -r requirements.txt`
- **"4 tests skipped"** → Normal on Windows (file permission tests)
- **"Tests taking too long"** → Use `python3 -m pytest tests/ -v -n auto` for parallel execution
- **"Property tests failing"** → Check hypothesis>=6.0.0 is installed

**Getting Help:**
- Check [validation/TEST_REPORTS.md](../../validation/TEST_REPORTS.md) for detailed test information
- Review [VALIDATION_TEST_SUITE.md](../../VALIDATION_TEST_SUITE.md) for property-based testing guide
- Open an issue at [GitHub Issues](https://github.com/jerisadeumai/zero-shield-cli/issues)

**Required configuration:**
```env
# GitHub Models API Token (REQUIRED)
GITHUB_TOKEN=your_github_personal_access_token_here

# Quarantine Security Group (OPTIONAL but recommended)
QUARANTINE_SG_ID=sg-your_quarantine_group_id_here
```

### Validate Installation (Recommended)
Run the complete test suite to verify everything works:
```bash
# Run all 152 tests (canonical command)
python3 -m pytest tests/ -v
```
**Expected Result:** 152 tests collected, 148 passed, 4 skipped (97.4% pass rate)

### Understanding Test Results
When you run `python3 -m pytest tests/ -v`, you should see:

```
================================= test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.0.0 -- python3
cachedir: .pytest_cache
rootdir: /home/cloudshell-user/zero-shield-cli
collected 152 tests

tests/test_action_detection.py::test_action_detection_basic PASSED                [ 5%]
tests/test_comprehensive_e2e.py::test_ec2_instance_listing PASSED                [15%]
tests/test_property_final_batch.py::TestProperty16ModelSelectionValidation::test_out_of_range_model_numbers_rejected PASSED [55%]
tests/test_security_fixes.py::test_file_permissions_unix PASSED                  [97%]
=============================== 152 passed, 0 skipped in 12.45s ===============================
```

**Test Breakdown:**
- **8 action detection tests** - Action parsing and validation
- **66 comprehensive tests** - All functionality, edge cases, integration
- **35 security tests** - Credential redaction, HITL, encryption
- **44 property-based tests** - Universal correctness properties

### Platform-Specific Test Behavior

**AWS CloudShell (linux platform):**
- **All 152 tests RUN** - Full test suite execution
- **Environment**: Amazon Linux 2 with Python 3.9.16
- **File permission tests**: Execute normally using chmod/stat system calls
- **Expected result**: 152 passed, 0 skipped (100% pass rate)

**Windows (win32 platform):**
- **4 tests SKIPPED** - Unix file permission tests (expected behavior)
- **Reason**: Windows uses ACL (Access Control Lists) instead of Unix file permissions (chmod 0600)
- **Affected tests**: `test_file_permissions_unix`, `test_session_file_permissions`, `test_kg_file_permissions`, `test_atomic_write_permissions`
- **Impact**: No functionality loss - Windows file security handled differently
- **Expected result**: 148 passed, 4 skipped (97.4% pass rate)

**Linux/Unix (linux platform):**
- **All 152 tests RUN** - Full test suite execution
- **File permission tests**: Execute normally using chmod/stat system calls
- **Expected result**: 152 passed, 0 skipped (100% pass rate)

**macOS (darwin platform):**
- **All 152 tests RUN** - Full test suite execution (same as Linux)
- **File permission tests**: Execute normally using Unix-style permissions
- **Expected result**: 152 passed, 0 skipped (100% pass rate)

### Step 4: Run Zero-Shield
```bash
python3 zero_shield_cli.py
```

**Expected startup output:**
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

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quick Start Guide
  1. Select a model below
  2. Ask plain-English questions - Zero-Shield calls tools automatically
  3. Type /help for all commands

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ AWS credentials: Inherited from CloudShell
✓ GitHub token: Configured
✓ Models available: 5 (gpt-4o-mini, Llama-3.3-70B-Instruct, Phi-4, DeepSeek-V3, gpt-4o)
✓ 32 AWS actions across 14 service categories

[Model Selection]
  1. gpt-4o-mini (128K context, fast & efficient)
  2. Llama-3.3-70B-Instruct (131K context, enterprise reasoning)
  3. Phi-4 (16K context, highly compliant)
  4. DeepSeek-V3 (65K context, deep reasoning)
  5. gpt-4o (128K context, most capable)

  Model (1-5):
```

---

## Getting Your GitHub Token

### Create GitHub Personal Access Token
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. **Name:** `Zero-Shield CLI`
4. **Expiration:** Choose appropriate duration (90 days recommended)
5. **Scopes:** 
 - For public repos: No scopes needed
 - For private repos: Check `repo`
6. Click "Generate token"
7. **Copy the token immediately** - you won't see it again!

### Add Token to Environment
```bash
# Edit .env file
nano .env

# Add your token:
GITHUB_TOKEN=ghp_your_actual_token_here_1234567890abcdef

# Save and exit (Ctrl+X, Y, Enter)
```

---

## Setting Up Quarantine Security Group (Optional)

Create a security group for quarantining compromised instances:

```bash
# Create quarantine security group
aws ec2 create-security-group \
 --group-name "ZeroShield-Quarantine" \
 --description "Quarantine zone for compromised instances - blocks all traffic"

# Note the security group ID from output (sg-xxxxxxxxx)
# Example output: "GroupId": "sg-0123456789abcdef0"

# Remove default outbound rule (allows all traffic)
aws ec2 revoke-security-group-egress \
 --group-id sg-0123456789abcdef0 \
 --protocol all \
 --port all \
 --cidr 0.0.0.0/0

# Add minimal outbound rules for logging (optional)
aws ec2 authorize-security-group-egress \
 --group-id sg-0123456789abcdef0 \
 --protocol tcp \
 --port 443 \
 --cidr 0.0.0.0/0

# Add the security group ID to .env
echo "QUARANTINE_SG_ID=sg-0123456789abcdef0" >> .env
```

---

## Test Your Setup

### Basic Functionality Test
```bash
# Start Zero-Shield
python3 zero_shield_cli.py

# Try these commands:
> list instances
> /status 
> /help
> exit
```

### Post-Deployment Test Verification
```bash
# If you cloned the full repository, run the test suite (canonical command)
python3 -m pytest tests/ -v

# Expected output: 152 tests collected, 148 passed, 4 skipped
# Pass rate: 97.4% (4 Windows file permission tests skipped)
```

**Expected test output:**
```
================================= test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.0.0 -- python3
cachedir: .pytest_cache
rootdir: /home/cloudshell-user/zero-shield-cli
collected 152 tests

tests/test_action_detection.py::test_action_detection_basic PASSED                [ 5%]
tests/test_comprehensive_e2e.py::test_ec2_instance_listing PASSED                [15%]
tests/test_property_final_batch.py::TestProperty16ModelSelectionValidation::test_out_of_range_model_numbers_rejected PASSED [55%]
tests/test_security_fixes.py::test_file_permissions_unix PASSED                  [97%]
=============================== 152 passed, 0 skipped in 12.45s ===============================
```

### Expected Test Results
```bash
# Command: list instances
[ORIENT]: The user wants to see running EC2 instances...
[DECIDE]: I'll retrieve the current list of instances...
[ACT]:
[ACTION:LIST]
[OBSERVE]: EC2 Instances Found:
[1] i-0123456789abcdef0 MyWebServer (RUNNING)
[2] i-0987654321fedcba0 DatabaseServer (STOPPED)

# Command: /status
┌─ System Status ──────────────────────────────────────────────────────────────┐
│ AWS Region: us-east-1 │
│ Active Target: None │
│ Session Files: Encrypted ✓ │
│ Models Available: 5/5 │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## CloudShell-Specific Features

### Automatic AWS Integration
- **Credentials:** Inherited from your AWS console session
- **Region:** Uses your console's current region
- **Permissions:** Same as your console user/role
- **MFA:** Inherits your console MFA session

### File Persistence
```bash
# Session files persist between CloudShell sessions
ls -la session_*.json
-rw------- 1 cloudshell-user cloudshell-user 1234 Mar 15 10:30 session_state.json
-rw------- 1 cloudshell-user cloudshell-user 5678 Mar 15 10:30 session_kg.json

# Files are automatically encrypted using your GITHUB_TOKEN
```

### Environment Management
```bash
# Check current AWS identity
aws sts get-caller-identity

# Check available regions
aws ec2 describe-regions --query 'Regions[].RegionName' --output table

# Switch regions (affects Zero-Shield operations)
export AWS_DEFAULT_REGION=us-west-2
```

---

## Troubleshooting

### "GITHUB_TOKEN not set" Error
```bash
# Check if .env file exists and has token
cat .env | grep GITHUB_TOKEN

# If empty or missing, edit .env:
nano .env
# Add: GITHUB_TOKEN=your_actual_token_here
```

### "No instances found" Message
```bash
# Check current region
aws configure get region
echo $AWS_DEFAULT_REGION

# List instances in current region
aws ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,Name:Tags[?Key==`Name`].Value|[0],State:State.Name}'

# If no instances, try different region:
export AWS_DEFAULT_REGION=us-west-2
python3 zero_shield_cli.py
```

### "Access Denied" Errors
```bash
# Check your AWS permissions
aws sts get-caller-identity

# Test specific permissions
aws ec2 describe-instances --max-items 1
aws iam list-users --max-items 1

# If access denied, your AWS user/role needs additional permissions
# See: ../../aws-setup/IAM_POLICIES.md
```

### "State file corrupt" Error
```bash
# Delete corrupted session files
rm session_state.json session_kg.json

# Restart Zero-Shield
python3 zero_shield_cli.py
```

### CloudShell Session Timeout
```bash
# CloudShell sessions timeout after ~20 minutes of inactivity
# Your files persist, but you need to restart Zero-Shield

# Check if files exist
ls -la zero_shield_cli.py .env session_*.json

# Restart
python3 zero_shield_cli.py
```

---

## Next Steps

### Learn Zero-Shield Commands
```bash
# Start Zero-Shield and try these:
> /help # Show all commands
> list instances # See your EC2 instances
> /target i-0123456789abcdef0 # Set active instance
> inspect instance # Get detailed info
> check its security groups # Analyze security
> what vpc is it in? # VPC information
```

### Explore Advanced Features
- **[Command Reference](../../docs/user-guide/COMMANDS.md)** - All available commands
- **[Example Scenarios](../../docs/user-guide/EXAMPLES.md)** - Real-world use cases
- **[Architecture Overview](../../docs/architecture/ARCHITECTURE.md)** - Technical details

### Set Up Proper IAM Permissions
- **[IAM Policies Guide](../../aws-setup/IAM_POLICIES.md)** - Detailed permission setup
- **[Security Best Practices](../../aws-setup/IAM_POLICIES.md#security-best-practices)** - Secure configuration

---

## Need Help?

- **CloudShell Issues:** [AWS CloudShell Documentation](https://docs.aws.amazon.com/cloudshell/)
- **Zero-Shield Issues:** [GitHub Issues](https://github.com/jerisadeumai/zero-shield-cli/issues)
- **AWS Permissions:** [IAM Setup Guide](../../aws-setup/IAM_POLICIES.md)

---

## You're Ready!

Your AWS CloudShell environment is now configured for Zero-Shield CLI. You can:

 Investigate security incidents with natural language 
 Quarantine compromised instances instantly 
 Analyze AWS resources across 14 services 
 Use 5 different AI models for optimal results 
 Maintain persistent investigation context 

**Start securing your AWS environment with AI! **