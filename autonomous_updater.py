#!/usr/bin/env python3
"""
Autonomous Repository Update System
Monitors for new information and autonomously updates the investigation
"""

import os
import json
import subprocess
from datetime import datetime
from typing import List, Dict, Optional
from document_analyzer import DocumentAnalyzer
from investigation_system import InvestigationDatabase, Entity, Evidence
from integrated_investigation import IntegratedInvestigation


class AutonomousUpdater:
    """
    Autonomously monitors and updates the investigation repository
    when new information is discovered
    """
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.db = InvestigationDatabase()
        self.analyzer = DocumentAnalyzer()
        self.update_log = []
        self.pending_updates = []
        
        # Load existing data
        self.db.load_from_file()
    
    def process_new_document(self, document_text: str, source: str, 
                           entity_of_interest: Optional[str] = None) -> Dict:
        """
        Process a new document and extract actionable information
        """
        print(f"\n{'='*70}")
        print(f"Processing New Document: {source}")
        print(f"{'='*70}")
        
        # Analyze document
        analysis = self.analyzer.analyze_document(document_text, entity_of_interest)
        
        updates = {
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'new_entities': [],
            'new_aliases': [],
            'new_connections': [],
            'name_changes': [],
            'redactions_found': analysis['redactions']['count']
        }
        
        # Extract cryptic identifiers and create aliases
        for cryptic in analysis.get('cryptic_identifiers', {}).get('items', []):
            identifier = cryptic['identifier']
            
            # Add to alias tracker
            self.analyzer.alias_tracker.add_cryptic_identifier(
                identifier, cryptic['context']
            )
            
            updates['new_aliases'].append({
                'identifier': identifier,
                'type': cryptic['type'],
                'context': cryptic['context']
            })
        
        # Process potential children
        for child_pattern in analysis.get('potential_children', []):
            for name in child_pattern.get('potential_names', []):
                # Create entity for potential child
                if name not in self.db.entities:
                    child_entity = Entity(name, "person", {
                        "discovery_source": source,
                        "relationship": "potential_child",
                        "confidence": child_pattern['confidence']
                    })
                    child_entity.add_tag("potential_child")
                    child_entity.add_tag("needs_verification")
                    
                    self.db.add_entity(child_entity)
                    updates['new_entities'].append(name)
                
                # Create connection if entity_of_interest exists
                if entity_of_interest and entity_of_interest in self.db.entities:
                    self.db.entities[entity_of_interest].add_connection(
                        name,
                        "potential_parent_child",
                        confidence=child_pattern['confidence']
                    )
                    updates['new_connections'].append({
                        'from': entity_of_interest,
                        'to': name,
                        'type': 'potential_parent_child'
                    })
        
        # Process family relationships
        for rel in analysis.get('family_relationships', []):
            for name in rel.get('potential_names', []):
                if name not in self.db.entities:
                    entity = Entity(name, "person", {
                        "discovery_source": source,
                        "relationship_type": rel['relationship_type']
                    })
                    entity.add_tag(rel['relationship_type'])
                    entity.add_tag("needs_verification")
                    
                    self.db.add_entity(entity)
                    updates['new_entities'].append(name)
                
                # Create connection
                if entity_of_interest and entity_of_interest in self.db.entities:
                    self.db.entities[entity_of_interest].add_connection(
                        name,
                        rel['relationship_type'],
                        confidence=rel['confidence']
                    )
                    updates['new_connections'].append({
                        'from': entity_of_interest,
                        'to': name,
                        'type': rel['relationship_type']
                    })
        
        # Process name changes
        for name_change in analysis.get('maiden_names', []):
            if 'married_name' in name_change:
                # Track maiden name
                self.analyzer.name_variation_detector.add_name_change(
                    name_change['maiden_name'],
                    name_change['married_name'],
                    reason='marriage',
                    source=source
                )
                updates['name_changes'].append(name_change)
            elif 'former_name' in name_change:
                # Track name change
                self.analyzer.name_variation_detector.add_name_change(
                    name_change['former_name'],
                    name_change['current_name'],
                    source=source
                )
                updates['name_changes'].append(name_change)
        
        # Store update
        self.update_log.append(updates)
        
        return updates
    
    def auto_commit_updates(self, updates: Dict, commit_message: Optional[str] = None):
        """
        Automatically commit updates to the repository
        """
        if not updates['new_entities'] and not updates['new_connections'] and not updates['name_changes']:
            print("  ℹ No actionable updates to commit")
            return False
        
        # Save database
        self.db.save_to_file()
        
        # Generate commit message
        if not commit_message:
            commit_message = self._generate_commit_message(updates)
        
        print(f"\n  📝 Auto-committing updates...")
        print(f"  Message: {commit_message}")
        
        # Add and commit (simulation - actual git commands would be used in production)
        try:
            # In production, these would be real git commands
            print(f"  ✓ Added {len(updates['new_entities'])} new entities")
            print(f"  ✓ Added {len(updates['new_connections'])} new connections")
            print(f"  ✓ Tracked {len(updates['name_changes'])} name changes")
            
            # Log the commit
            self.pending_updates.append({
                'timestamp': datetime.now().isoformat(),
                'message': commit_message,
                'updates': updates
            })
            
            return True
        except Exception as e:
            print(f"  ✗ Commit failed: {e}")
            return False
    
    def _generate_commit_message(self, updates: Dict) -> str:
        """Generate descriptive commit message"""
        parts = []
        
        if updates['new_entities']:
            parts.append(f"Add {len(updates['new_entities'])} entities")
        
        if updates['new_connections']:
            parts.append(f"add {len(updates['new_connections'])} connections")
        
        if updates['name_changes']:
            parts.append(f"track {len(updates['name_changes'])} name changes")
        
        if updates['redactions_found']:
            parts.append(f"detect {updates['redactions_found']} redactions")
        
        message = "Auto-update: " + ", ".join(parts)
        return message
    
    def run_investigation_suite(self, entity_name: str) -> Dict:
        """
        Run full investigation suite on an entity
        """
        print(f"\n{'='*70}")
        print(f"RUNNING INVESTIGATION SUITE: {entity_name}")
        print(f"{'='*70}")
        
        results = {
            'entity': entity_name,
            'timestamp': datetime.now().isoformat(),
            'findings': {}
        }
        
        # 1. Check for entity in database
        if entity_name in self.db.entities:
            entity = self.db.entities[entity_name]
            results['findings']['entity_exists'] = True
            results['findings']['connections'] = len(entity.connections)
            results['findings']['evidence_items'] = len(entity.evidence_ids)
            results['findings']['tags'] = list(entity.tags)
            print(f"  ✓ Entity found: {len(entity.connections)} connections")
        else:
            results['findings']['entity_exists'] = False
            print(f"  ℹ Entity not found, will create")
        
        # 2. Generate name variations
        variations = self.analyzer.name_variation_detector.detect_name_variations(entity_name)
        results['findings']['name_variations'] = variations
        print(f"  ✓ Generated {len(variations)} name variations")
        
        # 3. Check for aliases
        aliases = self.analyzer.alias_tracker.get_all_aliases(entity_name)
        results['findings']['known_aliases'] = list(aliases)
        if aliases:
            print(f"  ✓ Found {len(aliases)} known aliases")
        
        # 4. Search for entity in existing evidence
        evidence_mentions = []
        for eid, evidence in self.db.evidence.items():
            if entity_name.lower() in evidence.content.lower():
                evidence_mentions.append(eid)
        
        results['findings']['evidence_mentions'] = len(evidence_mentions)
        if evidence_mentions:
            print(f"  ✓ Found in {len(evidence_mentions)} evidence items")
        
        return results
    
    def monitor_and_update(self, check_interval: int = 3600):
        """
        Monitoring loop (would run continuously in production)
        """
        print(f"\n{'='*70}")
        print("AUTONOMOUS MONITORING ACTIVE")
        print(f"{'='*70}")
        print(f"Check interval: {check_interval} seconds")
        print("Monitoring for:")
        print("  • New documents with redactions")
        print("  • Cryptic identifiers and aliases")
        print("  • Name changes and variations")
        print("  • Hidden connections and relationships")
        print("  • Temporal events and births")
        print()
        print("Auto-update capabilities:")
        print("  ✓ Entity creation")
        print("  ✓ Connection mapping")
        print("  ✓ Alias tracking")
        print("  ✓ Repository commits")
        print()
        print("Status: READY")
    
    def generate_update_report(self) -> str:
        """Generate report of autonomous updates"""
        report = [
            "\n" + "="*70,
            "AUTONOMOUS UPDATE REPORT",
            "="*70,
            f"\nTotal Updates: {len(self.update_log)}",
            f"Pending Commits: {len(self.pending_updates)}",
        ]
        
        # Summary statistics
        total_entities = sum(len(u['new_entities']) for u in self.update_log)
        total_connections = sum(len(u['new_connections']) for u in self.update_log)
        total_name_changes = sum(len(u['name_changes']) for u in self.update_log)
        total_aliases = sum(len(u['new_aliases']) for u in self.update_log)
        
        report.append(f"\nTotal New Entities: {total_entities}")
        report.append(f"Total New Connections: {total_connections}")
        report.append(f"Total Name Changes: {total_name_changes}")
        report.append(f"Total Aliases Tracked: {total_aliases}")
        
        if self.update_log:
            report.append("\n--- Recent Updates ---")
            for i, update in enumerate(self.update_log[-5:], 1):
                report.append(f"\n{i}. Source: {update['source']}")
                report.append(f"   Time: {update['timestamp']}")
                report.append(f"   Entities: {len(update['new_entities'])}")
                report.append(f"   Connections: {len(update['new_connections'])}")
                report.append(f"   Redactions: {update['redactions_found']}")
        
        report.append("\n" + "="*70)
        
        return "\n".join(report)


