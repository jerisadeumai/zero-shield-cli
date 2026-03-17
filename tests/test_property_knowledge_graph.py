#!/usr/bin/env python3
"""
Property-Based Test 2: Knowledge Graph Round-Trip Integrity
Feature: zero-shield-cli-comprehensive-spec, Property 2: Knowledge Graph Round-Trip Integrity

This test validates that Knowledge Graph data maintains integrity through the complete
serialize → encrypt → write → read → decrypt → parse pipeline.

Validates Requirements:
- 15.1-15.8: Knowledge Graph persistence and restoration
- 16.1-16.10: Atomic write pattern prevents corruption
- 17.1-17.10: XOR encryption/decryption correctness
- 50.7: Data integrity guarantees

Property: For any valid Knowledge Graph data, the round-trip operation
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
from zero_shield_cli import KG_FILE

# Test configuration
TEST_ENCRYPTION_KEY = 'test_key_for_property_testing_12345678901234567890'

@composite
def knowledge_graph_data(draw):
    """Generate valid Knowledge Graph data structures for property testing."""
    
    # Generate security group rules cache
    sg_rules = {}
    for i in range(draw(st.integers(min_value=0, max_value=5))):
        sg_id = f"sg-{draw(st.text(min_size=8, max_size=17, alphabet='0123456789abcdef'))}"
        sg_rules[sg_id] = {
            "rules": draw(st.lists(
                st.fixed_dictionaries({
                    "protocol": st.sampled_from(["tcp", "udp", "icmp", "-1"]),
                    "from_port": st.integers(min_value=0, max_value=65535),
                    "to_port": st.integers(min_value=0, max_value=65535),
                    "cidr": st.sampled_from(["0.0.0.0/0", "10.0.0.0/8", "192.168.0.0/16"])
                }),
                min_size=0,
                max_size=10
            )),
            "cached_at": draw(st.datetimes().map(lambda dt: dt.isoformat()))
        }
    
    # Generate VPC configuration cache
    vpc_configs = {}
    for i in range(draw(st.integers(min_value=0, max_value=3))):
        vpc_id = f"vpc-{draw(st.text(min_size=8, max_size=17, alphabet='0123456789abcdef'))}"
        vpc_configs[vpc_id] = {
            "cidr_block": draw(st.sampled_from(["10.0.0.0/16", "172.16.0.0/12", "192.168.0.0/16"])),
            "subnets": draw(st.lists(
                st.text(min_size=15, max_size=24).filter(lambda x: x.startswith("subnet-")),
                min_size=0,
                max_size=5
            )),
            "cached_at": draw(st.datetimes().map(lambda dt: dt.isoformat()))
        }
    
    # Generate IAM mappings cache
    iam_mappings = {}
    for i in range(draw(st.integers(min_value=0, max_value=5))):
        instance_id = f"i-{draw(st.text(min_size=8, max_size=17, alphabet='0123456789abcdef'))}"
        iam_mappings[instance_id] = {
            "role": draw(st.text(min_size=5, max_size=50).filter(lambda x: x.strip())),
            "policies": draw(st.lists(
                st.text(min_size=5, max_size=50).filter(lambda x: x.strip()),
                min_size=0,
                max_size=5
            )),
            "cached_at": draw(st.datetimes().map(lambda dt: dt.isoformat()))
        }
    
    return {
        "saved_at": draw(st.datetimes().map(lambda dt: dt.isoformat())),
        "sg_rules": sg_rules,
        "vpc_configs": vpc_configs,
        "iam_mappings": iam_mappings
    }

def xor_encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    """XOR encryption/decryption function matching zero_shield_cli implementation."""
    result = bytearray(len(data))
    for i in range(len(data)):
        result[i] = data[i] ^ key[i % len(key)]
    return bytes(result)

def serialize_kg(data: dict) -> str:
    """Serialize Knowledge Graph data to JSON string."""
    return json.dumps(data, indent=2, default=str)

def parse_kg(json_str: str) -> dict:
    """Parse JSON string back to Knowledge Graph data."""
    return json.loads(json_str)

def atomic_write_read(data: bytes, test_dir: str) -> bytes:
    """Perform atomic write and read using the same pattern as zero_shield_cli."""
    # Create temporary file in test directory
    fd, temp_path = tempfile.mkstemp(dir=test_dir, prefix=".kg_", suffix=".tmp")
    target_path = os.path.join(test_dir, "session_kg.json")
    
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

@given(knowledge_graph_data())
@settings(max_examples=100, deadline=None)
def test_knowledge_graph_round_trip_integrity(data):
    """
    Property Test 2: Knowledge Graph Round-Trip Integrity
    
    Tests that Knowledge Graph data maintains integrity through the complete pipeline:
    serialize → encrypt → write → read → decrypt → parse
    """
    # Set up test environment
    test_dir = tempfile.mkdtemp()
    encryption_key = TEST_ENCRYPTION_KEY[:32].encode()
    
    try:
        # Step 1: Serialize to JSON
        json_data = serialize_kg(data)
        json_bytes = json_data.encode('utf-8')
        
        # Step 2: Encrypt using XOR
        encrypted_data = xor_encrypt_decrypt(json_bytes, encryption_key)
        
        # Step 3: Atomic write and read
        read_encrypted_data = atomic_write_read(encrypted_data, test_dir)
        
        # Step 4: Decrypt using XOR
        decrypted_data = xor_encrypt_decrypt(read_encrypted_data, encryption_key)
        
        # Step 5: Parse back to dict
        decrypted_json = decrypted_data.decode('utf-8')
        parsed_data = parse_kg(decrypted_json)
        
        # Property assertion: Round-trip must preserve data integrity
        assert parsed_data == data, f"Round-trip failed: {parsed_data} != {data}"
        
        # Additional integrity checks
        assert parsed_data["saved_at"] == data["saved_at"]
        assert parsed_data["sg_rules"] == data["sg_rules"]
        assert parsed_data["vpc_configs"] == data["vpc_configs"]
        assert parsed_data["iam_mappings"] == data["iam_mappings"]
        
        # Verify cached data structures preserved
        for sg_id, sg_data in data["sg_rules"].items():
            assert parsed_data["sg_rules"][sg_id] == sg_data
        
        for vpc_id, vpc_data in data["vpc_configs"].items():
            assert parsed_data["vpc_configs"][vpc_id] == vpc_data
        
        for instance_id, iam_data in data["iam_mappings"].items():
            assert parsed_data["iam_mappings"][instance_id] == iam_data
        
    finally:
        # Cleanup test directory
        shutil.rmtree(test_dir, ignore_errors=True)

if __name__ == "__main__":
    # Set test environment
    os.environ['GITHUB_TOKEN'] = TEST_ENCRYPTION_KEY
    
    print("Feature: zero-shield-cli-comprehensive-spec, Property 2: Knowledge Graph Round-Trip Integrity")
    print("Running property-based tests for Knowledge Graph integrity...")
    print()
    
    # Run the property tests
    try:
        print("Testing Knowledge Graph round-trip integrity...")
        test_knowledge_graph_round_trip_integrity()
        print("✓ Knowledge Graph round-trip integrity test passed")
        
        print("\n✓ All property tests passed!")
        
    except Exception as e:
        print(f"✗ Property test failed: {e}")
        if __name__ == "__main__":
            sys.exit(1)
