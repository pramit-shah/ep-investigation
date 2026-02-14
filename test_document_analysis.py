#!/usr/bin/env python3
"""
Test suite for document analysis and autonomous update features
"""

def test_redaction_detection():
    """Test redaction detection capabilities"""
    from document_analyzer import RedactionDetector
    
    print("Testing Redaction Detection...")
    
    detector = RedactionDetector()
    
    # Test various redaction patterns
    test_text = """
    The individual [REDACTED] traveled with ███████ on multiple occasions.
    Financial records show $XXX,XXX paid to [WITHHELD] in 2015.
    The subject's name was __________ according to documents.
    """
    
    redactions = detector.detect_redactions(test_text)
    
    assert len(redactions) > 0, "Should detect redactions"
    assert any('REDACTED' in r['redacted_text'] for r in redactions), "Should detect [REDACTED]"
    assert any('█' in r['redacted_text'] for r in redactions), "Should detect blocks"
    
    print("  ✓ Redaction detection works")
    print(f"  ✓ Found {len(redactions)} redactions")


def test_cryptic_identifier_detection():
    """Test cryptic identifier detection"""
    from document_analyzer import AliasTracker
    
    print("\nTesting Cryptic Identifier Detection...")
    
    tracker = AliasTracker()
    
    test_text = """
    Subject-1 met with Individual-A and Person-X.
    The individual known as "J.E." was present.
    Communications refer to someone as "M" in emails.
    """
    
    cryptic = tracker.detect_cryptic_patterns(test_text)
    
    assert len(cryptic) > 0, "Should detect cryptic identifiers"
    assert any(c['type'] == 'code_identifier' for c in cryptic), "Should detect code identifiers"
    assert any(c['type'] == 'single_char_identifier' for c in cryptic), "Should detect single char"
    
    print("  ✓ Cryptic identifier detection works")
    print(f"  ✓ Found {len(cryptic)} cryptic identifiers")


def test_name_variation_detection():
    """Test name variation generation"""
    from document_analyzer import NameVariationDetector
    
    print("\nTesting Name Variation Detection...")
    
    detector = NameVariationDetector()
    
    # Test variation generation
    variations = detector.detect_name_variations("Jeffrey Edward Epstein")
    
    assert "Jeffrey Epstein" in variations, "Should generate first+last"
    assert "Jeffrey" in variations, "Should generate first name"
    assert "Epstein" in variations, "Should generate last name"
    assert any("J." in v for v in variations), "Should generate initials"
    
    print("  ✓ Name variation generation works")
    print(f"  ✓ Generated {len(variations)} variations")
    
    # Test maiden name detection
    test_text = "Jane Doe (née Smith) married in 2000"
    maiden_names = detector.detect_maiden_name_pattern(test_text)
    
    assert len(maiden_names) > 0, "Should detect maiden names"
    assert maiden_names[0]['maiden_name'] == 'Smith', "Should extract maiden name"
    
    print("  ✓ Maiden name detection works")


def test_hidden_connection_finder():
    """Test hidden connection discovery"""
    from document_analyzer import HiddenConnectionFinder
    
    print("\nTesting Hidden Connection Finder...")
    
    finder = HiddenConnectionFinder()
    
    # Test child pattern detection
    test_text = """
    Jeffrey Epstein's daughter was born in 2003 according to records.
    The child, named Sarah, is mentioned in several documents.
    """
    
    children = finder.find_birth_patterns(test_text, "Jeffrey Epstein")
    
    assert len(children) > 0, "Should detect child patterns"
    assert any('daughter' in c['term'] for c in children), "Should detect daughter"
    
    print("  ✓ Child pattern detection works")
    print(f"  ✓ Found {len(children)} potential child patterns")
    
    # Test family relationship detection
    family = finder.find_family_relationships(test_text, "Jeffrey Epstein")
    
    assert len(family) > 0, "Should detect family relationships"
    
    print("  ✓ Family relationship detection works")


