# Investigation System Architecture

## System Components

### 1. Core Investigation System (`investigation_system.py`)

The heart of the investigation repository, providing:

#### Entity Class
Represents any person, organization, location, or event in the investigation.

**Attributes:**
- `name`: Entity identifier
- `entity_type`: person, organization, location, event
- `metadata`: Additional information dictionary
- `connections`: List of relationships to other entities
- `evidence_ids`: Links to supporting evidence
- `tags`: Categorization tags

**Methods:**
- `add_connection(entity, relationship, confidence)`: Link to another entity
- `add_evidence(evidence_id)`: Associate evidence
- `add_tag(tag)`: Add categorization tag

#### Evidence Class
Represents any piece of evidence in the investigation.

**Attributes:**
- `evidence_id`: Unique identifier
- `title`: Brief description
- `source`: Where the evidence came from
- `content`: Detailed information
- `related_entities`: Connected entities
- `tags`: Categorization
- `verification_status`: verified, unverified, disputed

**Methods:**
- `add_related_entity(name)`: Link entity
- `set_verification_status(status)`: Update verification
- `add_tag(tag)`: Categorize evidence

#### InvestigationDatabase Class
Central database managing all entities and evidence.

**Key Features:**
- Entity and evidence storage
- Search functionality
- Connection discovery
- Report generation
- JSON persistence

**Methods:**
- `add_entity(entity)`: Add/update entity
- `add_evidence(evidence)`: Add evidence
- `find_connections(entity, depth)`: Traverse network
- `search_entities(query, type)`: Search entities
- `search_evidence(query)`: Search evidence
- `get_entity_network(entity)`: Complete network view
- `generate_investigation_report()`: Status report
- `save_to_file()` / `load_from_file()`: Persistence

#### InvestigationAssistant Class
AI-powered analysis and insights.

**Capabilities:**
- Entity analysis with connections and evidence
- Connection suggestions based on shared evidence
- Investigation gap identification
- Human-readable summaries

### 2. Network Analysis (`network_analysis.py`)

Advanced graph analysis for relationship mapping.

#### NetworkAnalyzer Class

**Graph Algorithms:**
- `find_shortest_path(start, end)`: BFS pathfinding
- `find_all_paths(start, end, depth)`: DFS all paths
- `calculate_centrality()`: Degree centrality metrics
- `find_clusters(min_size)`: Community detection
- `identify_key_connectors()`: Central nodes
- `analyze_connection_strength()`: Relationship strength

**Analysis Features:**
- Path discovery between any entities
- Centrality scoring
- Cluster identification
- Shared evidence analysis
- Connection strength metrics

#### RelationshipMapper Class

Categorizes and analyzes relationship types:
- Business relationships
- Social connections
- Legal associations
- Family ties
- Institutional memberships
- Location relationships

### 3. Data Collection (`data_collector.py`)

Manages data import and organization.

#### DataCollector Class

**Functions:**
- Public records collection
- Entity batch import
- Connection batch import
- Evidence template generation
- Collection logging

#### TimelineBuilder Class

**Features:**
- Event chronology
- Date-based filtering
- Entity-event associations
- Evidence linking
- Timeline visualization data

### 4. Command-Line Interface (`cli.py`)

Interactive investigation interface.

**Menu Options:**
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

**Features:**
- User-friendly prompts
- Interactive search
- Entity suggestions
- Network visualization
- Report export

## Data Flow

### Adding an Entity
```
User Input → Entity Object → Database → JSON File
                ↓
         Connections & Tags
```

### Adding Evidence
```
Evidence Input → Evidence Object → Database
                      ↓
              Link to Entities ← Automatic backlink
                      ↓
                  JSON File
```

### Network Analysis
```
Database → NetworkAnalyzer → Graph Algorithms
              ↓
    Paths, Clusters, Centrality
              ↓
         Reports & Insights
```

### Search Process
```
Query → Search Engine → Filter by type/tags
          ↓
    Match in entities/evidence
          ↓
      Ranked Results
```

## Database Schema

