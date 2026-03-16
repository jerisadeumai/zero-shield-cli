# Zero-Shield Test Suites

## Running Tests

### Comprehensive Integration Tests
```bash
python3 tests/test_comprehensive_e2e.py
```

### Security Validation Tests
```bash
python3 tests/test_security_fixes.py
```

## Test Coverage

- **Integration Tests:** 66 tests covering all functionality (mocked AWS responses)
- **Security Tests:** 35 tests validating security hardening

**IMPORTANT:** test_comprehensive_e2e.py contains integration tests, NOT true end-to-end tests. Tests use mocked AWS responses and do not validate complete user workflows.

See [validation/TEST_REPORTS.md](../validation/TEST_REPORTS.md) for detailed results.
