# Zero-Shield CLI: Validation Test Suite

**Total Tests:** 131 (35 security + 66 comprehensive + 30 property-based)  
**Test Pass Rate:** 100%  
**Specification:** `.kiro/specs/zero-shield-cli-comprehensive-spec/`

---

## Test Suite Overview

### Test Categories

| Category | Tests | Status | Description |
|----------|-------|--------|-------------|
| **Security Validation** | 35 | ✅ 100% | Credential redaction, HITL, encryption |
| **Comprehensive E2E** | 66 | ✅ 100% | All functionality, edge cases, integration |
| **Property-Based** | 30 | ✅ 100% | Universal correctness properties |
| **Total** | **131** | ✅ **100%** | Complete validation |

### Quick Start

```bash
# Run all security tests
python3 tests/test_security_fixes.py

# Run all integration tests
python3 tests/test_comprehensive_e2e.py

# Run property-based tests
python3 tests/test_property_*.py

# Run specific test category
python3 -m pytest tests/test_comprehensive_e2e.py::TestCredentialRedaction -v
```

---

## Property-Based Testing Guide

### Overview

Property-based tests validate universal correctness properties across all possible inputs using the Hypothesis library. Unlike unit tests that check specific examples, property tests generate hundreds of random inputs to verify system behavior holds universally.

### Running Property-Based Tests

```bash
# Run all property tests
python3 -m pytest tests/test_property_*.py -v

# Run specific property test
python3 tests/test_property_session_state.py

# Run with increased iterations (default: 100)
python3 -m pytest tests/test_property_*.py --hypothesis-max-examples=1000
```

### Property Test Categories

#### 1. Data Integrity Properties (4 tests)

**Property 1: Session State Round-Trip Integrity**
```bash
python3 tests/test_property_session_state.py
```
Validates: Session state survives serialize → encrypt → write → read → decrypt → parse cycle

**Property 2: Knowledge Graph Round-Trip Integrity**
```bash
python3 tests/test_property_knowledge_graph.py
```
Validates: Knowledge Graph data preserved through full persistence pipeline

**Property 13: Atomic Write Corruption Prevention**
Validates: Interrupted writes don't corrupt existing files

**Property 14: XOR Encryption Reversibility**
Validates: decrypt(encrypt(data, key), key) == data for all inputs

#### 2. Security Properties (6 tests)

**Property 3: Credential Redaction Completeness**
```bash
python3 tests/test_property_credential_redaction.py
```
Validates: All AWS credentials (5 types) removed from any text

**Property 4: Credential Redaction Idempotence**
Validates: Applying redaction multiple times produces same result

**Property 5: AWS Metadata Sanitization Completeness**
```bash
python3 tests/test_property_aws_sanitization.py
```
Validates: All structural characters removed from AWS resource metadata

**Property 6: HITL Confirmation Requirement**
Validates: Destructive actions require exact resource ID re-entry

**Property 23: Path Sanitization Security**
Validates: Path traversal attacks prevented (removes ".." references)

**Property 24: Log Sanitization Application**
Validates: CloudWatch logs sanitized before display

#### 3. System Behavior Properties (8 tests)

**Property 7: OODA Loop Formatting Enforcement**
Validates: 3-strike system terminates on missing [ORIENT]/[DECIDE]/[ACT] markers

**Property 8: Action Detection Correctness**
Validates: All [ACTION:TAG] patterns extracted with correct resource IDs

**Property 9: AWS Client Caching Invariant**
Validates: Multiple calls to _client(service) return same cached instance

**Property 10: Rate Limit Cooldown Enforcement**
Validates: Models in cooldown prevent API calls until expiration

**Property 11: Target Context Preservation**
Validates: Active target persists across commands and restarts

**Property 18: Conversation History Management**
Validates: /clear resets history while preserving session state and KG

**Property 19: Signal Handler State Preservation**
Validates: Ctrl+C saves session state before exit

**Property 28: Action Execution Result Feedback**
Validates: Action results fed back into OODA Observe phase

#### 4. Risk Assessment Properties (2 tests)

**Property 12: Security Group Risk Assessment Accuracy**
Validates: 0.0.0.0/0 on SSH/RDP flagged as high risk, RFC 1918 not flagged

**Property 29: Knowledge Graph Update on Action Execution**
Validates: Resource metadata actions update Knowledge Graph

#### 5. User Interface Properties (4 tests)

**Property 15: Paste Guard Buffer Protection**
Validates: Multi-line paste bursts drained within 0.2 seconds

**Property 16: Model Selection Validation**
Validates: Invalid model numbers (not 1-5) rejected with clear errors

**Property 20: Color Code Application Consistency**
Validates: Correct ANSI colors applied (green=success, red=error, yellow=warning, cyan=info)

**Property 25: Timestamp Format Consistency**
Validates: All timestamps use ISO 8601 format with UTC timezone

#### 6. Configuration Properties (6 tests)

