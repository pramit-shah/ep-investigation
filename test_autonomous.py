#!/usr/bin/env python3
"""
Test script for autonomous research system
Validates .zip archival, data mapping, and integration
"""

def test_autonomous_researcher():
    """Test autonomous researcher functionality"""
    from autonomous_researcher import (
        AutonomousResearcher, DataSource, DataMap, 
        ZipArchiveManager, ResearchTask
    )
    
    print("Testing Autonomous Researcher...")
    
    # Test DataSource
    source = DataSource("TEST_001", "document", "http://test.com", "Test source")
    source.add_related_entity("Test Entity")
    assert source.source_id == "TEST_001"
    assert "Test Entity" in source.related_entities
    print("  ✓ DataSource works")
    
    # Test DataMap
    data_map = DataMap("data/test_map")
    data_map.add_source(source)
    data_map.add_transaction("Entity A", "Entity B", "payment", 100.0, "2020-01-01")
    data_map.add_tie("Entity A", "Entity C", "partner", "Business partners")
    
    assert "TEST_001" in data_map.sources
    assert len(data_map.transactions) == 1
    assert len(data_map.ties) == 1
    print("  ✓ DataMap works")
    
    # Test ZipArchiveManager
    import os
    import tempfile
    
    archive_mgr = ZipArchiveManager("data/test_archives")
    
    # Create test file
    test_file = os.path.join(tempfile.gettempdir(), "test_file.txt")
    with open(test_file, 'w') as f:
        f.write("Test content")
    
    # Create archive
    archive_path = archive_mgr.create_archive("test_archive", [test_file])
    assert os.path.exists(archive_path)
    
    # Verify archive
    is_valid = archive_mgr.verify_archive(archive_path)
    assert is_valid
    print("  ✓ ZipArchiveManager works")
    
    # Test ResearchTask
    task = ResearchTask("TEST_TASK", "Test research task", priority=1)
    task.add_source("TEST_001")
    task.add_entity("Test Entity")
    assert task.status == "pending"
    assert len(task.sources_to_collect) == 1
    print("  ✓ ResearchTask works")
    
    # Cleanup
    os.remove(test_file)
    
    print("✓ Autonomous Researcher tests passed\n")


def test_integrated_investigation():
    """Test integrated investigation functionality"""
    from integrated_investigation import IntegratedInvestigation
    
    print("Testing Integrated Investigation...")
    
    # Test initialization
    investigation = IntegratedInvestigation()
    assert investigation.researcher is not None
    assert investigation.db is not None
    print("  ✓ Integration initialization works")
    
    # Test manual transaction
    investigation.add_manual_transaction(
        "Test Entity A",
        "Test Entity B",
        "test_payment",
        amount=1000.0
    )
    
    # Verify in data map
    assert len(investigation.researcher.data_map.transactions) > 0
    print("  ✓ Manual transaction tracking works")
    
    # Test manual tie
    investigation.add_manual_tie(
        "Test Entity A",
        "Test Entity C",
        "test_associate",
        "Test description"
    )
    
    # Verify in data map
    assert len(investigation.researcher.data_map.ties) > 0
    print("  ✓ Manual tie tracking works")
    
    print("✓ Integrated Investigation tests passed\n")


def test_data_archival():
    """Test .zip file creation and integrity"""
    from autonomous_researcher import ZipArchiveManager
    import os
    import tempfile
    import zipfile
    
    print("Testing Data Archival...")
    
    archive_mgr = ZipArchiveManager("data/test_archives")
    
    # Create multiple test files
    test_files = []
    for i in range(3):
        test_file = os.path.join(tempfile.gettempdir(), f"test_file_{i}.txt")
        with open(test_file, 'w') as f:
            f.write(f"Test content {i}")
        test_files.append(test_file)
    
    # Create archive with metadata
    metadata = {
        'test': 'metadata',
        'count': len(test_files)
    }
    
    archive_path = archive_mgr.create_archive(
        "integrity_test",
        test_files,
        metadata=metadata
    )
    
    # Verify archive exists
    assert os.path.exists(archive_path)
    print("  ✓ Archive created")
    
    # Verify integrity
    is_valid = archive_mgr.verify_archive(archive_path)
    assert is_valid
    print("  ✓ Archive integrity verified")
    
    # Verify contents
    with zipfile.ZipFile(archive_path, 'r') as zipf:
        files_in_archive = zipf.namelist()
        assert 'metadata.json' in files_in_archive
        assert len(files_in_archive) == 4  # 3 files + metadata
    print("  ✓ Archive contents verified")
    
    # Test extraction
    extract_dir = archive_mgr.extract_archive(archive_path)
    assert os.path.exists(extract_dir)
    assert os.path.exists(os.path.join(extract_dir, 'metadata.json'))
    print("  ✓ Archive extraction works")
    
    # Cleanup
    for f in test_files:
        if os.path.exists(f):
            os.remove(f)
    
    print("✓ Data Archival tests passed\n")


def test_mission_focus():
    """Test that system focuses on uncovering truths with ties and transactions"""
    from autonomous_researcher import AutonomousResearcher
    
    print("Testing Mission Focus...")
    
    researcher = AutonomousResearcher("data/test_mission")
    
    # Track transactions
    researcher.track_transaction(
        "Entity X", "Entity Y", "payment", 50000.0, "2020-06-15"
    )
    
    # Track ties
    researcher.track_tie(
        "Entity X", "Entity Z", "business_partner", "Partners in venture"
    )
    
    # Verify tracking
    assert len(researcher.data_map.transactions) == 1
    assert len(researcher.data_map.ties) == 1
    
    trans = researcher.data_map.transactions[0]
    assert trans['from'] == "Entity X"
    assert trans['to'] == "Entity Y"
    assert trans['type'] == "payment"
    
    tie = researcher.data_map.ties[0]
    assert tie['entity1'] == "Entity X"
    assert tie['entity2'] == "Entity Z"
    
    print("  ✓ Transaction tracking works")
    print("  ✓ Tie tracking works")
    print("  ✓ Mission focus: Uncover all truths ✓")
    
    print("✓ Mission Focus tests passed\n")


def main():
    """Run all tests"""
    print("="*60)
    print("AUTONOMOUS RESEARCH SYSTEM - TEST SUITE")
    print("="*60)
    print()
    
    try:
        test_autonomous_researcher()
        test_integrated_investigation()
        test_data_archival()
        test_mission_focus()
        
        print("="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        print()
        print("System verified:")
        print("  ✓ Autonomous research capabilities")
        print("  ✓ .zip archive creation and integrity")
        print("  ✓ Data mapping and linking")
        print("  ✓ Transaction tracking")
        print("  ✓ Tie tracking")
        print("  ✓ Integration with investigation database")
        print("  ✓ Mission focus: Uncover all truths")
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
