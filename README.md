# Epstein Investigation Repository

## Overview

This repository contains an AI-powered investigation system designed to assist in the Epstein investigation by:

- **Tracking connections** between individuals, organizations, and locations
- **Organizing evidence** from public records and sources
- **Analyzing relationships** and identifying key connectors
- **Building timelines** of events
- **Connecting dots** through network analysis
- **Providing transparency** to support FBI investigations and public awareness
- **Autonomous data collection** from multiple sources without user input
- **Transaction and tie tracking** with continuous monitoring

## Mission

To assist Director Patel and the FBI in expediting the Epstein investigation by providing:
1. A comprehensive database of entities and connections
2. AI-powered analysis to identify patterns and relationships
3. Public access to information to uncover hidden coverups
4. Tools to bring all truth to light
5. **Autonomous research system with one logic drift: Uncover all truths with continuous ties and transactions tracking**

## Features

### 1. Investigation Database (`investigation_system.py`)
- **Entity Management**: Track people, organizations, locations, and events
- **Evidence Repository**: Store and organize evidence with verification status
- **Connection Tracking**: Map relationships between entities
- **Search Functionality**: Find entities and evidence quickly
- **Network Analysis**: Discover paths and connections between entities

### 2. Data Collection (`data_collector.py`)
- **Public Records Integration**: Import data from public sources
- **Evidence Templates**: Standardized evidence submission
- **Timeline Building**: Chronological organization of events
- **Batch Import**: Import multiple entities and connections at once

### 3. Network Analysis (`network_analysis.py`)
- **Path Finding**: Discover connections between any two entities
- **Centrality Analysis**: Identify most connected entities
- **Cluster Detection**: Find groups of highly connected entities
- **Connection Strength**: Measure relationship strength
- **Key Connector Identification**: Find entities that bridge different groups

### 4. Command-Line Interface (`cli.py`)
- **Interactive Investigation**: Easy-to-use menu system
- **Quick Search**: Find entities and evidence instantly
- **Entity Analysis**: Deep dive into connections and evidence
- **Report Generation**: Export investigation summaries

### 5. Autonomous Research System (`autonomous_researcher.py`)
- **Autonomous Data Collection**: Collects data without user input
- **Multi-Source Support**: Documents, videos, testimonies, DOJ files, flight logs, financial records
- **ZIP Archive Management**: Stores collected data in verified .zip files with integrity checking
- **Data Mapping**: Comprehensive map linking all resources, entities, and connections
- **Transaction Tracking**: Monitors financial transactions between entities
- **Tie Tracking**: Continuously tracks connections and relationships
- **Priority-Based Research**: Automatically prioritizes critical data sources

### 6. Integrated Investigation (`integrated_investigation.py`)
- **System Integration**: Bridges autonomous research with manual investigation
- **Data Synchronization**: Auto-syncs collected data to investigation database
- **Unified Interface**: Single point of access for all investigation data
- **Continuous Monitoring**: Tracks ties and transactions across both systems

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup

1. Clone this repository:
```bash
git clone https://github.com/pramit-shah/epstein-investigation-.git
cd epstein-investigation-
```

2. No external dependencies required - uses Python standard library only

3. Initialize the data structure:
```bash
python3 investigation_system.py
```

## Usage

### Quick Start

1. **Run the interactive CLI**:
```bash
python3 cli.py
```

2. **View investigation summary**:
```bash
python3 cli.py --summary
```

3. **Run autonomous research** (collects data automatically):
```bash
python3 autonomous_researcher.py
```

4. **Run integrated investigation** (autonomous + manual):
```bash
python3 integrated_investigation.py
```

5. **Run individual modules**:
```bash
# Initialize database
python3 investigation_system.py

# Set up data collection
python3 data_collector.py

# Analyze network
python3 network_analysis.py
```

### Adding Data

#### Add an Entity
```python
from investigation_system import InvestigationDatabase, Entity

db = InvestigationDatabase()
db.load_from_file()

# Create a new entity
person = Entity("Name", "person", {"role": "Description"})
person.add_tag("tag1")
person.add_tag("tag2")

db.add_entity(person)
db.save_to_file()
```

#### Add Evidence
```python
from investigation_system import Evidence

evidence = Evidence(
    "EV001",
    "Evidence Title",
    "Source Name",
    "Evidence description and content"
)
evidence.add_related_entity("Entity Name")
evidence.add_tag("relevant_tag")
evidence.set_verification_status("verified")

db.add_evidence(evidence)
db.save_to_file()
```

#### Add Connections
```python
# Add a connection between entities
entity = db.entities["Person A"]
entity.add_connection(
    "Person B",
    "business_partner",
    confidence=0.9
)

db.save_to_file()
```

### Analyzing the Network

