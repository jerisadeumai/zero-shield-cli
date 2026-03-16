#!/usr/bin/env python3
"""
Property-Based Test 5: AWS Metadata Sanitization Completeness
Feature: zero-shield-cli-comprehensive-spec, Property 5: AWS Metadata Sanitization

Validates Requirements: 12.1-12.10 (Prompt injection prevention)

Property: For any AWS metadata containing structural characters or dangerous keywords,
_sanitize_aws_tag() must remove all injection vectors.
"""

import os
import sys
from hypothesis import given, strategies as st, settings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zero_shield_cli import _sanitize_aws_tag

@given(st.text(min_size=0, max_size=200))
@settings(max_examples=100, deadline=None)
def test_structural_characters_removed(text):
    """Test that structural characters are removed from AWS tags."""
    dangerous_chars = ['[', ']', '`', '<', '>', '"']
    text_with_chars = text + ''.join(dangerous_chars)
    
    sanitized = _sanitize_aws_tag(text_with_chars)
    
    for char in dangerous_chars:
        assert char not in sanitized, f"Dangerous character not removed: {char}"

@given(st.text(min_size=0, max_size=100))
@settings(max_examples=100, deadline=None)
def test_action_keyword_removed(text):
    """Test that ACTION: keyword is removed to prevent command injection."""
    text_with_action = text + "ACTION:LIST"
    
    sanitized = _sanitize_aws_tag(text_with_action)
    
    assert "ACTION:" not in sanitized, "ACTION: keyword not removed"

@given(st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs', 'Pd')), min_size=0, max_size=100))
@settings(max_examples=50, deadline=None)
def test_allowlist_only_characters(text):
    """Test that only allowlisted characters pass through."""
    sanitized = _sanitize_aws_tag(text)
    
    # Allowlist: alphanumeric, spaces, hyphens
    allowed_pattern = re.compile(r'^[a-zA-Z0-9\s\-]*$')
    assert allowed_pattern.match(sanitized), f"Non-allowlisted characters in output: {sanitized}"

if __name__ == "__main__":
    import re
    print("Feature: zero-shield-cli-comprehensive-spec, Property 5: AWS Metadata Sanitization")
    print("Running property-based tests...")
    
    try:
        print("Testing structural character removal...")
        test_structural_characters_removed()
        print("✓ Structural character removal test passed")
        
        print("\nTesting ACTION keyword removal...")
        test_action_keyword_removed()
        print("✓ ACTION keyword removal test passed")
        
        print("\nTesting allowlist-only characters...")
        test_allowlist_only_characters()
        print("✓ Allowlist-only characters test passed")
        
        print("\n✓ All property tests passed!")
    except Exception as e:
        print(f"✗ Property test failed: {e}")
        sys.exit(1)