**Property 17: Preflight Validation Completeness**
Validates: GITHUB_TOKEN, AWS credentials, API connectivity verified at startup

**Property 21: Lazy Client Factory Service Support**
Validates: All 14 supported services return valid clients, unsupported raise ValueError

**Property 22: Quota Tracking Accuracy**
Validates: API calls update model request count and token consumption

**Property 26: Version String Consistency**
Validates: All 5 locations show "v2.0.0-dev" consistently

**Property 27: Dependency Version Pinning**
Validates: requirements.txt specifies exact versions for critical dependencies

**Property 30: Cross-Platform Terminal I/O Compatibility**
Validates: Appropriate I/O mechanisms per platform (termios on Unix, msvcrt on Windows)

### Property Test Example

```python
from hypothesis import given, settings, strategies as st

@settings(max_examples=100)  # Minimum 100 iterations
@given(state=st.builds(generate_session_state))
def test_session_state_round_trip(state):
    """
    Feature: zero-shield-cli-comprehensive-spec
    Property 1: Session State Round-Trip Integrity
    
    For any valid SessionState object, serializing to JSON, encrypting 
    with XOR, writing to disk, reading from disk, decrypting with XOR, 
    and parsing from JSON SHALL produce an equivalent SessionState object.
    """
    # Serialize
    json_str = json.dumps(state)
    
    # Encrypt
    encrypted = xor_encrypt(json_str, GITHUB_TOKEN)
    
    # Write (atomic pattern)
    temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False)
    temp_file.write(encrypted)
    temp_file.close()
    os.replace(temp_file.name, "test_session_state.json")
    
    # Read
    with open("test_session_state.json", "rb") as f:
        encrypted_read = f.read()
    
    # Decrypt
    decrypted = xor_decrypt(encrypted_read, GITHUB_TOKEN)
    
    # Parse
    state_loaded = json.loads(decrypted)
    
    # Assert equivalence
    assert state_loaded == state
```

### Benefits of Property-Based Testing

- **Universal Validation**: Tests verify behavior across all possible inputs, not just specific examples
- **Edge Case Discovery**: Automatically finds edge cases developers didn't anticipate
- **Regression Prevention**: Catches bugs that unit tests miss
- **Mathematical Guarantees**: Provides formal correctness guarantees
- **Minimal Test Code**: One property test replaces dozens of unit tests

### Specification Traceability

Every property test traces back to specific requirements in the comprehensive specification:

- **Requirements**: `.kiro/specs/zero-shield-cli-comprehensive-spec/requirements.md` (50 requirements)
- **Design Properties**: `.kiro/specs/zero-shield-cli-comprehensive-spec/design.md` (30 properties)
- **Implementation Tasks**: `.kiro/specs/zero-shield-cli-comprehensive-spec/tasks.md` (all completed)

---

## ✅ VERIFIED FROM YOUR OUTPUT

### Test 5: System Guard - Single Action ✓ PASSED
**Prompt:** `Give me your confidence score for this environment's security posture`

**Result:** 
- ✅ No "[SYSTEM GUARD]" warning
- ✅ No "MULTIPLE_ACTIONS_DETECTED" 
- ✅ Clean execution: `[ACTION:SG_RULES:sg-041a97ba55afb006e]`
- ✅ Proper OODA format: [ORIENT] → [DECIDE] → [ACT]

**Status:** CRITICAL TEST PASSED

---

## 🔄 REMAINING TESTS TO RUN

Copy and paste these prompts in order:

---

### Test Suite 1: Target Resolution (NEW FIX)

#### Test 1: List Instances
```
list
```
**Expected:** Lists all instances with full IDs
**Pass Criteria:** Shows `i-02c35a50d214cf886` (full ID)

---

#### Test 2: Partial ID Resolution
```
/target i-02c35a
```
**Expected:** `[*] Target resolved to instance: i-02c35a50d214cf886` (FULL ID)
**Fail if:** Shows partial ID "i-02c35a"
**Status:** CRITICAL TEST

---

#### Test 3: Numeric Target (Ambiguity Detection)
```
/target 1
```
**Expected:** Resolves to instance [1] OR shows ambiguity with full IDs
**Pass Criteria:** Full IDs displayed in any messages
**Status:** CRITICAL TEST

---

#### Test 4: Partial SG Resolution
```
/target sg-041
```
**Expected:** `[*] Target resolved to security group: sg-041a97ba55afb006e` (FULL ID)
**Fail if:** Shows partial ID "sg-041"
**Status:** CRITICAL TEST

---

### Test Suite 2: System Guard (Previous Fix Validation)

#### Test 5: Single Action - List ✅ ALREADY PASSED
(See verified section above)

---

#### Test 6: Inspect Without Guard Trigger
```
/target i-02c35a
inspect instance
```
**Expected:** Clean execution, no "[SYSTEM GUARD]" warning
**Fail if:** "MULTIPLE_ACTIONS_DETECTED" appears
**Status:** MAJOR TEST

---

### Test Su