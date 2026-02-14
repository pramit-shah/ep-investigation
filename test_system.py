#!/usr/bin/env python3
"""
System Test - Validates all components work correctly
"""

def test_investigation_system():
    """Test the investigation system"""
    from investigation_system import InvestigationDatabase, Entity, Evidence, InvestigationAssistant
    
    db = InvestigationDatabase()
    
    # Test entity creation
    entity = Entity("Test Person", "person")
    entity.add_tag("test")
    db.add_entity(entity)
    
    # Test evidence creation
    evidence = Evidence("TEST001", "Test Evidence", "Test Source", "Test content")
    evidence.add_related_entity("Test Person")
    db.add_evidence(evidence)
    
    # Test search
    results = db.search_entities("Test")
    assert len(results) > 0, "Search failed"
    
    # Test assistant
    assistant = InvestigationAssistant(db)
    summary = assistant.generate_investigation_summary()
    assert "Test Person" in summary or "Total Entities" in summary, "Summary failed"
    
    print("✓ Investigation System test passed")

def test_network_analysis():
    """Test network analysis"""
    from investigation_system import InvestigationDatabase, Entity
    from network_analysis import NetworkAnalyzer
    
    db = InvestigationDatabase()
    
    # Create test entities
    e1 = Entity("Person A", "person")
    e1.add_connection("Person B", "friend")
    db.add_entity(e1)
    
    e2 = Entity("Person B", "person")
    db.add_entity(e2)
    
    # Test analyzer
    analyzer = NetworkAnalyzer(db.entities, db.evidence)
    path = analyzer.find_shortest_path("Person A", "Person B")
    assert len(path) == 2, f"Path should be 2, got {len(path)}"
    
    print("✓ Network Analysis test passed")

def test_data_collector():
    """Test data collector"""
    from data_collector import DataCollector, TimelineBuilder
    
    collector = DataCollector()
    template = collector.create_evidence_template()
    assert 'title' in template, "Template missing title"
    
    timeline = TimelineBuilder()
    timeline.add_event("2020-01-01", "Test Event", "Description", ["Entity"])
    events = timeline.get_timeline()
    assert len(events) > 0, "Timeline failed"
    
    print("✓ Data Collector test passed")

def main():
    """Run all tests"""
    print("="*60)
    print("Running System Tests")
    print("="*60)
    print()
    
    try:
        test_investigation_system()
        test_network_analysis()
        test_data_collector()
        
        print()
        print("="*60)
        print("All Tests Passed!")
        print("="*60)
        return 0
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
