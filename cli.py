#!/usr/bin/env python3
"""
Command-line interface for the Epstein Investigation System
Provides an interactive interface for investigators
"""

import sys
import json
from investigation_system import InvestigationDatabase, InvestigationAssistant, Entity, Evidence
from data_collector import DataCollector, TimelineBuilder, create_initial_data_structure
from network_analysis import NetworkAnalyzer, RelationshipMapper


class InvestigationCLI:
    """Command-line interface for the investigation system"""
    
    def __init__(self):
        self.db = InvestigationDatabase()
        self.assistant = InvestigationAssistant(self.db)
        self.collector = DataCollector()
        self.timeline = TimelineBuilder()
        
        # Load existing data
        self.db.load_from_file()
        self.timeline.load_timeline()
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("EPSTEIN INVESTIGATION SYSTEM - Main Menu")
        print("="*60)
        print("\n1. View Investigation Summary")
        print("2. Search Entities")
        print("3. Search Evidence")
        print("4. Analyze Entity")
        print("5. Add Entity")
        print("6. Add Evidence")
        print("7. Add Connection")
        print("8. Network Analysis")
        print("9. Export Report")
        print("10. Save & Exit")
        print("\n0. Exit without saving")
        print("="*60)
    
    def search_entities_interactive(self):
        """Interactive entity search"""
        query = input("\nEnter search query: ").strip()
        if not query:
            return
        
        results = self.db.search_entities(query)
        
        if not results:
            print(f"\nNo entities found matching '{query}'")
            return
        
        print(f"\nFound {len(results)} entities:")
        for i, entity in enumerate(results, 1):
            print(f"{i}. {entity.name} ({entity.entity_type}) - "
                  f"{len(entity.connections)} connections, "
                  f"{len(entity.evidence_ids)} evidence items")
    
    def search_evidence_interactive(self):
        """Interactive evidence search"""
        query = input("\nEnter search query: ").strip()
        if not query:
            return
        
        results = self.db.search_evidence(query)
        
        if not results:
            print(f"\nNo evidence found matching '{query}'")
            return
        
        print(f"\nFound {len(results)} evidence items:")
        for i, evidence in enumerate(results, 1):
            print(f"{i}. [{evidence.verification_status}] {evidence.title}")
            print(f"   Source: {evidence.source}")
            print(f"   Related entities: {', '.join(evidence.related_entities)}")
    
    def analyze_entity_interactive(self):
        """Interactive entity analysis"""
        entity_name = input("\nEnter entity name to analyze: ").strip()
        if not entity_name:
            return
        
        if entity_name not in self.db.entities:
            print(f"\nEntity '{entity_name}' not found. Searching...")
            results = self.db.search_entities(entity_name)
            if results:
                print("\nDid you mean:")
                for i, entity in enumerate(results[:5], 1):
                    print(f"{i}. {entity.name}")
                choice = input("\nSelect entity (1-5) or 0 to cancel: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= min(5, len(results)):
                    entity_name = results[int(choice)-1].name
                else:
                    return
            else:
                return
        
        analysis = self.assistant.analyze_entity(entity_name)
        print(analysis)
        
        # Show suggestions
        suggestions = self.assistant.suggest_connections(entity_name)
        if suggestions:
            print("\n--- Suggested Investigations ---")
            for suggestion in suggestions[:5]:
                print(f"  • {suggestion}")
    
    def add_entity_interactive(self):
        """Interactive entity addition"""
        print("\n--- Add New Entity ---")
        name = input("Entity name: ").strip()
        if not name:
            return
        
        print("\nEntity types: person, organization, location, event")
        entity_type = input("Entity type: ").strip() or "person"
        
        entity = Entity(name, entity_type)
        
        # Add tags
        tags_input = input("Tags (comma-separated, optional): ").strip()
        if tags_input:
            for tag in tags_input.split(','):
                entity.add_tag(tag.strip())
        
        self.db.add_entity(entity)
        print(f"\n✓ Entity '{name}' added successfully")
    
    def add_evidence_interactive(self):
        """Interactive evidence addition"""
        print("\n--- Add New Evidence ---")
        title = input("Evidence title: ").strip()
        if not title:
            return
        
        source = input("Source: ").strip()
        content = input("Content/Description: ").strip()
        
        evidence_id = f"EV{len(self.db.evidence) + 1:04d}"
        evidence = Evidence(evidence_id, title, source, content)
        
        # Add related entities
        entities_input = input("Related entities (comma-separated, optional): ").strip()
        if entities_input:
            for entity_name in entities_input.split(','):
                evidence.add_related_entity(entity_name.strip())
        
        # Add tags
        tags_input = input("Tags (comma-separated, optional): ").strip()
        if tags_input:
            for tag in tags_input.split(','):
                evidence.add_tag(tag.strip())
        
        self.db.add_evidence(evidence)
        print(f"\n✓ Evidence '{title}' added successfully (ID: {evidence_id})")
    
    def add_connection_interactive(self):
        """Interactive connection addition"""
        print("\n--- Add Connection ---")
        entity1 = input("From entity: ").strip()
        entity2 = input("To entity: ").strip()
        relationship = input("Relationship type: ").strip()
        
        if not entity1 or not entity2 or not relationship:
            print("\n✗ All fields are required")
            return
        
        if entity1 not in self.db.entities:
            print(f"\n✗ Entity '{entity1}' not found")
            return
        
        confidence_input = input("Confidence (0.0-1.0, default 1.0): ").strip()
        confidence = float(confidence_input) if confidence_input else 1.0
        
        self.db.entities[entity1].add_connection(entity2, relationship, confidence)
        print(f"\n✓ Connection added: {entity1} → {entity2} ({relationship})")
    
    def network_analysis_interactive(self):
        """Interactive network analysis"""
        print("\n--- Network Analysis ---")
        print("1. Find path between entities")
        print("2. Generate network report")
        print("3. Identify key connectors")
        
        choice = input("\nSelect option: ").strip()
        
        analyzer = NetworkAnalyzer(self.db.entities, self.db.evidence)
        
        if choice == '1':
            start = input("Start entity: ").strip()
            end = input("End entity: ").strip()
            
            path = analyzer.find_shortest_path(start, end)
            if path:
                print(f"\nShortest path: {' → '.join(path)}")
                
                # Show connection strength
                strength = analyzer.analyze_connection_strength(start, end)
                print(f"Connection strength: {strength['connection_strength']:.3f}")
                print(f"Shared evidence: {strength['shared_evidence_count']}")
            else:
                print(f"\nNo path found between {start} and {end}")
        
        elif choice == '2':
            print(analyzer.generate_network_report())
        
        elif choice == '3':
            connectors = analyzer.identify_key_connectors(15)
            print("\nTop Key Connectors:")
            for i, conn in enumerate(connectors, 1):
                print(f"{i}. {conn['name']} - Centrality: {conn['centrality_score']:.3f}")
    
    def export_report(self):
        """Export investigation report"""
        print("\n--- Export Report ---")
        filename = input("Report filename (default: investigation_report.json): ").strip()
        if not filename:
            filename = "investigation_report.json"
        
        report = self.db.generate_investigation_report()
        
        with open(f"data/reports/{filename}", 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Report exported to data/reports/{filename}")
    
    def run(self):
        """Run the CLI"""
        create_initial_data_structure()
        
        print("\nWelcome to the Epstein Investigation System")
        print("This system assists in tracking connections, evidence, and analysis")
        
        while True:
            self.show_menu()
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                print(self.assistant.generate_investigation_summary())
            elif choice == '2':
                self.search_entities_interactive()
            elif choice == '3':
                self.search_evidence_interactive()
            elif choice == '4':
                self.analyze_entity_interactive()
            elif choice == '5':
                self.add_entity_interactive()
            elif choice == '6':
                self.add_evidence_interactive()
            elif choice == '7':
                self.add_connection_interactive()
            elif choice == '8':
                self.network_analysis_interactive()
            elif choice == '9':
                self.export_report()
            elif choice == '10':
                self.db.save_to_file()
                self.timeline.save_timeline()
                print("\n✓ Data saved. Exiting...")
                break
            elif choice == '0':
                confirm = input("\nExit without saving? (y/n): ").strip().lower()
                if confirm == 'y':
                    print("\nExiting without saving...")
                    break
            else:
                print("\nInvalid option. Please try again.")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--summary':
        # Quick summary mode
        db = InvestigationDatabase()
        db.load_from_file()
        assistant = InvestigationAssistant(db)
        print(assistant.generate_investigation_summary())
    else:
        # Interactive mode
        cli = InvestigationCLI()
        cli.run()


if __name__ == "__main__":
    main()
