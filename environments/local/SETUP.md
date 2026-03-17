# Local Development Setup

> ⚠️ **DEVELOPMENT BRANCH**  
> Version: v2.0.0-dev | Status: Development Only | Last Updated: March 17, 2026  
> **Not recommended for production use. Use `main` branch for stable release.**

Set up Zero-Shield CLI on your local development machine.

## Prerequisites

- Python 3.9 or higher
- AWS CLI configured with credentials
- Git (for cloning repository)

## Installation

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

### Step 3: Configure Environment
```bash
cp environments/local/.env.example .env
```

Edit the `.env` file with your credentials:
```env
# GitHub Models API Token (Required)
GITHUB_TOKEN=your_github_personal_access_token_here

# AWS Credentials (Required for local development)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_DEFAULT_REGION=us-east-1

# Quarantine Security Group (Optional but recommended)
QUARANTINE_SG_ID=sg-your_quarantine_group_id_here
```

### Step 4: Set Up AWS IAM Permissions

Choose the appropriate policy tier for your needs:

**Option 1: Standard Policy (Recommended)**
```bash
aws iam create-policy \
  --policy-name ZeroShield-Standard \
  --policy-document file://aws-setup/policies/zero-shield-standard.json

aws iam attach-user-policy \
  --user-name YOUR_USERNAME \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/ZeroShield-Standard
```

See [IAM Policies Guide](../../aws-setup/IAM_POLICIES.md) for all policy options.

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

### Step 5: Run Zero-Shield
```bash
python3 zero_shield_cli.py
```

## Verification

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

### Run Test Suite
```bash
# Verify installation by running the complete test suite (canonical command)
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

### Test Categories Breakdown
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

## Troubleshooting

### "AWS credentials not found"
```bash
# Check AWS credentials
aws sts get-caller-identity

# If fails, configure:
aws configure
```

### "GITHUB_TOKEN not set"
```bash
# Check .env file
cat .env | grep GITHUB_TOKEN

# Or export directly
export GITHUB_TOKEN=your_token_here
```

### "No instances found"
- Verify you're in the correct AWS region
- Check IAM permissions
- Ensure you have EC2 instances in your account

## Development Features

Local development provides additional capabilities:

- **Code Editing**: Modify `zero_shield_cli.py` directly
- **Debug Mode**: Add print statements for troubleshooting
- **Custom Models**: Test different LLM configurations
- **Offline Testing**: Work with cached session data

## Next Steps

- [Read the User Guide](../../docs/user-guide/COMMANDS.md)
- [Try Example Commands](../../docs/user-guide/EXAMPLES.md)
- [Explore Architecture](../../docs/architecture/ARCHITECTURE.md)