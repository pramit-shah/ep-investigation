# Epstein Investigation System - Quick Start Guide

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/pramit-shah/epstein-investigation-.git
cd epstein-investigation-
```

### 2. Run Setup
```bash
python3 setup.py
```

This will:
- Create necessary directories
- Initialize the database
- Set up the investigation system

## Using the System

### Interactive Mode
The easiest way to use the system:
```bash
python3 cli.py
```

You'll see a menu with options:
1. View Investigation Summary
2. Search Entities
3. Search Evidence
4. Analyze Entity
5. Add Entity
6. Add Evidence
7. Add Connection
8. Network Analysis
9. Export Report
10. Save & Exit

### Quick Summary
View the current state of the investigation:
```bash
python3 cli.py --summary
```

## Common Tasks

### Adding an Entity

**Via CLI:**
1. Run `python3 cli.py`
2. Select option 5 (Add Entity)
3. Enter the entity details when prompted

**Via Python:**
```python
from investigation_system import InvestigationDatabase, Entity

db = InvestigationDatabase()
db.load_from_file()

person = Entity("Jane Doe", "person", {"role": "Example"})
person.add_tag("witness")
db.add_entity(person)
db.save_to_file()
```

### Adding Evidence

**Via CLI:**
1. Run `python3 cli.py`
2. Select option 6 (Add Evidence)
3. Fill in the evidence details

**Via Python:**
```python
from investigation_system import Evidence

evidence = Evidence(
    "EV001",
    "Court Document X",
    "U.S. District Court",
    "Document describes..."
)
evidence.add_related_entity("Jeffrey Epstein")
evidence.add_tag("legal")
evidence.set_verification_status("verified")

db.add_evidence(evidence)
db.save_to_file()
```

### Adding Connections

**Via CLI:**
1. Run `python3 cli.py`
2. Select option 7 (Add Connection)
3. Enter the entity names and relationship

**Via Python:**
```python
db.load_from_file()
entity = db.entities["Jeffrey Epstein"]
entity.add_connection("Jane Doe", "associate", confidence=0.8)
db.save_to_file()
```

### Searching

**Search Entities:**
```bash
python3 cli.py
# Then select option 2 and enter search term
```

**Search Evidence:**
```bash
python3 cli.py
# Then select option 3 and enter search term
```

### Network Analysis

**Find Connections Between Entities:**
```bash
python3 cli.py
# Select option 8 (Network Analysis)
# Choose option 1 (Find path)
# Enter start and end entities
```

**View Network Report:**
```bash
python3 cli.py
# Select option 8
# Choose option 2
```

## Working with Templates

Templates are provided in the `templates/` directory:

- `example_evidence.json` - Template for evidence
- `example_entities.json` - Template for entities
- `example_connections.json` - Template for connections

Copy and modify these templates with your data.

## Data Organization

All data is stored in the `data/` directory:
- `data/investigation_data.json` - Main database file
- `data/reports/` - Generated reports
- `data/timeline/` - Timeline events

## Python API Examples

### Complete Example
```python
from investigation_system import InvestigationDatabase, Entity, Evidence
from network_analysis import NetworkAnalyzer

# Initialize
db = InvestigationDatabase()
db.load_from_file()

# Add entity
person = Entity("John Smith", "person")
person.add_tag("witness")
db.add_entity(person)

# Add evidence
evidence = Evidence("EV002", "Testimony", "Court", "Details...")
evidence.add_related_entity("John Smith")
db.add_evidence(evidence)

# Add connection
db.entities["Jeffrey Epstein"].add_connection(
    "John Smith", 
    "acquaintance",
    confidence=0.7
)

# Save
db.save_to_file()

# Analyze
analyzer = NetworkAnalyzer(db.entities, db.evidence)
path = analyzer.find_shortest_path("Jeffrey Epstein", "John Smith")
print(f"Path: {' → '.join(path)}")
```

## Tips

1. **Save Often**: Use option 10 in the CLI to save your work
2. **Verify Sources**: Always include source information for evidence
3. **Use Tags**: Tag entities and evidence for better organization
4. **Check Connections**: Use network analysis to verify relationships
5. **Export Reports**: Regularly export reports for record-keeping

## Troubleshooting

**Problem**: "No module named 'investigation_system'"
**Solution**: Make sure you're in the repository directory

**Problem**: Data not saving
**Solution**: Use option 10 in CLI or call `db.save_to_file()` in Python

**Problem**: Entity not found
**Solution**: Use search function to find correct entity name

## Getting Help

- Read the full README.md for detailed documentation
- Check CONTRIBUTING.md for contribution guidelines
- Review the code comments for API details
- Open an issue on GitHub for bugs or questions

## Next Steps

1. Familiarize yourself with the CLI
2. Add your first entity or evidence
3. Explore the network analysis features
4. Export a report to see the data structure
5. Review the Python API for programmatic access

For more information, see README.md and the inline documentation in the Python files.
