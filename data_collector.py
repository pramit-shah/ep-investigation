#!/usr/bin/env python3
"""
Data Collection Module for Epstein Investigation
Assists in collecting and organizing public information
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class DataCollector:
    """Collects and organizes investigation data from various sources"""
    
    def __init__(self, output_dir: str = "data/collected"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.collection_log = []
    
    def collect_from_public_records(self, record_type: str, data: Dict) -> str:
        """
        Collect data from public records
        
        Args:
            record_type: Type of record (court_documents, flight_logs, etc.)
            data: Dictionary containing the record data
        
        Returns:
            Record ID
        """
        record_id = f"{record_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        record = {
            'id': record_id,
            'type': record_type,
            'data': data,
            'collected_date': datetime.now().isoformat(),
            'source': 'public_records',
            'verification_status': 'pending'
        }
        
        # Save to file
        filename = os.path.join(self.output_dir, f"{record_id}.json")
        with open(filename, 'w') as f:
            json.dump(record, f, indent=2)
        
        self.collection_log.append({
            'record_id': record_id,
            'type': record_type,
            'timestamp': datetime.now().isoformat()
        })
        
        return record_id
    
    def import_entity_list(self, entities: List[Dict]) -> int:
        """
        Import a list of entities (people, organizations, locations)
        
        Args:
            entities: List of entity dictionaries with name, type, metadata
        
        Returns:
            Number of entities imported
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.output_dir, f"entities_import_{timestamp}.json")
        
        import_data = {
            'import_date': datetime.now().isoformat(),
            'entity_count': len(entities),
            'entities': entities
        }
        
        with open(filename, 'w') as f:
            json.dump(import_data, f, indent=2)
        
        return len(entities)
    
    def import_connection_list(self, connections: List[Dict]) -> int:
        """
        Import a list of connections between entities
        
        Args:
            connections: List of connection dictionaries
        
        Returns:
            Number of connections imported
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.output_dir, f"connections_import_{timestamp}.json")
        
        import_data = {
            'import_date': datetime.now().isoformat(),
            'connection_count': len(connections),
            'connections': connections
        }
        
        with open(filename, 'w') as f:
            json.dump(import_data, f, indent=2)
        
        return len(connections)
    
    def create_evidence_template(self) -> Dict:
        """Create a template for evidence submission"""
        return {
            'title': '',
            'source': '',
            'source_type': '',  # document, testimony, media, etc.
            'date_of_occurrence': '',
            'date_obtained': datetime.now().isoformat(),
            'content': '',
            'related_entities': [],
            'tags': [],
            'verification_notes': '',
            'metadata': {}
        }
    
    def save_collection_log(self):
        """Save the collection log"""
        filename = os.path.join(self.output_dir, 'collection_log.json')
        with open(filename, 'w') as f:
            json.dump(self.collection_log, f, indent=2)


class TimelineBuilder:
    """Build chronological timeline of events"""
    
    def __init__(self, output_dir: str = "data/timeline"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.events = []
    
    def add_event(self, date: str, title: str, description: str, 
                  entities: List[str], evidence_ids: List[str] = None):
        """Add an event to the timeline"""
        event = {
            'date': date,
            'title': title,
            'description': description,
            'entities': entities,
            'evidence_ids': evidence_ids or [],
            'added_on': datetime.now().isoformat()
        }
        
        self.events.append(event)
        return event
    
    def get_timeline(self, start_date: Optional[str] = None, 
                     end_date: Optional[str] = None) -> List[Dict]:
        """Get timeline events within a date range"""
        filtered_events = self.events
        
        if start_date:
            filtered_events = [e for e in filtered_events if e['date'] >= start_date]
        
        if end_date:
            filtered_events = [e for e in filtered_events if e['date'] <= end_date]
        
        return sorted(filtered_events, key=lambda x: x['date'])
    
    def save_timeline(self, filename: str = "timeline.json"):
        """Save timeline to file"""
        filepath = os.path.join(self.output_dir, filename)
        
        timeline_data = {
            'generated_date': datetime.now().isoformat(),
            'event_count': len(self.events),
            'events': sorted(self.events, key=lambda x: x['date'])
        }
        
        with open(filepath, 'w') as f:
            json.dump(timeline_data, f, indent=2)
        
        print(f"Timeline saved to {filepath}")
    
    def load_timeline(self, filename: str = "timeline.json"):
        """Load timeline from file"""
        filepath = os.path.join(self.output_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.events = data.get('events', [])
            print(f"Loaded {len(self.events)} events from timeline")


def create_initial_data_structure():
    """Create initial directory structure for data organization"""
    directories = [
        'data',
        'data/entities',
        'data/evidence',
        'data/connections',
        'data/timeline',
        'data/collected',
        'data/reports',
        'data/analysis'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Data directory structure created")


if __name__ == "__main__":
    print("Data Collection Module for Epstein Investigation")
    print("=" * 50)
    create_initial_data_structure()
    
    # Create example templates
    collector = DataCollector()
    template = collector.create_evidence_template()
    
    print("\nEvidence Template Created:")
    print(json.dumps(template, indent=2))
