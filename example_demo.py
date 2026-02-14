#!/usr/bin/env python3
"""
Example demonstration of the Investigation System
Shows how to add entities, evidence, and connections
"""

from investigation_system import InvestigationDatabase, Entity, Evidence, InvestigationAssistant
from network_analysis import NetworkAnalyzer
from data_collector import TimelineBuilder


def create_example_data():
    """Create example data to demonstrate the system"""
    print("="*60)
    print("Creating Example Investigation Data")
    print("="*60)
    print()
    
    # Initialize database
    db = InvestigationDatabase()
    db.load_from_file()
    
    # Add example entities
    print("Adding example entities...")
    
    # Add Jeffrey Epstein first (primary subject)
    jeffrey_epstein = Entity("Jeffrey Epstein", "person", {
        "role": "Primary Subject",
        "status": "Deceased",
        "date_of_death": "2019-08-10"
    })
    jeffrey_epstein.add_tag("primary_subject")
    jeffrey_epstein.add_tag("deceased")
    db.add_entity(jeffrey_epstein)
    
    # People
    entities_to_add = [
        Entity("Ghislaine Maxwell", "person", {
            "role": "Associate",
            "status": "Convicted"
        }),
        Entity("Prince Andrew", "person", {
            "role": "British Royal",
            "status": "Active"
        }),
        Entity("Bill Clinton", "person", {
            "role": "Former U.S. President",
            "status": "Active"
        }),
        Entity("Donald Trump", "person", {
            "role": "Former U.S. President, Businessman",
            "status": "Active"
        }),
        # Organizations
        Entity("The Clinton Foundation", "organization", {
            "type": "Non-profit",
            "location": "New York, USA"
        }),
        Entity("J. Epstein & Co.", "organization", {
            "type": "Financial Services",
            "location": "New York, USA"
        }),
        # Locations
        Entity("Little St. James Island", "location", {
            "type": "Private Island",
            "location": "U.S. Virgin Islands",
            "significance": "Epstein-owned property"
        }),
        Entity("Zorro Ranch", "location", {
            "type": "Ranch",
            "location": "New Mexico, USA",
            "significance": "Epstein-owned property"
        }),
        Entity("New York Mansion", "location", {
            "type": "Residence",
            "location": "Manhattan, New York",
            "significance": "Epstein-owned property"
        }),
    ]
    
    for entity in entities_to_add:
        if entity.entity_type == "person":
            entity.add_tag("individual")
        elif entity.entity_type == "organization":
            entity.add_tag("organization")
        elif entity.entity_type == "location":
            entity.add_tag("property")
        
        db.add_entity(entity)
    
    print(f"✓ Added {len(entities_to_add) + 1} entities (including Jeffrey Epstein)")
    
    # Add connections
    print("\nAdding example connections...")
    
    connections = [
        ("Jeffrey Epstein", "Ghislaine Maxwell", "close_associate", 1.0),
        ("Jeffrey Epstein", "Prince Andrew", "acquaintance", 0.9),
        ("Jeffrey Epstein", "Bill Clinton", "acquaintance", 0.85),
        ("Jeffrey Epstein", "Donald Trump", "acquaintance", 0.8),
        ("Jeffrey Epstein", "Little St. James Island", "owner", 1.0),
        ("Jeffrey Epstein", "Zorro Ranch", "owner", 1.0),
        ("Jeffrey Epstein", "New York Mansion", "owner", 1.0),
        ("Jeffrey Epstein", "J. Epstein & Co.", "founder", 1.0),
        ("Ghislaine Maxwell", "Prince Andrew", "acquaintance", 0.9),
        ("Bill Clinton", "The Clinton Foundation", "founder", 1.0),
    ]
    
    for entity1, entity2, relationship, confidence in connections:
        if entity1 in db.entities:
            db.entities[entity1].add_connection(entity2, relationship, confidence)
    
    print(f"✓ Added {len(connections)} connections")
    
    # Add example evidence
    print("\nAdding example evidence...")
    
    evidence_items = [
        Evidence(
            "EV001",
            "Flight Logs - Lolita Express",
            "Court Documents - Public Records",
            "Flight logs from Epstein's private jet showing passenger manifests "
            "and travel destinations to various locations including Little St. James Island."
        ),
        Evidence(
            "EV002",
            "2008 Plea Agreement",
            "U.S. District Court, Southern District of Florida",
            "Plea agreement in which Jeffrey Epstein pleaded guilty to state charges "
            "of solicitation of prostitution involving a minor."
        ),
        Evidence(
            "EV003",
            "2019 Federal Indictment",
            "U.S. District Court, Southern District of New York",
            "Federal indictment charging Jeffrey Epstein with sex trafficking "
            "of minors and conspiracy."
        ),
        Evidence(
            "EV004",
            "Maxwell Trial Testimony",
            "U.S. District Court, Southern District of New York",
            "Testimony from the trial of Ghislaine Maxwell regarding her relationship "
            "with Jeffrey Epstein and alleged criminal activities."
        ),
    ]
    
    for evidence in evidence_items:
        if "EV001" in evidence.evidence_id:
            evidence.add_related_entity("Jeffrey Epstein")
            evidence.add_related_entity("Bill Clinton")
            evidence.add_related_entity("Prince Andrew")
            evidence.add_tag("flight_logs")
            evidence.add_tag("transportation")
        elif "EV002" in evidence.evidence_id:
            evidence.add_related_entity("Jeffrey Epstein")
            evidence.add_tag("legal")
            evidence.add_tag("plea_agreement")
        elif "EV003" in evidence.evidence_id:
            evidence.add_related_entity("Jeffrey Epstein")
            evidence.add_tag("legal")
            evidence.add_tag("indictment")
        elif "EV004" in evidence.evidence_id:
            evidence.add_related_entity("Ghislaine Maxwell")
            evidence.add_related_entity("Jeffrey Epstein")
            evidence.add_tag("legal")
            evidence.add_tag("testimony")
        
        evidence.set_verification_status("verified")
        db.add_evidence(evidence)
    
    print(f"✓ Added {len(evidence_items)} evidence items")
    
    # Add timeline events
    print("\nAdding timeline events...")
    timeline = TimelineBuilder()
    
    timeline.add_event(
        "2008-06-30",
        "Epstein Plea Agreement",
        "Epstein pleads guilty to state charges in Florida",
        ["Jeffrey Epstein"],
        ["EV002"]
    )
    
    timeline.add_event(
        "2019-07-06",
        "Epstein Arrested",
        "Jeffrey Epstein arrested on federal sex trafficking charges",
        ["Jeffrey Epstein"],
        ["EV003"]
    )
    
    timeline.add_event(
        "2019-08-10",
        "Epstein Death",
        "Jeffrey Epstein found dead in jail cell",
        ["Jeffrey Epstein"],
        []
    )
    
    timeline.add_event(
        "2021-12-29",
        "Maxwell Convicted",
        "Ghislaine Maxwell convicted on five counts",
        ["Ghislaine Maxwell"],
        ["EV004"]
    )
    
    timeline.save_timeline()
    print(f"✓ Added timeline events")
    
    # Save database
    db.save_to_file()
    print("\n✓ All example data saved to database")
    print()
    
    return db


