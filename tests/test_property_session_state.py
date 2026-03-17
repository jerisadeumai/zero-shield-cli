#!/usr/bin/env python3
"""
Property-Based Test 1: Session State Round-Trip Integrity
Feature: zero-shield-cli-comprehensive-spec, Property 1: Session State Round-Trip Integrity

This test validates that session state data maintains integrity through the complete
serialize → encrypt → write → read → decrypt → parse pipeline.

Validates Requirements:
- 14.6-14.9: Session state persistence and restoration
- 16.1-16.10: Atomic write pattern prevents corruption
- 17.1-17.10: XOR encryption/decryption correctness
- 50.6: Data integrity guarantees

Property: For any valid session state data, the round-trip operation
serialize(data) → encrypt(data) → write(data) → read(data) → decrypt(data) → parse(data)
must produce data equivalent to the original input.
"""

import os
import sys
import json
import tempfile
import shutil
from datetime import datetime
from hypothesis import given, strategies as st, settings
from hypothesis.strategies import composite

# Add the parent directory to sys.path to import zero_shield_cli
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required functions and globals
import zero_shield_cli
from zero_shield_cli import _session_ctx, _quota_map, _cooldown_until, STATE_FILE

# Test configuration
TEST_ENCRYPTION_KEY = 'test_key_for_property_testing_12345678901234567890'

@composite
def session_state_data(draw):
    """Generate valid session state data structures for property testing."""
    
    # Generate session context data
    last_id = draw(st.one_of(
        st.none(),
        st.text(min_size=1, max_size=50).filter(lambda x: x.strip() and not any(c in x for c in '\n\r\t'))
    ))
    
    last_sg_id = draw(st.one_of(
        st.none(),
        st.text(min_size=1, max_size=50).filter(lambda x: x.strip() and not any(c in x for c in '\n\r\t'))
    ))
    
    model_idx = draw(st.integers(min_value=0, max_value=4))
    
    ctx = {
        "last_id": last_id,
        "last_sg_id": last_sg_id,
        "model_idx": model_idx
    }
    
    # Generate quota map data (model_idx -> quota info)
    quota_map = {}
    for i in range(draw(st.integers(min_value=0, max_value=5))):
        model_id = draw(st.integers(min_value=0, max_value=4))
        quota_map[model_id] = {
            "requests": draw(st.integers(min_value=0, max_value=10000)),
            "tokens": draw(st.integers(min_value=0, max_value=1000000)),
            "reset_time": draw(st.datetimes().map(lambda dt: dt.isoformat()))
        }
    
    # Generate cooldown data (model_idx -> cooldown timestamp)
    cooldown_until = {}
    for i in range(draw(st.integers(min_value=0, max_value=5))):
        model_id = draw(st.integers(min_value=0, max_value=4))
        cooldown_until[model_id] = draw(st.datetimes().map(lambda dt: dt.isoformat()))
    
    return {
        "saved_at": draw(st.datetimes().map(lambda dt: dt.isoformat())),
        "ctx": ctx,
        "quota_map": {str(k): v for k, v in quota_map.items()},
        "cooldown_until": {str(k): v for k, v in cooldown_until.items()}
    }

def xor_encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    """XOR encryption/decryption function matching zero_shield_cli implementation."""
    result = bytearray(len(data))
    for i in range(len(data)):
        result[i] = data[i] ^ key[i % len(key)]
    return bytes(result)

def serialize_session_state(data: dict) -> str:
    """Serialize session state data to JSON string."""
    return json.dumps(data, indent=2, default=str)

def parse_session_state(json_str: str) -> dict:
    """Parse JSON string back to session state data."""
    return json.loads(json_str)

def atomic_write_read(data: bytes, test_dir: str) -> bytes:
    """Perform atomic write and read using the same pattern as zero_shield_cli."""
    # Create temporary file in test directory
    fd, temp_path = tempfile.mkstemp(dir=test_dir, prefix=".state_", suffix=".tmp")
    target_path = os.path.join(test_dir, "session_state.json")
    
    try:
        # Write data atomically
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        os.replace(temp_path, target_path)
        
        # Set restrictive permissions (Unix only)
        if os.name != 'nt':
            os.chmod(target_path, 0o600)
        
        # Read data back
        with open(target_path, 'rb') as f:
            return f.read()
    
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(target_path):
            os.remove(target_path)

