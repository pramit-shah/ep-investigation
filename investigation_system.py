#!/usr/bin/env python3
"""
Epstein Investigation AI System
Assists in tracking connections, gathering evidence, and connecting dots in the investigation
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Set, Optional
from collections import defaultdict


class Entity:
    """Represents a person, organization, or location in the investigation"""
    
    def __init__(self, name: str, entity_type: str, metadata: Optional[Dict] = None):
        self.name = name
        self.entity_type = entity_type  # person, organization, location, event
        self.metadata = metadata or {}
        self.connections = []
        self.evidence_ids = []
        self.tags = set()
    
    def add_connection(self, other_entity: str, relationship: str, confidence: float = 1.0):
        """Add a connection to another entity"""
        self.connections.append({
            'entity': other_entity,
            'relationship': relationship,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_evidence(self, evidence_id: str):
        """Link evidence to this entity"""
        if evidence_id not in self.evidence_ids:
            self.evidence_ids.append(evidence_id)
    
    def add_tag(self, tag: str):
        """Add a tag for categorization"""
        self.tags.add(tag)
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            'name': self.name,
            'type': self.entity_type,
            'metadata': self.metadata,
            'connections': self.connections,
            'evidence_ids': self.evidence_ids,
            'tags': list(self.tags)
        }


class Evidence:
    """Represents a piece of evidence in the investigation"""
    
    def __init__(self, evidence_id: str, title: str, source: str, content: str):
        self.evidence_id = evidence_id
        self.title = title
        self.source = source
        self.content = content
        self.date_added = datetime.now().isoformat()
        self.related_entities = []
        self.tags = set()
        self.verification_status = "unverified"
        self.metadata = {}
    
    def add_related_entity(self, entity_name: str):
        """Link an entity to this evidence"""
        if entity_name not in self.related_entities:
            self.related_entities.append(entity_name)
    
    def set_verification_status(self, status: str):
        """Set verification status: verified, unverified, disputed"""
        self.verification_status = status
    
    def add_tag(self, tag: str):
        """Add a tag for categorization"""
        self.tags.add(tag)
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            'id': self.evidence_id,
            'title': self.title,
            'source': self.source,
            'content': self.content,
            'date_added': self.date_added,
            'related_entities': self.related_entities,
            'tags': list(self.tags),
            'verification_status': self.verification_status,
            'metadata': self.metadata
        }


class InvestigationDatabase:
    """Main investigation database for tracking all entities and evidence"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.entities: Dict[str, Entity] = {}
        self.evidence: Dict[str, Evidence] = {}
        self.timeline = []
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
    def add_entity(self, entity: Entity):
        """Add or update an entity in the database"""
        self.entities[entity.name] = entity
    
    def add_evidence(self, evidence: Evidence):
        """Add evidence to the database"""
        self.evidence[evidence.evidence_id] = evidence
        
        # Automatically link entities mentioned in evidence
        for entity_name in evidence.related_entities:
            if entity_name in self.entities:
                self.entities[entity_name].add_evidence(evidence.evidence_id)
    
    def find_connections(self, entity_name: str, max_depth: int = 2) -> Dict:
        """Find all connections to an entity up to max_depth"""
        if entity_name not in self.entities:
            return {}
        
        visited = set()
        connections = defaultdict(list)
        
        def traverse(name: str, depth: int, path: List[str]):
            if depth > max_depth or name in visited:
                return
            
            visited.add(name)
            
            if name in self.entities:
                entity = self.entities[name]
                for conn in entity.connections:
                    connected_entity = conn['entity']
                    new_path = path + [connected_entity]
                    connections[connected_entity].append({
                        'path': new_path,
                        'relationship': conn['relationship'],
                        'depth': depth,
                        'confidence': conn.get('confidence', 1.0)
                    })
                    traverse(connected_entity, depth + 1, new_path)
        
        traverse(entity_name, 0, [entity_name])
        return dict(connections)
    
    def search_entities(self, query: str, entity_type: Optional[str] = None) -> List[Entity]:
        """Search for entities by name or tags"""
        results = []
        query_lower = query.lower()
        
        for entity in self.entities.values():
            if entity_type and entity.entity_type != entity_type:
                continue
            
            if (query_lower in entity.name.lower() or 
                any(query_lower in tag.lower() for tag in entity.tags)):
                results.append(entity)
        
        return results
    
    def search_evidence(self, query: str) -> List[Evidence]:
        """Search evidence by content, title, or tags"""
        results = []
        query_lower = query.lower()
        
        for evidence in self.evidence.values():
            if (query_lower in evidence.title.lower() or 
                query_lower in evidence.content.lower() or
                any(query_lower in tag.lower() for tag in evidence.tags)):
                results.append(evidence)
        
        return results
    
    def get_entity_network(self, entity_name: str) -> Dict:
        """Get complete network information for an entity"""
        if entity_name not in self.entities:
            return {}
        
        entity = self.entities[entity_name]
        connections = self.find_connections(entity_name, max_depth=3)
        
        # Get all related evidence
        evidence_list = [
            self.evidence[eid].to_dict() 
            for eid in entity.evidence_ids 
            if eid in self.evidence
        ]
        
        return {
            'entity': entity.to_dict(),
            'connections': connections,
            'evidence': evidence_list,
            'connection_count': len(connections),
            'evidence_count': len(evidence_list)
        }
    
    def generate_investigation_report(self) -> Dict:
        """Generate a comprehensive investigation report"""
        return {
            'report_date': datetime.now().isoformat(),
            'total_entities': len(self.entities),
            'total_evidence': len(self.evidence),
            'entity_breakdown': self._get_entity_breakdown(),
            'high_connection_entities': self._get_high_connection_entities(),
            'verification_status': self._get_verification_breakdown(),
            'recent_additions': self._get_recent_additions()
        }
    
    def _get_entity_breakdown(self) -> Dict[str, int]:
        """Get count of entities by type"""
        breakdown = defaultdict(int)
        for entity in self.entities.values():
            breakdown[entity.entity_type] += 1
        return dict(breakdown)
    
    def _get_high_connection_entities(self, top_n: int = 20) -> List[Dict]:
        """Get entities with most connections"""
        entity_connections = [
            {
                'name': entity.name,
                'type': entity.entity_type,
                'connection_count': len(entity.connections),
                'evidence_count': len(entity.evidence_ids)
            }
            for entity in self.entities.values()
        ]
        
        return sorted(entity_connections, 
                     key=lambda x: (x['connection_count'], x['evidence_count']), 
                     reverse=True)[:top_n]
    
    def _get_verification_breakdown(self) -> Dict[str, int]:
        """Get count of evidence by verification status"""
        breakdown = defaultdict(int)
        for evidence in self.evidence.values():
            breakdown[evidence.verification_status] += 1
        return dict(breakdown)
    
    def _get_recent_additions(self, days: int = 7) -> Dict:
        """Get recently added evidence"""
        recent_evidence = sorted(
            self.evidence.values(),
            key=lambda e: e.date_added,
            reverse=True
        )[:10]
        
        return {
            'recent_evidence': [e.to_dict() for e in recent_evidence]
        }
    
    def save_to_file(self, filename: str = "investigation_data.json"):
        """Save the entire database to a JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        
        data = {
            'entities': {name: entity.to_dict() for name, entity in self.entities.items()},
            'evidence': {eid: evidence.to_dict() for eid, evidence in self.evidence.items()},
            'last_updated': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Investigation data saved to {filepath}")
    
    def load_from_file(self, filename: str = "investigation_data.json"):
        """Load database from a JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"No existing data file found at {filepath}")
            return
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Load entities
        for name, entity_data in data.get('entities', {}).items():
            entity = Entity(
                entity_data['name'],
                entity_data['type'],
                entity_data.get('metadata', {})
            )
            entity.connections = entity_data.get('connections', [])
            entity.evidence_ids = entity_data.get('evidence_ids', [])
            entity.tags = set(entity_data.get('tags', []))
            self.entities[name] = entity
        
        # Load evidence
        for eid, evidence_data in data.get('evidence', {}).items():
            evidence = Evidence(
                evidence_data['id'],
                evidence_data['title'],
                evidence_data['source'],
                evidence_data['content']
            )
            evidence.date_added = evidence_data.get('date_added', '')
            evidence.related_entities = evidence_data.get('related_entities', [])
            evidence.tags = set(evidence_data.get('tags', []))
            evidence.verification_status = evidence_data.get('verification_status', 'unverified')
            evidence.metadata = evidence_data.get('metadata', {})
            self.evidence[eid] = evidence
        
        print(f"Loaded {len(self.entities)} entities and {len(self.evidence)} evidence items")