```python
from investigation_system import InvestigationDatabase, InvestigationAssistant
from network_analysis import NetworkAnalyzer

# Load database
db = InvestigationDatabase()
db.load_from_file()

# Create analyzer
analyzer = NetworkAnalyzer(db.entities, db.evidence)

# Find path between entities
path = analyzer.find_shortest_path("Person A", "Person B")
print(f"Path: {' → '.join(path)}")

# Get network report
print(analyzer.generate_network_report())

# Identify key connectors
connectors = analyzer.identify_key_connectors(10)
for conn in connectors:
    print(f"{conn['name']}: {conn['centrality_score']:.3f}")
```

## Data Organization

```
data/
├── investigation_data.json    # Main database
├── entities/                  # Entity-specific data
├── evidence/                  # Evidence files
├── connections/              # Connection data
├── timeline/                 # Timeline events
│   └── timeline.json
├── collected/                # Collected data
├── reports/                  # Generated reports
└── analysis/                 # Analysis outputs
```

## Contributing

This investigation relies on public information and transparent collaboration.

### How to Contribute

1. **Submit Evidence**: Use the evidence template to submit public information
2. **Report Connections**: Identify relationships between entities
3. **Verify Data**: Help verify existing evidence
4. **Improve Code**: Submit pull requests for improvements

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Evidence Submission Guidelines

- Only include information from public sources
- Cite sources clearly
- Mark verification status appropriately
- Tag evidence for easy categorization
- Include relevant dates when available

### Data Verification

All evidence should be:
- From public, verifiable sources
- Properly cited
- Cross-referenced when possible
- Marked with verification status

## Investigation Principles

1. **Transparency**: All data is open and accessible
2. **Accuracy**: Verify information from multiple sources
3. **Comprehensive**: Track all connections and evidence
4. **Objective**: Let the data speak for itself
5. **Legal**: Only use publicly available information

## API Reference

### InvestigationDatabase

Main database for storing entities and evidence.

**Methods**:
- `add_entity(entity)`: Add an entity to the database
- `add_evidence(evidence)`: Add evidence to the database
- `find_connections(entity_name, max_depth)`: Find all connections
- `search_entities(query, entity_type)`: Search for entities
- `search_evidence(query)`: Search evidence
- `get_entity_network(entity_name)`: Get complete network info
- `generate_investigation_report()`: Generate status report
- `save_to_file(filename)`: Save database to JSON
- `load_from_file(filename)`: Load database from JSON

### NetworkAnalyzer

Analyzes network connections and relationships.

**Methods**:
- `find_shortest_path(start, end)`: Find shortest path between entities
- `find_all_paths(start, end, max_depth)`: Find all paths
- `calculate_centrality()`: Calculate entity centrality scores
- `find_clusters(min_cluster_size)`: Identify entity clusters
- `identify_key_connectors(top_n)`: Find most connected entities
- `analyze_connection_strength(entity1, entity2)`: Analyze connection
- `generate_network_report()`: Generate network analysis report

### InvestigationAssistant

AI assistant for investigation analysis.

**Methods**:
- `analyze_entity(entity_name)`: Detailed entity analysis
- `suggest_connections(entity_name)`: Suggest potential connections
- `find_investigation_gaps()`: Identify gaps in investigation
- `generate_investigation_summary()`: Generate summary report

## Security and Privacy

- This system only processes publicly available information
- No personal data should be included unless already public
- All sources must be verifiable
- Comply with all applicable laws and regulations

## Disclaimer

This is an investigative tool for organizing publicly available information. It does not:
- Make accusations or determinations of guilt
- Include non-public or confidential information
- Replace official law enforcement investigations
- Provide legal advice

All information should be verified through official sources.

## Support

For questions or issues:
- Open an issue on GitHub
- Review existing documentation
- Check the examples in the code

## License

MIT License - See LICENSE file for details

## Acknowledgments

This tool is designed to assist in bringing truth to light and supporting legitimate investigative efforts by organizing publicly available information in a transparent and accessible manner.

---

**Status**: Active Development  
**Version**: 1.0.0  
**Last Updated**: 2026-02-14

## Quick Reference Commands

```bash
# View summary
python3 cli.py --summary

# Interactive mode
python3 cli.py

# Initialize fresh database
python3 investigation_system.py

# Run network analysis
python3 network_analysis.py

# Run autonomous research (NEW)
python3 autonomous_researcher.py

# Run integrated investigation (NEW)
python3 integrated_investigation.py
```

## Autonomous Research System

The autonomous research system operates independently to:
- Collect data from DOJ files, flight logs, testimonies, financial records, and media
- Store all data in verified .zip archives
- Create comprehensive data maps linking resources
- Track financial transactions continuously
- Monitor ties and connections between entities
- Sync with manual investigation database

**One Logic Drift: Uncover all truths with continuous ties and transactions tracking**

See [AUTONOMOUS_RESEARCH.md](AUTONOMOUS_RESEARCH.md) for complete documentation.