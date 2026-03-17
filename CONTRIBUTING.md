# Contributing to Zero-Shield CLI

We welcome contributions! Here's how you can help:

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/zero-shield-cli.git`
3. Create a branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Run tests: `python3 -m pytest tests/ -v`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp environments/local/.env.example .env
# Edit .env with your credentials

# Run tests
python3 -m pytest tests/ -v
```

## Code Style

- Follow PEP 8 guidelines
- Add docstrings to new functions
- Include type hints where appropriate
- Write tests for new features

## Running Tests

Zero-Shield CLI has a comprehensive test suite with 152 tests across multiple categories:

### Test Categories

**1. Action Detection Tests (8 tests)**
```bash
# Test natural language command parsing
python3 -m pytest tests/test_action_detection.py -v
```

**2. Comprehensive E2E Tests (66 tests)**
```bash
# Test all AWS functionality end-to-end
python3 -m pytest tests/test_comprehensive_e2e.py -v
```

**3. Security Tests (35 tests)**
```bash
# Test credential redaction, HITL, encryption
python3 -m pytest tests/test_security_fixes.py -v
```

**4. Property-Based Tests (44 tests across 6 files)**
```bash
# Test AWS sanitization
python3 -m pytest tests/test_property_aws_sanitization.py -v

# Test credential redaction
python3 -m pytest tests/test_property_credential_redaction.py -v

# Test knowledge graph
python3 -m pytest tests/test_property_knowledge_graph.py -v

# Test session state
python3 -m pytest tests/test_property_session_state.py -v

# Test remaining batch 1
python3 -m pytest tests/test_property_remaining_batch1.py -v

# Test final batch
python3 -m pytest tests/test_property_final_batch.py -v
```

### Run All Tests
```bash
# Run complete test suite with verbose output
python3 -m pytest tests/ -v

# Expected output:
# ================================= test session starts =================================
# platform win32 -- Python 3.11.0, pytest-7.4.0, pluggy-1.0.0 -- python.exe
# cachedir: .pytest_cache
# rootdir: C:\path\to\zero-shield-cli
# collected 152 tests
# 
# tests/test_action_detection.py::test_action_detection_basic PASSED                [ 5%]
# tests/test_comprehensive_e2e.py::test_ec2_instance_listing PASSED                [15%]
# tests/test_property_final_batch.py::TestProperty16ModelSelectionValidation::test_out_of_range_model_numbers_rejected PASSED [55%]
# tests/test_security_fixes.py::test_file_permissions_unix SKIPPED (File permissions t...) [97%]
# =============================== 148 passed, 4 skipped in 16.80s ===============================
```

### Test Collection Info
```bash
# See all tests without running them
python3 -m pytest tests/ --collect-only -q
# Shows: 152 tests collected in 2.76s
```

### Test Results Summary
- **Total Tests:** 152
- **Pass Rate:** 97.4% (148 passing, 4 skipped)
- **Skipped Tests:** 4 Windows file permission tests
- **Test Breakdown:**
  - Action detection: 8 tests
  - Comprehensive E2E: 66 tests  
  - Security validation: 35 tests
  - Property-based: 44 tests (across 6 files)

### Troubleshooting Test Issues

**If tests fail:**
1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check environment configuration: `cp environments/local/.env.example .env`
3. Verify AWS credentials (for E2E tests): `aws sts get-caller-identity`
4. Check Python version: `python3 --version` (requires 3.9+)

**Common test issues:**
- **File permission tests skipped on Windows:** This is expected behavior
- **AWS credential errors:** Configure `.env` file or AWS CLI
- **Import errors:** Ensure you're running from the project root directory

## Testing

All new features must include tests:
- Add tests to appropriate test files in `tests/` directory
- Ensure 97.4% or higher pass rate before submitting PR
- Include both unit tests and integration tests where applicable

## Documentation

Update documentation for new features:
- User-facing: `docs/user-guide/`
- Technical: `docs/architecture/`
- Examples: `docs/user-guide/EXAMPLES.md`

## Questions?

Open an issue or discussion on GitHub.

Thank you for contributing! 


---

**Project Maintainer:** Jeri L3D | JeriSadeuM  
**Repository:** https://github.com/jerisadeumai/zero-shield-cli  
**Copyright © 2026 Jeri L3D | JeriSadeuM | All Rights Reserved**