### investigation_data.json Structure
```json
{
  "entities": {
    "Entity Name": {
      "name": "string",
      "type": "person|organization|location|event",
      "metadata": {},
      "connections": [
        {
          "entity": "string",
          "relationship": "string",
          "confidence": 0.0-1.0,
          "timestamp": "ISO-8601"
        }
      ],
      "evidence_ids": ["EV001", "EV002"],
      "tags": ["tag1", "tag2"]
    }
  },
  "evidence": {
    "EV001": {
      "id": "string",
      "title": "string",
      "source": "string",
      "content": "string",
      "date_added": "ISO-8601",
      "related_entities": ["Entity Name"],
      "tags": ["tag1"],
      "verification_status": "verified|unverified|disputed",
      "metadata": {}
    }
  },
  "last_updated": "ISO-8601"
}
```

### Timeline Structure
```json
{
  "generated_date": "ISO-8601",
  "event_count": 0,
  "events": [
    {
      "date": "YYYY-MM-DD",
      "title": "string",
      "description": "string",
      "entities": ["Entity Name"],
      "evidence_ids": ["EV001"],
      "added_on": "ISO-8601"
    }
  ]
}
```

## Algorithms

### Path Finding (BFS)
```python
# Find shortest path between entities
queue = [(start, [start])]
visited = {start}
while queue:
    current, path = queue.pop(0)
    for neighbor in adjacency[current]:
        if neighbor == target:
            return path + [neighbor]
        if neighbor not in visited:
            queue.append((neighbor, path + [neighbor]))
```

### Centrality Calculation
```python
# Degree centrality
for entity in entities:
    outgoing = len(connections[entity])
    incoming = count_incoming(entity)
    centrality[entity] = (outgoing + incoming) / max_connections
```

### Cluster Detection
```python
# Connected component analysis
for entity in entities:
    if not visited[entity]:
        cluster = explore_connected(entity, min_confidence=0.7)
        if len(cluster) >= min_size:
            clusters.append(cluster)
```

## Performance Considerations

### Database Size
- **Small** (< 100 entities): All operations fast
- **Medium** (100-1000 entities): Network analysis may take seconds
- **Large** (> 1000 entities): Consider indexed search

### Optimization Strategies
1. **Lazy Loading**: Load only needed data
2. **Caching**: Cache frequent queries
3. **Indexing**: Build search indices
4. **Pagination**: Limit result sets

## Extension Points

### Adding New Entity Types
```python
# In investigation_system.py, Entity class
valid_types = ['person', 'organization', 'location', 'event', 'document']
```

### Custom Relationship Types
```python
# In network_analysis.py, RelationshipMapper class
relationship_types = {
    'custom_category': ['type1', 'type2']
}
```

### Additional Analysis
```python
# Create new analyzer
class CustomAnalyzer:
    def __init__(self, db):
        self.db = db
    
    def custom_analysis(self):
        # Your analysis logic
        pass
```

## Security & Privacy

### Data Handling
- All data stored locally
- No external network calls
- JSON file encryption optional
- Access control via file system

### Verification Levels
1. **Verified**: Multiple reliable sources
2. **Unverified**: Single source, needs confirmation
3. **Disputed**: Conflicting evidence

### Source Requirements
- Must be publicly available
- Must be legally obtained
- Must be properly cited
- Must be verifiable

## Best Practices

### Entity Management
1. Use consistent naming (full legal names)
2. Include aliases in metadata
3. Tag comprehensively
4. Link all relevant evidence

### Evidence Organization
1. Cite sources completely
2. Include dates when available
3. Cross-reference related items
4. Mark verification status

### Connection Tracking
1. Set appropriate confidence levels
2. Document relationship types clearly
3. Update as new information emerges
4. Remove invalidated connections

### Regular Maintenance
1. Verify old evidence periodically
2. Update entity metadata
3. Export backups regularly
4. Review investigation gaps

## Troubleshooting

### Common Issues

**Issue**: Entity not found
- **Cause**: Exact name match required
- **Solution**: Use search function

**Issue**: Slow network analysis
- **Cause**: Too many connections
- **Solution**: Limit max_depth parameter

**Issue**: Data not saving
- **Cause**: File permissions or path
- **Solution**: Check write permissions

## Future Enhancements

Potential additions:
- Web-based interface
- Visualization graphs
- Advanced search with filters
- Automated data import from sources
- Collaborative features
- Export to various formats
- API for external tools

## Contributing to Development

See CONTRIBUTING.md for:
- Code style guidelines
- Testing procedures
- Pull request process
- Feature requests
