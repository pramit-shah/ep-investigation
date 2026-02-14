#!/usr/bin/env python3
"""
Test suite for security, identity protection, and release control
"""

def test_creator_identity_protection():
    """Test creator identity protection features"""
    from identity_protection import CreatorIdentityProtection
    
    print("Testing Creator Identity Protection...")
    
    protection = CreatorIdentityProtection()
    
    # Test anonymous attribution
    attribution = protection.get_safe_attribution()
    assert 'name' in attribution
    assert 'email' in attribution
    assert 'id' in attribution
    assert attribution['name'] in CreatorIdentityProtection.ANONYMOUS_NAMES
    assert attribution['email'] in CreatorIdentityProtection.ANONYMOUS_EMAILS
    print("  ✓ Anonymous attribution works")
    
    # Test metadata sanitization
    metadata = {
        'name': 'Real Name',
        'email': 'real@email.com',
        'username': 'realuser',
        'project': 'Test'
    }
    sanitized = protection.sanitize_metadata(metadata)
    assert sanitized['name'] == '[REDACTED]'
    assert sanitized['email'] == '[REDACTED]'
    assert sanitized['username'] == '[REDACTED]'
    assert sanitized['project'] == 'Test'  # Not PII
    print("  ✓ Metadata sanitization works")
    
    # Test anonymous signature
    signature = protection.create_anonymous_signature("test content")
    assert len(signature) == 64  # SHA-256 hex length
    print("  ✓ Anonymous signature generation works")
    
    print("  ✓ Creator identity protection: PASSED\n")


def test_anonymous_contributions():
    """Test anonymous contribution management"""
    from identity_protection import AnonymousContributionManager
    
    print("Testing Anonymous Contribution Management...")
    
    manager = AnonymousContributionManager()
    
    # Add contributions
    contrib_id1 = manager.add_contribution(
        {'finding': 'Test finding'},
        contributor_hint='researcher1'
    )
    contrib_id2 = manager.add_contribution(
        {'finding': 'Another finding'},
        contributor_hint='researcher1'
    )
    
    assert len(manager.contributions) == 2
    assert contrib_id1.startswith('CONTRIB_')
    
    # Same contributor should get same ID
    assert manager.contributions[0]['contributor_id'] == manager.contributions[1]['contributor_id']
    
    summary = manager.get_contributions_summary()
    assert summary['total_contributions'] == 2
    assert summary['anonymous_contributors'] == 1
    
    print("  ✓ Anonymous contributions: PASSED\n")


def test_data_anonymization():
    """Test data anonymization"""
    from identity_protection import DataAnonymizer
    
    print("Testing Data Anonymization...")
    
    anonymizer = DataAnonymizer()
    
    # Anonymize entities
    anon1 = anonymizer.anonymize_entity("John Doe")
    anon2 = anonymizer.anonymize_entity("Jane Smith")
    anon3 = anonymizer.anonymize_entity("John Doe")  # Same entity again
    
    assert anon1.startswith('ENTITY_')
    assert anon2.startswith('ENTITY_')
    assert anon1 == anon3  # Same entity gets same anonymous name
    assert anon1 != anon2  # Different entities get different names
    
    # Test text anonymization
    text = "John Doe met with Jane Smith at the office"
    entities = ["John Doe", "Jane Smith"]
    anonymized = anonymizer.anonymize_text(text, entities)
    
    assert "John Doe" not in anonymized
    assert "Jane Smith" not in anonymized
    assert "ENTITY_" in anonymized
    
    # Test deanonymization (with authorization)
    original = anonymizer.deanonymize_entity(anon1, authorized=True)
    assert original == "John Doe"
    
    # Test unauthorized deanonymization
    try:
        anonymizer.deanonymize_entity(anon1, authorized=False)
        assert False, "Should have raised PermissionError"
    except PermissionError:
        pass
    
    print("  ✓ Data anonymization: PASSED\n")


def test_release_control():
    """Test release control system"""
    from release_control import InvestigationReleaseManager, ReleaseStatus
    
    print("Testing Release Control...")
    
    manager = InvestigationReleaseManager()
    
    # Seal data
    manager.seal_data('TEST_001', {'sensitive': 'data'}, 'finding')
    assert len(manager.sealed_items) == 1
    assert manager.sealed_items['TEST_001']['released'] == False
    
    # Try to release before ready
    result = manager.release_item('TEST_001', authorized=True)
    assert result is None, "Should not release before authorization"
    
    # Update completion
    manager.update_completion(0.50)
    assert manager.completion_percentage == 0.50
    
    # Still cannot release
    result = manager.release_item('TEST_001', authorized=True)
    assert result is None
    
    # Update to 95% and set criteria
    manager.update_completion(0.95)
    manager.release_criteria['evidence_verified'] = True
    manager.release_criteria['legal_review'] = True
    manager.release_criteria['safety_assessment'] = True
    manager.release_criteria['creator_consent'] = True
    
    # Authorize release
    manager.authorize_release('ANON_TEST', 'full')
    assert manager.release_authorization == True
    
    # Now can release
    result = manager.release_item('TEST_001', authorized=True)
    assert result is not None
    assert result == {'sensitive': 'data'}
    assert manager.sealed_items['TEST_001']['released'] == True
    
    print("  ✓ Release control: PASSED\n")