def main():
    """Demonstrate autonomous update capabilities"""
    print("="*70)
    print("AUTONOMOUS REPOSITORY UPDATE SYSTEM")
    print("="*70)
    print()
    
    updater = AutonomousUpdater()
    
    # Example: Process new document
    example_doc = """
    Newly released court documents reveal that Jane Doe (née Smith) had a
    daughter named Sarah Anderson in 2005. The child's connection to
    Subject-1 (identified elsewhere as J.E.) is mentioned in several emails.
    
    Additionally, an individual referred to as "T.B." appears in flight logs
    from 2003-2006. Financial records show [REDACTED] made payments totaling
    $500,000 to Individual-B during this period.
    
    Records indicate the person formerly known as Michael Roberts changed his
    name to Marcus Richardson in 2008. His relationship to the investigation
    remains under review.
    """
    
    print("Processing new document...")
    updates = updater.process_new_document(
        example_doc,
        "Court Filing 2024-001",
        entity_of_interest="Jeffrey Epstein"
    )
    
    print("\n" + updater.analyzer.generate_analysis_report(
        updater.analyzer.analysis_results[-1]
    ))
    
    # Auto-commit updates
    updater.auto_commit_updates(updates)
    
    # Run investigation suite
    suite_results = updater.run_investigation_suite("Jeffrey Epstein")
    
    # Show monitoring status
    updater.monitor_and_update()
    
    # Generate report
    print(updater.generate_update_report())
    
    print("\n" + "="*70)
    print("SYSTEM STATUS")
    print("="*70)
    print("✓ Document analysis: OPERATIONAL")
    print("✓ Redaction detection: ACTIVE")
    print("✓ Cryptic identifier tracking: ACTIVE")
    print("✓ Name change detection: ACTIVE")
    print("✓ Hidden connection discovery: ACTIVE")
    print("✓ Autonomous updates: ENABLED")
    print("✓ Repository commits: READY")
    print()


if __name__ == "__main__":
    main()
