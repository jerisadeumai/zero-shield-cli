# Quick Start Guide

> ⚠️ **DEVELOPMENT BRANCH WARNING**  
> This guide covers the `agent-v2-dev` development branch. For production deployment, use the stable `main` branch.

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
platform win32 -- Python 3.11.0, pytest-7.4.0, pluggy-1.0.0 -- python.exe
cachedir: .pytest_cache
rootdir: C:\path\to\zero-shield-cli
collected 152 tests

tests/test_action_detection.py::test_action_detection_basic PASSED                [ 5%]
tests/test_comprehensive_e2e.py::test_ec2_instance_listing PASSED                [15%]
tests/test_property_final_batch.py::TestProperty16ModelSelectionValidation::test_out_of_range_model_numbers_rejected PASSED [55%]
tests/test_security_fixes.py::test_file_permissions_unix SKIPPED (File permissions t...) [97%]
=============================== 148 passed, 4 skipped in 16.80s ===============================
```

**Test Breakdown:**
- **8 action detection tests** - Action parsing and validation
- **66 comprehensive tests** - All functionality, edge cases, integration
- **35 security tests** - Credential redaction, HITL, encryption
- **44 property-based tests** - Universal correctness properties
- **4 skipped tests** - Windows file permission tests (expected on Windows)

### Platform-Specific Test Behavior

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

**AWS CloudShell (linux platform):**
- **All 152 tests RUN** - Full test suite execution
- **Environment**: Amazon Linux 2 with Python 3.9.16
- **Expected result**: 152 passed, 0 skipped (100% pass rate)

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

### Dependencies Installed
The `pip install -r requirements.txt` command installs:
- **pytest>=7.0.0** - Test framework for running all 152 tests
- **hypothesis>=6.0.0** - Property-based testing library (44 tests)
- **pytest-xdist>=3.0.0** - Parallel test execution support
- Plus all core application dependencies (openai, boto3, python-dotenv, httpx)

### About pytest Testing Framework
Zero-Shield CLI uses pytest as its primary testing framework. After installation via `pip install -r requirements.txt`, you can run the complete test suite with:

```bash
# Run all 152 tests (canonical command)
python3 -m pytest tests/ -v
```

This command:
- Discovers all test files in the `tests/` directory
- Runs 152 tests across 4 categories (8 action + 66 comprehensive + 35 security + 44 property-based)
- Provides verbose output showing each test result
- Expected result: 148 passed, 4 skipped (97.4% pass rate)

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

### Validate Installation (Recommended)
Run the complete test suite to verify everything works:
```bash
python3 -m pytest tests/ -v
```
**Expected Result:** 152 tests collected, 148 passed, 4 skipped (97.4% pass rate)

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

### Run Test Suite
```bash
# Verify installation by running tests
python3 -m pytest tests/ -v

# Expected output: 152 tests collected, 148 passed, 4 skipped
# Pass rate: 97.4% (4 Windows file permission tests skipped)
```

**Expected test output:**
```
================================= test session starts =================================
platform win32 -- Python 3.11.0, pytest-7.4.0, pluggy-1.0.0 -- python.exe
cachedir: .pytest_cache
rootdir: C:\path\to\zero-shield-cli
collected 152 tests

tests/test_action_detection.py::test_action_detection_basic PASSED                [ 5%]
tests/test_comprehensive_e2e.py::test_ec2_instance_listing PASSED                [15%]
tests/test_property_final_batch.py::TestProperty16ModelSelectionValidation::test_out_of_range_model_numbers_rejected PASSED [55%]
tests/test_security_fixes.py::test_file_permissions_unix SKIPPED (File permissions t...) [97%]
=============================== 148 passed, 4 skipped in 16.80s ===============================
```

### Test Breakdown Verification
```bash
# Check test collection
python3 -m pytest tests/ --collect-only -q
# Shows: 152 tests collected in 2.76s

# Test breakdown:
#   Action detection tests: 8
#   Comprehensive E2E tests: 66  
#   Security tests: 35
#   Property-based tests: 44 (across 6 files)
#   Total: 152 tests
#
# Pass rate: 97.4% (148 passing, 4 skipped on Windows)
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

## Verify Installation

### Step 1: Install All Dependencies
```bash
pip install -r requirements.txt
```
This installs pytest, hypothesis, pytest-xdist, and all core dependencies.

### Step 2: Run Complete Test Suite
```bash
python3 -m pytest tests/ -v
```
**Expected Output:**
- 152 tests collected
- 148 passed, 4 skipped
- Pass rate: 97.4%
- Test categories: 8 action detection + 66 comprehensive + 35 security + 44 property-based

### Step 3: Verify Test Breakdown
```bash
python3 -m pytest tests/ --collect-only -q
```
Should show exactly 152 tests discovered.

### Step 4: Run Application
```bash
python3 zero_shield_cli.py
```
Should start successfully with model selection menu.

### Troubleshooting Tests
If tests fail:
1. **Missing dependencies:** Run `pip install -r requirements.txt` again
2. **Environment issues:** Check your .env file configuration
3. **Windows file permission tests:** 4 tests expected to skip on Windows (normal)
4. **Hypothesis tests:** Require hypothesis>=6.0.0 (installed via requirements.txt)

### Test Troubleshooting

**Common Issues:**
- **"No module named pytest"** → Run `pip install -r requirements.txt`
- **"No module named hypothesis"** → Run `pip install -r requirements.txt`
- **"4 tests skipped"** → Normal on Windows (file permission tests)
- **"Tests taking too long"** → Use `python3 -m pytest tests/ -v -n auto` for parallel execution
- **"Property tests failing"** → Check hypothesis>=6.0.0 is installed

**Getting Help:**
- Check [validation/TEST_REPORTS.md](validation/TEST_REPORTS.md) for detailed test information
- Review [VALIDATION_TEST_SUITE.md](VALIDATION_TEST_SUITE.md) for property-based testing guide
- Open an issue at [GitHub Issues](https://github.com/jerisadeumai/zero-shield-cli/issues)

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