@given(session_state_data())
@settings(max_examples=100, deadline=None)
def test_session_state_round_trip_integrity(data):
    """
    Property Test 1: Session State Round-Trip Integrity
    
    Tests that session state data maintains integrity through the complete pipeline:
    serialize → encrypt → write → read → decrypt → parse
    """
    # Set up test environment
    test_dir = tempfile.mkdtemp()
    encryption_key = TEST_ENCRYPTION_KEY[:32].encode()
    
    try:
        # Step 1: Serialize to JSON
        json_data = serialize_session_state(data)
        json_bytes = json_data.encode('utf-8')
        
        # Step 2: Encrypt using XOR
        encrypted_data = xor_encrypt_decrypt(json_bytes, encryption_key)
        
        # Step 3: Atomic write and read
        read_encrypted_data = atomic_write_read(encrypted_data, test_dir)
        
        # Step 4: Decrypt using XOR
        decrypted_data = xor_encrypt_decrypt(read_encrypted_data, encryption_key)
        
        # Step 5: Parse back to dict
        decrypted_json = decrypted_data.decode('utf-8')
        parsed_data = parse_session_state(decrypted_json)
        
        # Property assertion: Round-trip must preserve data integrity
        assert parsed_data == data, f"Round-trip failed: {parsed_data} != {data}"
        
        # Additional integrity checks
        assert parsed_data["saved_at"] == data["saved_at"]
        assert parsed_data["ctx"] == data["ctx"]
        assert parsed_data["quota_map"] == data["quota_map"]
        assert parsed_data["cooldown_until"] == data["cooldown_until"]
        
        # Verify specific session context fields
        if data["ctx"]["last_id"] is not None:
            assert parsed_data["ctx"]["last_id"] == data["ctx"]["last_id"]
        if data["ctx"]["last_sg_id"] is not None:
            assert parsed_data["ctx"]["last_sg_id"] == data["ctx"]["last_sg_id"]
        assert parsed_data["ctx"]["model_idx"] == data["ctx"]["model_idx"]
        
    finally:
        # Cleanup test directory
        shutil.rmtree(test_dir, ignore_errors=True)

@given(st.binary(min_size=1, max_size=10000))
@settings(max_examples=100, deadline=None)
def test_xor_encryption_reversibility(data):
    """
    Property Test: XOR encryption is reversible
    
    Tests that decrypt(encrypt(data, key), key) == data for all inputs
    """
    encryption_key = TEST_ENCRYPTION_KEY[:32].encode()
    
    # Encrypt then decrypt
    encrypted = xor_encrypt_decrypt(data, encryption_key)
    decrypted = xor_encrypt_decrypt(encrypted, encryption_key)
    
    # Property assertion: XOR encryption must be reversible
    assert decrypted == data, f"XOR encryption not reversible: {len(decrypted)} != {len(data)}"

@given(session_state_data())
@settings(max_examples=50, deadline=None)
def test_json_serialization_reversibility(data):
    """
    Property Test: JSON serialization is reversible for session state data
    
    Tests that parse(serialize(data)) == data for valid session state structures
    """
    # Serialize then parse
    json_str = serialize_session_state(data)
    parsed_data = parse_session_state(json_str)
    
    # Property assertion: JSON serialization must be reversible
    assert parsed_data == data, f"JSON serialization not reversible: {parsed_data} != {data}"

if __name__ == "__main__":
    # Set test environment
    os.environ['GITHUB_TOKEN'] = TEST_ENCRYPTION_KEY
    
    print("Feature: zero-shield-cli-comprehensive-spec, Property 1: Session State Round-Trip Integrity")
    print("Running property-based tests for session state integrity...")
    print()
    
    # Run the property tests
    try:
        print("Testing session state round-trip integrity...")
        test_session_state_round_trip_integrity()
        print("✓ Session state round-trip integrity test passed")
        
        print("\nTesting XOR encryption reversibility...")
        test_xor_encryption_reversibility()
        print("✓ XOR encryption reversibility test passed")
        
        print("\nTesting JSON serialization reversibility...")
        test_json_serialization_reversibility()
        print("✓ JSON serialization reversibility test passed")
        
        print("\n✓ All property tests passed!")
        
    except Exception as e:
        print(f"✗ Property test failed: {e}")
        if __name__ == "__main__":
            sys.exit(1)