class InvestigationAssistant:
    """AI Assistant for conducting the investigation"""
    
    def __init__(self, database: InvestigationDatabase):
        self.db = database
    
    def analyze_entity(self, entity_name: str) -> str:
        """Analyze an entity and provide insights"""
        if entity_name not in self.db.entities:
            return f"Entity '{entity_name}' not found in database."
        
        network = self.db.get_entity_network(entity_name)
        entity = self.db.entities[entity_name]
        
        analysis = [
            f"\n=== Analysis of {entity_name} ===\n",
            f"Type: {entity.entity_type}",
            f"Total Connections: {network['connection_count']}",
            f"Evidence Items: {network['evidence_count']}",
            f"Tags: {', '.join(entity.tags) if entity.tags else 'None'}",
            "\n--- Direct Connections ---"
        ]
        
        for conn in entity.connections[:10]:  # Show first 10
            analysis.append(
                f"  • {conn['entity']} ({conn['relationship']}) "
                f"[Confidence: {conn['confidence']:.2f}]"
            )
        
        if network['evidence_count'] > 0:
            analysis.append("\n--- Related Evidence ---")
            for evidence in network['evidence'][:5]:  # Show first 5
                analysis.append(
                    f"  • [{evidence['verification_status']}] {evidence['title']} "
                    f"(Source: {evidence['source']})"
                )
        
        return "\n".join(analysis)
    
    def suggest_connections(self, entity_name: str) -> List[str]:
        """Suggest potential connections to investigate"""
        suggestions = []
        
        if entity_name not in self.db.entities:
            return suggestions
        
        entity = self.db.entities[entity_name]
        
        # Find entities that appear in the same evidence
        shared_evidence_entities = set()
        for eid in entity.evidence_ids:
            if eid in self.db.evidence:
                for related_entity in self.db.evidence[eid].related_entities:
                    if related_entity != entity_name:
                        shared_evidence_entities.add(related_entity)
        
        # Check which ones aren't already connected
        existing_connections = {conn['entity'] for conn in entity.connections}
        potential_connections = shared_evidence_entities - existing_connections
        
        for potential in potential_connections:
            suggestions.append(
                f"Potential connection: {entity_name} ↔ {potential} "
                f"(appears in shared evidence)"
            )
        
        return suggestions
    
    def find_investigation_gaps(self) -> List[str]:
        """Identify gaps in the investigation"""
        gaps = []
        
        # Find entities with no evidence
        entities_without_evidence = [
            entity.name for entity in self.db.entities.values()
            if len(entity.evidence_ids) == 0
        ]
        
        if entities_without_evidence:
            gaps.append(
                f"Entities without evidence ({len(entities_without_evidence)}): "
                f"{', '.join(entities_without_evidence[:5])}"
                + (" ..." if len(entities_without_evidence) > 5 else "")
            )
        
        # Find unverified evidence
        unverified = [
            e for e in self.db.evidence.values()
            if e.verification_status == 'unverified'
        ]
        
        if unverified:
            gaps.append(
                f"Unverified evidence items: {len(unverified)}"
            )
        
        # Find entities with few connections
        isolated_entities = [
            entity.name for entity in self.db.entities.values()
            if len(entity.connections) < 2
        ]
        
        if isolated_entities:
            gaps.append(
                f"Potentially isolated entities ({len(isolated_entities)}): "
                f"{', '.join(isolated_entities[:5])}"
                + (" ..." if len(isolated_entities) > 5 else "")
            )
        
        return gaps
    
    def generate_investigation_summary(self) -> str:
        """Generate a human-readable investigation summary"""
        report = self.db.generate_investigation_report()
        
        summary = [
            "\n" + "="*60,
            "EPSTEIN INVESTIGATION - STATUS REPORT",
            "="*60,
            f"\nReport Generated: {report['report_date']}",
            f"\nDatabase Statistics:",
            f"  • Total Entities: {report['total_entities']}",
            f"  • Total Evidence Items: {report['total_evidence']}",
            "\nEntity Breakdown:"
        ]
        
        for entity_type, count in report['entity_breakdown'].items():
            summary.append(f"  • {entity_type.capitalize()}: {count}")
        
        summary.append("\nTop Connected Entities:")
        for entity_info in report['high_connection_entities'][:10]:
            summary.append(
                f"  • {entity_info['name']} ({entity_info['type']}): "
                f"{entity_info['connection_count']} connections, "
                f"{entity_info['evidence_count']} evidence items"
            )
        
        summary.append("\nEvidence Verification Status:")
        for status, count in report['verification_status'].items():
            summary.append(f"  • {status.capitalize()}: {count}")
        
        # Investigation gaps
        gaps = self.find_investigation_gaps()
        if gaps:
            summary.append("\nInvestigation Gaps & Recommendations:")
            for gap in gaps:
                summary.append(f"  ⚠ {gap}")
        
        summary.append("\n" + "="*60)
        
        return "\n".join(summary)


def main():
    """Main function to demonstrate the investigation system"""
    print("Epstein Investigation AI System")
    print("================================\n")
    
    # Initialize the investigation database
    db = InvestigationDatabase()
    assistant = InvestigationAssistant(db)
    
    # Try to load existing data
    db.load_from_file()
    
    # If no data exists, create sample structure
    if len(db.entities) == 0:
        print("Initializing investigation database with core entities...\n")
        
        # Add core entities
        epstein = Entity("Jeffrey Epstein", "person", {
            "role": "Primary Subject",
            "status": "Deceased"
        })
        epstein.add_tag("primary_subject")
        epstein.add_tag("deceased")
        db.add_entity(epstein)
        
        print("Investigation system initialized.")
        print("Use the API to add entities, evidence, and connections.\n")
    
    # Display current status
    print(assistant.generate_investigation_summary())
    
    # Save the database
    db.save_to_file()


if __name__ == "__main__":
    main()
