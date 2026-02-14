# Contributing to the Epstein Investigation Repository

Thank you for your interest in contributing to this investigation. This project aims to organize publicly available information to support transparency and accountability.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Evidence Submission Guidelines](#evidence-submission-guidelines)
- [Data Verification](#data-verification)
- [Development](#development)

## Code of Conduct

### Our Standards

- **Accuracy**: Only submit verified, publicly available information
- **Transparency**: Cite all sources clearly
- **Respect**: Maintain professional conduct
- **Legality**: Only use information that is legally public
- **Objectivity**: Present facts without bias

### Prohibited Actions

- Submitting false or unverified information
- Including private or confidential data
- Making unfounded accusations
- Harassment or unprofessional behavior
- Violating any laws or regulations

## How to Contribute

### 1. Submit Evidence

If you have publicly available evidence:

```python
# Use the evidence template
from data_collector import DataCollector

collector = DataCollector()
template = collector.create_evidence_template()

# Fill in the template
evidence_data = {
    'title': 'Brief descriptive title',
    'source': 'Source name (e.g., court document, news article)',
    'source_type': 'document/testimony/media/etc',
    'date_of_occurrence': 'YYYY-MM-DD',
    'content': 'Detailed description of the evidence',
    'related_entities': ['Entity Name 1', 'Entity Name 2'],
    'tags': ['tag1', 'tag2'],
    'verification_notes': 'How this was verified',
    'metadata': {
        'url': 'source URL if applicable',
        'document_id': 'official document ID if applicable'
    }
}

# Submit via pull request
```

### 2. Report Connections

If you've identified connections between entities:

```python
from investigation_system import InvestigationDatabase

db = InvestigationDatabase()
db.load_from_file()

# Add connection
if "Entity A" in db.entities:
    db.entities["Entity A"].add_connection(
        "Entity B",
        "relationship_type",
        confidence=0.9  # 0.0-1.0 based on evidence strength
    )

db.save_to_file()
```

### 3. Add New Entities

To add a person, organization, or location:

```python
from investigation_system import Entity

# Create entity
entity = Entity(
    "Entity Name",
    "person",  # or organization, location, event
    {
        "role": "Description of role",
        "additional_info": "Any relevant metadata"
    }
)

# Add tags for categorization
entity.add_tag("relevant_tag")

# Submit via pull request
```

### 4. Improve Code

For code contributions:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a pull request

## Evidence Submission Guidelines

### Required Information

Every piece of evidence must include:

1. **Title**: Clear, descriptive title
2. **Source**: Where the information came from
3. **Content**: Detailed description
4. **Date**: When the event occurred (if applicable)
5. **Related Entities**: Who/what is involved
6. **Verification**: How it was verified

### Source Requirements

Sources must be:
- **Publicly accessible**: Available to anyone
- **Verifiable**: Can be independently confirmed
- **Cited properly**: Include URLs, document IDs, etc.
- **Legal**: Obtained through legal means

### Valid Source Types

- Court documents and filings
- News articles from reputable outlets
- Public records (flight logs, property records, etc.)
- Government documents
- Verified social media posts
- Academic publications
- Documentary evidence

### Invalid Sources

- Private communications
- Unverified rumors or hearsay
- Confidential documents
- Information obtained illegally
- Unattributed anonymous tips

## Data Verification

### Verification Levels

**Verified**: 
- Confirmed from official source
- Multiple independent sources
- Primary source documentation

**Unverified**:
- Single source only
- Needs confirmation
- Awaiting verification

**Disputed**:
- Contradicting evidence exists
- Source reliability questioned
- Under review

### Verification Process

1. **Check Source Credibility**
   - Is it from an official source?
   - Is the source reputable?
   - Can it be independently verified?

2. **Cross-Reference**
   - Look for corroborating sources
   - Check against known facts
   - Verify dates and details

3. **Document Verification**
   - Record verification steps
   - Note any discrepancies
   - Update verification status

## Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/pramit-shah/epstein-investigation-.git
cd epstein-investigation-

# Run tests (when available)
python3 -m pytest

# Initialize database
python3 investigation_system.py
```

### Code Style

- Use Python 3.7+ features
- Follow PEP 8 style guidelines
- Include docstrings for functions
- Comment complex logic
- Keep functions focused and modular

### Testing

Before submitting:
- Test all new functionality
- Ensure existing features still work
- Verify data integrity
- Check for edge cases

### Pull Request Process

1. **Update Documentation**: Document any changes
2. **Test Thoroughly**: Ensure everything works
3. **Clear Description**: Explain what and why
4. **Small Changes**: Keep PRs focused
5. **Respond to Feedback**: Address review comments

## Data Organization Standards

### Entity Naming
- Use full legal names when available
- Include aliases in metadata
- Be consistent with spelling/format

### Tagging System
Use relevant tags:
- `individual`: Individual person
- `organization`: Company, foundation, etc.
- `location`: Physical place
- `event`: Specific event or occurrence
- `legal`: Legal proceedings
- `financial`: Financial transactions
- `flight`: Flight logs related
- `property`: Real estate

### Relationship Types

Standard relationship types:
- Business: `business_partner`, `employer`, `employee`, `investor`
- Social: `friend`, `acquaintance`, `associate`
- Legal: `attorney`, `client`, `co-defendant`, `witness`
- Family: `spouse`, `child`, `parent`, `sibling`
- Institutional: `member`, `board_member`, `donor`
- Location: `resident`, `visitor`, `owner`

## Questions?

- Open an issue for questions
- Review existing documentation
- Check code examples
- Consult the README

## Legal Notice

By contributing, you affirm that:
- All submitted information is publicly available
- You have the right to submit this information
- The information is accurate to the best of your knowledge
- You comply with all applicable laws

## Thank You

Your contributions help bring transparency and accountability to this important investigation. Every verified piece of evidence and connection helps paint a clearer picture of the truth.
