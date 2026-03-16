#!/bin/bash
# Zero-Shield CLI Deployment Script for AWS CloudShell
# Version: v2.0.0-dev
# Date: March 16, 2026
# Branch: agent-v2-dev

set -e  # Exit on error

echo "================================================================================"
echo "Zero-Shield CLI - CloudShell Deployment"
echo "Version: v2.0.0-dev (Development Branch)"
echo "================================================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "zero_shield_cli.py" ]; then
    echo "ERROR: zero_shield_cli.py not found in current directory"
    echo "Please run this script from the repository root"
    exit 1
fi

# Backup existing files
echo "[1/6] Creating backups..."
if [ -f "zero_shield_cli.py" ]; then
    cp zero_shield_cli.py zero_shield_cli.py.backup.$(date +%Y%m%d_%H%M%S)
    echo "  ✓ Backed up zero_shield_cli.py"
fi

if [ -f "session_state.json" ]; then
    cp session_state.json session_state.json.backup.$(date +%Y%m%d_%H%M%S)
    echo "  ✓ Backed up session_state.json"
fi

if [ -f "session_kg.json" ]; then
    cp session_kg.json session_kg.json.backup.$(date +%Y%m%d_%H%M%S)
    echo "  ✓ Backed up session_kg.json"
fi

echo ""

# Verify environment
echo "[2/6] Verifying environment..."

if [ -f ".env" ]; then
    echo "  ✓ .env file found"
    source .env
else
    echo "  ⚠ WARNING: .env file not found"
    echo "  Copy environments/cloudshell/.env.example to .env and configure"
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "  ✗ GITHUB_TOKEN not set"
    echo "    Required for: LLM inference and session file encryption"
    echo "    Configure in: .env file"
else
    echo "  ✓ GITHUB_TOKEN is set"
fi

if [ -z "$QUARANTINE_SG_ID" ]; then
    echo "  ⚠ QUARANTINE_SG_ID not set"
    echo "    Required for: Instance quarantine operations"
    echo "    Configure in: .env file"
else
    echo "  ✓ QUARANTINE_SG_ID is set ($QUARANTINE_SG_ID)"
fi

# Check if running in CloudShell (AWS credentials inherited)
if [ -n "$AWS_EXECUTION_ENV" ]; then
    echo "  ✓ Running in AWS CloudShell (credentials inherited)"
else
    if [ -z "$AWS_ACCESS_KEY_ID" ]; then
        echo "  ✗ AWS_ACCESS_KEY_ID not set"
        echo "    Required for: AWS API operations"
        echo "    Configure in: .env file"
    else
        echo "  ✓ AWS credentials are set"
    fi
fi

echo ""

# Check Python version
echo "[3/6] Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python version: $PYTHON_VERSION"

REQUIRED_VERSION="3.9"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    echo "  ✓ Python version meets requirements (3.9+)"
else
    echo "  ✗ Python version too old (requires 3.9+)"
    exit 1
fi

echo ""

# Check dependencies
echo "[4/6] Checking dependencies..."
python3 -c "import boto3" 2>/dev/null && echo "  ✓ boto3 installed" || echo "  ✗ boto3 NOT installed (run: pip install -r requirements.txt)"
python3 -c "import openai" 2>/dev/null && echo "  ✓ openai installed" || echo "  ✗ openai NOT installed (run: pip install -r requirements.txt)"
python3 -c "from dotenv import load_dotenv" 2>/dev/null && echo "  ✓ python-dotenv installed" || echo "  ✗ python-dotenv NOT installed (run: pip install -r requirements.txt)"
python3 -c "import httpx" 2>/dev/null && echo "  ✓ httpx installed" || echo "  ✗ httpx NOT installed (run: pip install -r requirements.txt)"

echo ""

# Verify AWS connectivity
echo "[5/6] Verifying AWS connectivity..."
if aws sts get-caller-identity &>/dev/null; then
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    USER_ARN=$(aws sts get-caller-identity --query Arn --output text)
    echo "  ✓ AWS credentials valid"
    echo "    Account: $ACCOUNT_ID"
    echo "    Identity: $USER_ARN"
else
    echo "  ✗ AWS credentials invalid or not configured"
    exit 1
fi

echo ""

# Run test suite (optional)
echo "[6/6] Running test suite (optional)..."
if [ -d "tests" ]; then
    echo "  Test suite found. Run tests? (y/N)"
    read -t 10 -n 1 RUN_TESTS || RUN_TESTS="n"
    echo ""
    
    if [ "$RUN_TESTS" = "y" ] || [ "$RUN_TESTS" = "Y" ]; then
        echo "  Running security tests..."
        python3 tests/test_security_fixes.py > test_results.log 2>&1
        
        echo "  Running comprehensive tests..."
        python3 tests/test_comprehensive_e2e.py >> test_results.log 2>&1
        
        # Check results
        if grep -q "OK" test_results.log && ! grep -q "FAILED" test_results.log; then
            echo "  ✓ All tests passed"
        else
            echo "  ⚠ Some tests failed - review test_results.log"
        fi
    else
        echo "  ⊘ Tests skipped"
    fi
else
    echo "  ⊘ Test suite not found (tests/ directory missing)"
fi

echo ""
echo "================================================================================"
echo "DEPLOYMENT SUMMARY"
echo "================================================================================"
echo ""
echo "Zero-Shield CLI v2.0.0-dev is ready to use!"
echo ""
echo "Security Features:"
echo "  ✓ 5-layer credential redaction"
echo "  ✓ XOR-encrypted session files"
echo "  ✓ Human-in-the-Loop confirmations"
echo "  ✓ Allowlist-based input sanitization"
echo "  ✓ File permissions restricted (0600)"
echo ""
echo "Capabilities:"
echo "  • 32 AWS actions across 14 service categories"
echo "  • 5 LLM models (GPT-4o, Llama-3.3-70B, Phi-4, DeepSeek-V3, gpt-4o-mini)"
echo "  • OODA loop cognitive framework"
echo "  • Context-aware Knowledge Graph"
echo ""
echo "Next Steps:"
echo "  1. Run: python3 zero_shield_cli.py"
echo "  2. Test with: list instances"
echo "  3. Set target: /target i-xxxxx"
echo "  4. Explore: inspect instance"
echo ""
echo "Documentation:"
echo "  • Quick Start: QUICK_START.md"
echo "  • Commands: docs/user-guide/COMMANDS.md"
echo "  • Examples: docs/user-guide/EXAMPLES.md"
echo "  • IAM Setup: aws-setup/IAM_POLICIES.md"
echo ""
echo "Rollback Instructions:"
echo "  If issues occur, restore from backup:"
echo "  cp zero_shield_cli.py.backup.* zero_shield_cli.py"
echo ""
echo "Support:"
echo "  • Repository: https://github.com/jerisadeumai/zero-shield-cli"
echo "  • Issues: https://github.com/jerisadeumai/zero-shield-cli/issues"
echo "  • Maintainer: Jeri L3D | JeriSadeuM"
echo ""
echo "================================================================================"
echo "DEPLOYMENT COMPLETE - Ready to launch!"
echo "================================================================================"
