#!/usr/bin/env python3
"""
Property-Based Test 3 & 4: Credential Redaction Completeness and Idempotence
Feature: zero-shield-cli-comprehensive-spec, Property 3 & 4: Credential Redaction

This test validates that credential redaction removes all sensitive patterns and is idempotent.

Validates Requirements:
- 11.1-11.10: 5-layer credential redaction
- Property 3: Completeness - all credentials are redacted
- Property 4: Idempotence - multiple applications produce same result

Property 3: For any text containing AWS credentials, _redact_secrets() must remove all patterns.
Property 4: For any text, _redact_secrets(_redact_secrets(text)) == _redact_secrets(text)
"""

import os
import sys
import re
from hypothesis import given, strategies as st, settings
from hypothesis.strategies import composite

# Add the parent directory to sys.path to import zero_shield_cli
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required functions
import zero_shield_cli
from zero_shield_cli import _redact_secrets

@composite
def aws_access_key(draw):
    """Generate valid AWS access key pattern."""
    return "AKIA" + ''.join(draw(st.lists(
        st.sampled_from('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        min_size=16,
        max_size=16
    )))

@composite
def aws_secret_key(draw):
    """Generate valid AWS secret key pattern."""
    return ''.join(draw(st.lists(
        st.sampled_from('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/+='),
        min_size=40,
        max_size=40
    )))

@composite
def aws_session_token(draw):
    """Generate valid AWS session token pattern."""
    return ''.join(draw(st.lists(
        st.sampled_from('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/+='),
        min_size=100,
        max_size=200
    )))

@composite
def jwt_token(draw):
    """Generate valid JWT token pattern."""
    header = ''.join(draw(st.lists(
        st.sampled_from('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'),
        min_size=20,
        max_size=50
    )))
    payload = ''.join(draw(st.lists(
        st.sampled_from('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'),
        min_size=50,
        max_size=100
    )))
    signature = ''.join(draw(st.lists(
        st.sampled_from('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'),
        min_size=20,
        max_size=50
    )))
    return f"eyJ{header}.{payload}.{signature}"

@composite
def text_with_credentials(draw):
    """Generate text containing various credential types."""
    credential_type = draw(st.sampled_from([
        'access_key',
        'secret_key',
        'session_token',
        'jwt',
        'multiple'
    ]))
    
    prefix = draw(st.text(min_size=0, max_size=50))
    suffix = draw(st.text(min_size=0, max_size=50))
    
    if credential_type == 'access_key':
        cred = draw(aws_access_key())
        return f"{prefix}{cred}{suffix}", cred
    elif credential_type == 'secret_key':
        cred = draw(aws_secret_key())
        return f"{prefix}{cred}{suffix}", cred
    elif credential_type == 'session_token':
        cred = draw(aws_session_token())
        return f"{prefix}{cred}{suffix}", cred
    elif credential_type == 'jwt':
        cred = draw(jwt_token())
        return f"{prefix}{cred}{suffix}", cred
    else:  # multiple
        access = draw(aws_access_key())
        secret = draw(aws_secret_key())
        return f"{prefix}Access: {access}, Secret: {secret}{suffix}", [access, secret]

@given(text_with_credentials())
@settings(max_examples=100, deadline=None)
def test_credential_redaction_completeness(data):
    """
    Property Test 3: Credential Redaction Completeness
    
    Tests that _redact_secrets() removes all credential patterns from text.
    """
    text, credentials = data
    redacted = _redact_secrets(text)
    
    # Property assertion: Original credentials must not appear in redacted text
    if isinstance(credentials, list):
        for cred in credentials:
            assert cred not in redacted, f"Credential not redacted: {cred[:10]}..."
    else:
        assert credentials not in redacted, f"Credential not redacted: {credentials[:10]}..."
    
    # Verify redaction markers are present
    assert "[REDACTED" in redacted or text == redacted, "Redaction marker missing"

@given(st.text(min_size=0, max_size=500))
@settings(max_examples=100, deadline=None)
def test_credential_redaction_idempotence(text):
    """
    Property Test 4: Credential Redaction Idempotence
    
    Tests that applying _redact_secrets() multiple times produces the same result.
    """
    # Apply redaction once
    redacted_once = _redact_secrets(text)
    
    # Apply redaction twice
    redacted_twice = _redact_secrets(redacted_once)
    
    # Property assertion: Idempotence - f(f(x)) == f(x)
    assert redacted_once == redacted_twice, "Redaction is not idempotent"
    
    # Apply redaction three times
    redacted_thrice = _redact_secrets(redacted_twice)
    
    # Verify still idempotent
    assert redacted_once == redacted_thrice, "Redaction is not idempotent after 3 applications"

@given(st.text(min_size=0, max_size=200))
@settings(max_examples=50, deadline=None)
def test_aws_resource_ids_preserved(text):
    """
    Property Test: AWS resource IDs are preserved during redaction
    
    Tests that legitimate AWS resource IDs (i-, sg-, vpc-, vol-) are not redacted.
    """
    # Add AWS resource IDs to text
    resource_ids = ["i-1234567890abcdef0", "sg-0123456789abcdef0", "vpc-abc123", "vol-xyz789"]
    text_with_ids = text + " " + " ".join(resource_ids)
    
    redacted = _redact_secrets(text_with_ids)
    
    # Property assertion: Resource IDs must be preserved
    for resource_id in resource_ids:
        assert resource_id in redacted, f"Resource ID incorrectly redacted: {resource_id}"

if __name__ == "__main__":
    print("Feature: zero-shield-cli-comprehensive-spec, Property 3 & 4: Credential Redaction")
    print("Running property-based tests for credential redaction...")
    print()
    
    # Run the property tests
    try:
        print("Testing credential redaction completeness...")
        test_credential_redaction_completeness()
        print("✓ Credential redaction completeness test passed")
        
        print("\nTesting credential redaction idempotence...")
        test_credential_redaction_idempotence()
        print("✓ Credential redaction idempotence test passed")
        
        print("\nTesting AWS resource ID preservation...")
        test_aws_resource_ids_preserved()
        print("✓ AWS resource ID preservation test passed")
        
        print("\n✓ All property tests passed!")
        
    except Exception as e:
        print(f"✗ Property test failed: {e}")
        sys.exit(1)