def test_progressive_disclosure():
    """Test progressive disclosure"""
    from release_control import ProgressiveDisclosure
    
    print("Testing Progressive Disclosure...")
    
    disclosure = ProgressiveDisclosure()
    
    # Test disclosure levels
    assert disclosure.get_disclosure_level(0.0) == 'NOTHING'
    assert disclosure.get_disclosure_level(0.50) == 'MINIMAL'
    assert disclosure.get_disclosure_level(0.75) == 'MODERATE'
    assert disclosure.get_disclosure_level(0.90) == 'SUBSTANTIAL'
    assert disclosure.get_disclosure_level(0.95) == 'COMPREHENSIVE'
    assert disclosure.get_disclosure_level(1.0) == 'COMPLETE'
    
    # Test sensitivity thresholds
    # Low sensitivity item at 50% completion
    can_disclose, reason = disclosure.can_disclose(1, 0.50)
    assert can_disclose == True
    
    # High sensitivity item at 50% completion
    can_disclose, reason = disclosure.can_disclose(5, 0.50)
    assert can_disclose == False
    
    # High sensitivity item at 100% completion
    can_disclose, reason = disclosure.can_disclose(5, 1.0)
    assert can_disclose == True
    
    print("  ✓ Progressive disclosure: PASSED\n")


def test_safe_git_config():
    """Test safe git configuration"""
    from identity_protection import setup_safe_git_config
    
    print("Testing Safe Git Configuration...")
    
    config = setup_safe_git_config()
    
    # Check config contains safe settings
    assert '[user]' in config
    assert 'name =' in config
    assert 'email =' in config
    assert '@' in config  # Email should be present
    
    # Check that it uses anonymous attribution
    assert 'Anonymous' in config or 'Investigator' in config or 'Researcher' in config
    
    print("  ✓ Safe git configuration: PASSED\n")


def test_secure_work_environment():
    """Test secure work environment"""
    from identity_protection import SecureWorkEnvironment
    
    print("Testing Secure Work Environment...")
    
    env = SecureWorkEnvironment()
    
    # Log actions
    env.log_action('TEST', 'Test action')
    env.log_action('SENSITIVE', 'Sensitive action', sensitive=True)
    
    assert len(env.actions) == 2
    assert env.actions[1]['description'] == '[REDACTED]'  # Sensitive action
    
    # Check status
    status = env.check_security_status()
    assert 'session_id' in status
    assert status['actions_logged'] == 2
    assert status['warnings'] == 0
    assert status['secure'] == True
    
    # Add warning
    env.add_security_warning("Test warning")
    status = env.check_security_status()
    assert status['secure'] == False
    
    # Get recommendations
    recommendations = env.get_recommendations()
    assert len(recommendations) > 0
    assert isinstance(recommendations[0], str)
    
    print("  ✓ Secure work environment: PASSED\n")


def test_safety_assessment():
    """Test pre-release safety assessment"""
    from release_control import SafeReleaseProtocol
    
    print("Testing Safety Assessment...")
    
    protocol = SafeReleaseProtocol()
    
    # Add checks
    protocol.add_pre_release_check('Test check 1', True)
    protocol.add_pre_release_check('Test check 2', True)
    protocol.add_pre_release_check('Test check 3', False)
    
    assert len(protocol.pre_release_checks) == 3
    
    # Run assessment
    assessment = protocol.run_safety_assessment()
    
    # Should fail because one check failed
    assert assessment['all_checks_passed'] == False
    assert assessment['safe_to_release'] == False
    
    print("  ✓ Safety assessment: PASSED\n")


def main():
    """Run all security tests"""
    print("="*70)
    print("SECURITY & PROTECTION - TEST SUITE")
    print("="*70)
    print()
    
    try:
        test_creator_identity_protection()
        test_anonymous_contributions()
        test_data_anonymization()
        test_release_control()
        test_progressive_disclosure()
        test_safe_git_config()
        test_secure_work_environment()
        test_safety_assessment()
        
        print("="*70)
        print("ALL SECURITY TESTS PASSED ✓")
        print("="*70)
        print()
        print("System verified:")
        print("  ✓ Creator identity protection")
        print("  ✓ Anonymous contributions")
        print("  ✓ Data anonymization")
        print("  ✓ Release control")
        print("  ✓ Progressive disclosure")
        print("  ✓ Safe git configuration")
        print("  ✓ Secure work environment")
        print("  ✓ Safety assessment")
        print()
        print("⚠️  CREATOR IDENTITY: PROTECTED")
        print("🔒 ALL DATA: SEALED UNTIL RELEASE")
        print()
        return 0
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