def test_document_analyzer():
    """Test complete document analysis"""
    from document_analyzer import DocumentAnalyzer
    
    print("\nTesting Document Analyzer...")
    
    analyzer = DocumentAnalyzer()
    
    test_doc = """
    Subject-1 traveled with [REDACTED] on flight logs from 2000-2005.
    Individual-A, formerly known as John Smith, changed his name in 2008.
    A child referred to as "M" appears in emails from 2004.
    Financial records show ███████ paid to Jane Doe (née Johnson).
    """
    
    results = analyzer.analyze_document(test_doc, entity_of_interest="Subject-1")
    
    assert results['redactions']['count'] > 0, "Should detect redactions"
    assert results['cryptic_identifiers']['count'] > 0, "Should detect cryptic IDs"
    assert len(results.get('maiden_names', [])) > 0, "Should detect maiden names"
    
    print("  ✓ Complete document analysis works")
    print(f"  ✓ Redactions: {results['redactions']['count']}")
    print(f"  ✓ Cryptic IDs: {results['cryptic_identifiers']['count']}")


def test_autonomous_updater():
    """Test autonomous update system"""
    from autonomous_updater import AutonomousUpdater
    
    print("\nTesting Autonomous Updater...")
    
    updater = AutonomousUpdater()
    
    test_doc = """
    Court documents reveal Jane Doe (née Smith) had a child in 2005.
    The individual known as "J.E." is mentioned in connection with Subject-A.
    [REDACTED] made payments totaling $500,000 in 2010.
    """
    
    updates = updater.process_new_document(
        test_doc,
        "Test Document",
        entity_of_interest="J.E."
    )
    
    assert 'new_aliases' in updates, "Should track new aliases"
    assert 'name_changes' in updates, "Should track name changes"
    assert 'redactions_found' in updates, "Should count redactions"
    
    print("  ✓ Document processing works")
    print(f"  ✓ Aliases: {len(updates['new_aliases'])}")
    print(f"  ✓ Redactions: {updates['redactions_found']}")


def test_redaction_context_analysis():
    """Test redaction context analysis"""
    from document_analyzer import RedactionDetector
    
    print("\nTesting Redaction Context Analysis...")
    
    detector = RedactionDetector()
    
    # Test name redaction
    text = "Mr. [REDACTED] attended the meeting"
    redactions = detector.detect_redactions(text)
    analysis = detector.analyze_redaction_context(redactions[0])
    
    assert analysis['likely_type'] == 'name', "Should detect name context"
    assert analysis['confidence'] > 0, "Should have confidence score"
    
    # Test amount redaction
    text = "Payment of $[REDACTED] was made"
    redactions = detector.detect_redactions(text)
    analysis = detector.analyze_redaction_context(redactions[0])
    
    assert analysis['likely_type'] == 'amount', "Should detect amount context"
    
    print("  ✓ Context analysis works")
    print("  ✓ Can infer redaction types")


def main():
    """Run all tests"""
    print("="*70)
    print("DOCUMENT ANALYSIS & AUTONOMOUS UPDATE - TEST SUITE")
    print("="*70)
    print()
    
    try:
        test_redaction_detection()
        test_cryptic_identifier_detection()
        test_name_variation_detection()
        test_hidden_connection_finder()
        test_document_analyzer()
        test_autonomous_updater()
        test_redaction_context_analysis()
        
        print("\n" + "="*70)
        print("ALL TESTS PASSED ✓")
        print("="*70)
        print()
        print("System verified:")
        print("  ✓ Redaction detection and analysis")
        print("  ✓ Cryptic identifier tracking")
        print("  ✓ Name variation detection")
        print("  ✓ Hidden connection discovery")
        print("  ✓ Document analysis pipeline")
        print("  ✓ Autonomous update system")
        print("  ✓ Context-aware analysis")
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