def demonstrate_features(db):
    """Demonstrate system features"""
    print("="*60)
    print("Demonstrating System Features")
    print("="*60)
    print()
    
    # Create assistant
    assistant = InvestigationAssistant(db)
    
    # 1. Investigation Summary
    print("1. INVESTIGATION SUMMARY")
    print("-" * 60)
    print(assistant.generate_investigation_summary())
    
    # 2. Entity Analysis
    print("\n2. ENTITY ANALYSIS - Jeffrey Epstein")
    print("-" * 60)
    print(assistant.analyze_entity("Jeffrey Epstein"))
    
    # 3. Search
    print("\n3. SEARCH FUNCTIONALITY")
    print("-" * 60)
    results = db.search_entities("Prince")
    print(f"Search for 'Prince': Found {len(results)} entities")
    for entity in results:
        print(f"  • {entity.name} ({entity.entity_type})")
    
    # 4. Network Analysis
    print("\n4. NETWORK ANALYSIS")
    print("-" * 60)
    analyzer = NetworkAnalyzer(db.entities, db.evidence)
    print(analyzer.generate_network_report())
    
    # 5. Connection Path
    print("\n5. CONNECTION PATH ANALYSIS")
    print("-" * 60)
    path = analyzer.find_shortest_path("Jeffrey Epstein", "The Clinton Foundation")
    if path:
        print(f"Path from Jeffrey Epstein to The Clinton Foundation:")
        print(f"  {' → '.join(path)}")
    
    # 6. Connection Strength
    print("\n6. CONNECTION STRENGTH ANALYSIS")
    print("-" * 60)
    strength = analyzer.analyze_connection_strength("Jeffrey Epstein", "Ghislaine Maxwell")
    print(f"Connection between Jeffrey Epstein and Ghislaine Maxwell:")
    print(f"  • Direct connection: {strength['direct_connection']}")
    print(f"  • Connection strength: {strength['connection_strength']:.3f}")
    print(f"  • Shared evidence: {strength['shared_evidence_count']} items")
    
    # 7. Investigation Gaps
    print("\n7. INVESTIGATION GAPS")
    print("-" * 60)
    gaps = assistant.find_investigation_gaps()
    if gaps:
        for gap in gaps:
            print(f"  • {gap}")
    else:
        print("  No significant gaps identified")
    
    print()


def main():
    """Main demonstration function"""
    print("\n" + "="*60)
    print("EPSTEIN INVESTIGATION SYSTEM - DEMONSTRATION")
    print("="*60)
    print()
    print("This demonstration will:")
    print("1. Create example entities, evidence, and connections")
    print("2. Demonstrate key system features")
    print("3. Show network analysis capabilities")
    print()
    
    input("Press Enter to continue...")
    print()
    
    # Create example data
    db = create_example_data()
    
    # Demonstrate features
    demonstrate_features(db)
    
    print("="*60)
    print("Demonstration Complete!")
    print("="*60)
    print()
    print("The example data has been saved to data/investigation_data.json")
    print()
    print("Next steps:")
    print("  • Run 'python3 cli.py' to explore the data interactively")
    print("  • Run 'python3 cli.py --summary' for a quick summary")
    print("  • Add your own entities and evidence")
    print("  • Perform network analysis on connections")
    print()


if __name__ == "__main__":
    main()
