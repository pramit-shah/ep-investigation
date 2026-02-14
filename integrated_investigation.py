#!/usr/bin/env python3
"""
Integration module connecting autonomous researcher with investigation system
Ensures continuous tracking of ties and transactions
"""

from autonomous_researcher import AutonomousResearcher, DataSource
from investigation_system import InvestigationDatabase, Entity, Evidence
from typing import List, Dict, Optional


class IntegratedInvestigation:
    """
    Integrates autonomous research with manual investigation
    Synchronizes data between systems
    """
    
    def __init__(self):
        self.researcher = AutonomousResearcher()
        self.db = InvestigationDatabase()
        
        # Load existing data
        self.db.load_from_file()
        self.researcher.data_map.load_map()
    
    def sync_data_to_investigation_db(self):
        """
        Sync data from autonomous research to investigation database
        """
        print("\n" + "="*60)
        print("Syncing Autonomous Research → Investigation Database")
        print("="*60)
        
        synced_entities = 0
        synced_evidence = 0
        synced_connections = 0
        
        # Sync collected sources as evidence
        for source_id, source in self.researcher.data_map.sources.items():
            if source.collected:
                # Create evidence from collected source
                evidence = Evidence(
                    source.source_id,
                    f"{source.source_type.upper()}: {source.description}",
                    source.url,
                    f"Autonomously collected on {source.collection_date}\n"
                    f"File: {source.file_path}\n"
                    f"Checksum: {source.checksum}"
                )
                
                # Add related entities
                for entity_name in source.related_entities:
                    evidence.add_related_entity(entity_name)
                    
                    # Ensure entity exists
                    if entity_name not in self.db.entities:
                        entity = Entity(entity_name, "person")
                        entity.add_tag("autonomous_research")
                        self.db.add_entity(entity)
                        synced_entities += 1
                
                evidence.add_tag("autonomous_collection")
                evidence.add_tag(source.source_type)
                evidence.set_verification_status("unverified")  # Needs manual verification
                
                self.db.add_evidence(evidence)
                synced_evidence += 1
        
        # Sync transactions as connections
        for transaction in self.researcher.data_map.transactions:
            from_entity = transaction['from']
            to_entity = transaction['to']
            
            # Ensure both entities exist
            for entity_name in [from_entity, to_entity]:
                if entity_name not in self.db.entities:
                    entity = Entity(entity_name, "person")
                    entity.add_tag("transaction_party")
                    self.db.add_entity(entity)
                    synced_entities += 1
            
            # Add connection
            if from_entity in self.db.entities:
                relationship = f"transaction_{transaction['type']}"
                self.db.entities[from_entity].add_connection(
                    to_entity,
                    relationship,
                    confidence=0.8  # Transactions are fairly reliable
                )
                synced_connections += 1
        
        # Sync ties as connections
        for tie in self.researcher.data_map.ties:
            entity1 = tie['entity1']
            entity2 = tie['entity2']
            
            # Ensure both entities exist
            for entity_name in [entity1, entity2]:
                if entity_name not in self.db.entities:
                    entity = Entity(entity_name, "person")
                    entity.add_tag("connected_entity")
                    self.db.add_entity(entity)
                    synced_entities += 1
            
            # Add bidirectional connection
            if entity1 in self.db.entities:
                self.db.entities[entity1].add_connection(
                    entity2,
                    tie['type'],
                    confidence=0.7  # Ties need verification
                )
                synced_connections += 1
        
        # Save updated database
        self.db.save_to_file()
        
        print(f"\n✓ Synced {synced_entities} entities")
        print(f"✓ Synced {synced_evidence} evidence items")
        print(f"✓ Synced {synced_connections} connections")
        print("\n" + "="*60)
    
    def start_autonomous_research_cycle(self, max_tasks: Optional[int] = None):
        """
        Run a complete autonomous research cycle
        1. Run autonomous research
        2. Sync data to investigation database
        3. Generate reports
        """
        print("\n" + "="*60)
        print("INTEGRATED INVESTIGATION - AUTONOMOUS CYCLE")
        print("="*60)
        print("\nMission: Uncover all truths with continuous ties and transactions")
        
        # Check if research needs initialization
        if not self.researcher.research_tasks:
            print("\nInitializing autonomous research targets...")
            self.researcher.initialize_research_targets()
        
        # Run autonomous research
        print("\nPhase 1: Autonomous Data Collection")
        print("-" * 60)
        self.researcher.run_autonomous_research(max_tasks=max_tasks)
        
        # Sync to investigation database
        print("\nPhase 2: Data Integration")
        print("-" * 60)
        self.sync_data_to_investigation_db()
        
        # Generate comprehensive report
        print("\nPhase 3: Report Generation")
        print("-" * 60)
        print(self.researcher.generate_research_report())
        
        print("\n" + "="*60)
        print("AUTONOMOUS RESEARCH CYCLE COMPLETE")
        print("="*60)
        print("\nAll collected data:")
        print(f"  • Stored in .zip archives: data/autonomous/archives/")
        print(f"  • Mapped in: data/autonomous/collected/data_map.json")
        print(f"  • Integrated into: data/investigation_data.json")
        print("\nUse 'python3 cli.py' to explore the integrated investigation data")
    
    def add_manual_transaction(self, from_entity: str, to_entity: str,
                              transaction_type: str, amount: Optional[float] = None,
                              date: Optional[str] = None, source_id: Optional[str] = None):
        """
        Manually add a transaction to track
        Syncs to both systems
        """
        # Add to autonomous researcher
        self.researcher.track_transaction(
            from_entity, to_entity, transaction_type, amount, date, source_id
        )
        
        # Add to investigation database as connection
        if from_entity not in self.db.entities:
            entity = Entity(from_entity, "person")
            self.db.add_entity(entity)
        
        if to_entity not in self.db.entities:
            entity = Entity(to_entity, "person")
            self.db.add_entity(entity)
        
        self.db.entities[from_entity].add_connection(
            to_entity,
            f"transaction_{transaction_type}",
            confidence=0.9
        )
        
        # Save both systems
        self.researcher.data_map.save_map()
        self.db.save_to_file()
        
        print(f"✓ Tracked transaction: {from_entity} → {to_entity} ({transaction_type})")
    
    def add_manual_tie(self, entity1: str, entity2: str, tie_type: str,
                      description: str, source_id: Optional[str] = None):
        """
        Manually add a tie/connection to track
        Syncs to both systems
        """
        # Add to autonomous researcher
        self.researcher.track_tie(entity1, entity2, tie_type, description, source_id)
        
        # Add to investigation database as connection
        if entity1 not in self.db.entities:
            entity = Entity(entity1, "person")
            self.db.add_entity(entity)
        
        if entity2 not in self.db.entities:
            entity = Entity(entity2, "person")
            self.db.add_entity(entity)
        
        self.db.entities[entity1].add_connection(entity2, tie_type, confidence=0.8)
        
        # Save both systems
        self.researcher.data_map.save_map()
        self.db.save_to_file()
        
        print(f"✓ Tracked tie: {entity1} ↔ {entity2} ({tie_type})")


def main():
    """Main function demonstrating integrated investigation"""
    print("="*60)
    print("INTEGRATED INVESTIGATION SYSTEM")
    print("Autonomous Research + Manual Investigation")
    print("="*60)
    
    # Create integrated investigation
    investigation = IntegratedInvestigation()
    
    # Run autonomous research cycle
    investigation.start_autonomous_research_cycle(max_tasks=5)
    
    # Example: Add manual transactions and ties
    print("\n" + "="*60)
    print("Example: Adding Manual Transactions & Ties")
    print("="*60)
    
    investigation.add_manual_transaction(
        "Jeffrey Epstein",
        "Ghislaine Maxwell",
        "payment",
        amount=100000.0,
        date="2010-05-15"
    )
    
    investigation.add_manual_tie(
        "Jeffrey Epstein",
        "Unknown Associate",
        "business_partner",
        "Identified through flight logs"
    )
    
    print("\n✓ Integration complete. All data synchronized.")


if __name__ == "__main__":
    main()
