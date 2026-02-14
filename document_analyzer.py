#!/usr/bin/env python3
"""
Advanced Document Analysis Module
Detects redactions, uncovers hidden information, tracks aliases and name changes
"""

import re
import hashlib
from datetime import datetime
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict


class RedactionDetector:
    """Detects and analyzes redacted or edited content in documents"""
    
    # Common redaction patterns
    REDACTION_PATTERNS = [
        r'\[REDACTED\]',
        r'\[.*?REDACTED.*?\]',
        r'█+',  # Black boxes
        r'▓+',  # Shaded boxes
        r'■+',  # Solid squares
        r'\*\*\*+',  # Asterisks
        r'XXX+',
        r'\[DELETED\]',
        r'\[WITHHELD\]',
        r'\[CLASSIFIED\]',
        r'_{3,}',  # Underscores
        r'\.{3,}',  # Dots
    ]
    
    def __init__(self):
        self.detected_redactions = []
        self.context_clues = []
    
    def detect_redactions(self, text: str) -> List[Dict]:
        """
        Detect redacted content in text
        Returns list of redaction locations with context
        """
        redactions = []
        
        for pattern in self.REDACTION_PATTERNS:
            for match in re.finditer(pattern, text):
                # Get context around redaction
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                redaction = {
                    'pattern': pattern,
                    'location': match.span(),
                    'redacted_text': match.group(),
                    'before_context': text[start:match.start()],
                    'after_context': text[match.end():end],
                    'full_context': context,
                    'length': len(match.group())
                }
                
                redactions.append(redaction)
                self.detected_redactions.append(redaction)
        
        return redactions
    
    def analyze_redaction_context(self, redaction: Dict) -> Dict:
        """
        Analyze context around redaction to infer what might be hidden
        """
        before = redaction['before_context'].strip()
        after = redaction['after_context'].strip()
        
        analysis = {
            'likely_type': 'unknown',
            'confidence': 0.0,
            'clues': []
        }
        
        # Name detection
        name_indicators = ['Mr.', 'Mrs.', 'Ms.', 'Dr.', 'named', 'called', 'known as']
        if any(indicator in before for indicator in name_indicators):
            analysis['likely_type'] = 'name'
            analysis['confidence'] = 0.7
            analysis['clues'].append('Name indicator found before redaction')
        
        # Location detection
        location_indicators = ['at', 'in', 'from', 'located', 'address', 'city', 'state']
        if any(indicator in before for indicator in location_indicators):
            analysis['likely_type'] = 'location'
            analysis['confidence'] = 0.6
            analysis['clues'].append('Location indicator found')
        
        # Date detection
        if re.search(r'on\s+$', before) or re.search(r'^,?\s*\d{4}', after):
            analysis['likely_type'] = 'date'
            analysis['confidence'] = 0.8
            analysis['clues'].append('Date pattern detected')
        
        # Amount detection
        if '$' in before or re.search(r'\d{1,3}(,\d{3})*$', before):
            analysis['likely_type'] = 'amount'
            analysis['confidence'] = 0.7
            analysis['clues'].append('Currency/amount pattern detected')
        
        # Organization detection
        org_indicators = ['company', 'corporation', 'foundation', 'organization', 'LLC', 'Inc']
        if any(indicator in before for indicator in org_indicators):
            analysis['likely_type'] = 'organization'
            analysis['confidence'] = 0.65
            analysis['clues'].append('Organization indicator found')
        
        return analysis
    
    def find_length_clues(self, redacted_text: str) -> Dict:
        """
        Use length of redaction to narrow down possibilities
        """
        length = len(redacted_text)
        
        clues = {
            'length': length,
            'possibilities': []
        }
        
        # Character-based redactions give us exact length
        if '█' in redacted_text or '▓' in redacted_text or '■' in redacted_text:
            clues['exact_length'] = True
            
            if 2 <= length <= 4:
                clues['possibilities'].append('Short name or code')
            elif 5 <= length <= 15:
                clues['possibilities'].append('Full name or identifier')
            elif 16 <= length <= 30:
                clues['possibilities'].append('Full name with middle name or organization')
            else:
                clues['possibilities'].append('Long text or multiple items')
        else:
            clues['exact_length'] = False
            clues['possibilities'].append('Length unknown - placeholder used')
        
        return clues


class AliasTracker:
    """Tracks aliases, cryptic names, and name variations"""
    
    def __init__(self):
        self.aliases: Dict[str, Set[str]] = defaultdict(set)  # canonical_name -> aliases
        self.reverse_map: Dict[str, str] = {}  # alias -> canonical_name
        self.cryptic_identifiers: Dict[str, List[str]] = defaultdict(list)
        self.name_patterns = []
    
    def add_alias(self, canonical_name: str, alias: str):
        """Add an alias for a canonical name"""
        self.aliases[canonical_name].add(alias)
        self.reverse_map[alias] = canonical_name
        self.reverse_map[canonical_name] = canonical_name
    
    def add_cryptic_identifier(self, identifier: str, context: str):
        """
        Add a cryptic identifier (code name, nickname, etc.)
        """
        self.cryptic_identifiers[identifier].append({
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
    
    def detect_cryptic_patterns(self, text: str) -> List[Dict]:
        """
        Detect potential cryptic identifiers in text
        """
        patterns = []
        
        # Pattern: Single letters or numbers in quotes
        for match in re.finditer(r'["\']([\w])["\']', text):
            patterns.append({
                'type': 'single_char_identifier',
                'identifier': match.group(1),
                'context': self._get_context(text, match.span())
            })
        
        # Pattern: Code names (Subject-1, Individual-A, etc.)
        for match in re.finditer(r'\b(Subject|Individual|Person|Entity)[-\s]([A-Z0-9]+)\b', text, re.IGNORECASE):
            patterns.append({
                'type': 'code_identifier',
                'identifier': match.group(0),
                'context': self._get_context(text, match.span())
            })
        
        # Pattern: Initials (J.E., G.M., etc.)
        for match in re.finditer(r'\b([A-Z]\.[A-Z]\.(?:[A-Z]\.)?)\b', text):
            patterns.append({
                'type': 'initials',
                'identifier': match.group(1),
                'context': self._get_context(text, match.span())
            })
        
        # Pattern: Nicknames in quotes
        for match in re.finditer(r'["\']([\w\s]{2,15})["\']', text):
            potential_nickname = match.group(1)
            if not potential_nickname.isupper():  # Not all caps (likely not yelling)
                patterns.append({
                    'type': 'potential_nickname',
                    'identifier': potential_nickname,
                    'context': self._get_context(text, match.span())
                })
        
        return patterns
    
    def _get_context(self, text: str, span: Tuple[int, int], window: int = 40) -> str:
        """Get context around a match"""
        start = max(0, span[0] - window)
        end = min(len(text), span[1] + window)
        return text[start:end]
    
    def resolve_alias(self, name: str) -> str:
        """Resolve an alias to canonical name"""
        return self.reverse_map.get(name, name)
    
    def get_all_aliases(self, canonical_name: str) -> Set[str]:
        """Get all known aliases for a canonical name"""
        return self.aliases.get(canonical_name, set())


class NameVariationDetector:
    """Detects name changes, variations, and maiden names"""
    
    def __init__(self):
        self.name_changes: List[Dict] = []
        self.variations: Dict[str, List[str]] = defaultdict(list)
    
    def detect_name_variations(self, name: str) -> List[str]:
        """
        Generate possible variations of a name
        """
        variations = [name]
        
        # Split name into parts
        parts = name.split()
        
        if len(parts) >= 2:
            # First + Last
            variations.append(f"{parts[0]} {parts[-1]}")
            
            # Initials variations
            initials = ''.join([p[0] for p in parts if p])
            variations.append(initials)
            variations.append('.'.join([p[0] for p in parts if p]) + '.')
            
            # First name only
            variations.append(parts[0])
            
            # Last name only
            variations.append(parts[-1])
            
            # First initial + Last name
            if parts[0]:
                variations.append(f"{parts[0][0]}. {parts[-1]}")
        
        return list(set(variations))
    
    def detect_maiden_name_pattern(self, text: str) -> List[Dict]:
        """
        Detect maiden name patterns in text
        """
        patterns = []
        
        # Pattern: "née" or "nee" with parentheses
        for match in re.finditer(r'([\w\s]+)\s*\((?:née|nee|born)\s+([\w\s]+)\)', text, re.IGNORECASE):
            patterns.append({
                'married_name': match.group(1).strip(),
                'maiden_name': match.group(2).strip(),
                'pattern': 'nee',
                'context': self._get_context(text, match.span())
            })
        
        # Pattern: "née" or "nee" without parentheses
        for match in re.finditer(r'([\w\s]+)\s+(?:née|nee|born)\s+([\w\s]+)', text, re.IGNORECASE):
            patterns.append({
                'married_name': match.group(1).strip(),
                'maiden_name': match.group(2).strip(),
                'pattern': 'nee',
                'context': self._get_context(text, match.span())
            })
        
        # Pattern: "formerly known as"
        for match in re.finditer(r'([\w\s]+)\s+(?:formerly known as|previously)\s+([\w\s]+)', text, re.IGNORECASE):
            patterns.append({
                'current_name': match.group(1).strip(),
                'former_name': match.group(2).strip(),
                'pattern': 'formerly',
                'context': self._get_context(text, match.span())
            })
        
        return patterns
    
    def _get_context(self, text: str, span: Tuple[int, int], window: int = 50) -> str:
        """Get context around a match"""
        start = max(0, span[0] - window)
        end = min(len(text), span[1] + window)
        return text[start:end]
    
    def add_name_change(self, old_name: str, new_name: str, date: Optional[str] = None, 
                       reason: Optional[str] = None, source: Optional[str] = None):
        """Record a name change"""
        change = {
            'old_name': old_name,
            'new_name': new_name,
            'date': date,
            'reason': reason,
            'source': source,
            'recorded': datetime.now().isoformat()
        }
        self.name_changes.append(change)
        self.variations[new_name].append(old_name)
        self.variations[old_name].append(new_name)


class HiddenConnectionFinder:
    """Finds hidden connections like children, relatives, associates"""
    
    def __init__(self):
        self.potential_children = []
        self.potential_relatives = []
        self.temporal_connections = []
    
    def find_birth_patterns(self, text: str, entity_name: str) -> List[Dict]:
        """
        Find patterns suggesting children or births around certain times
        """
        patterns = []
        
        # Pattern: "child", "son", "daughter" near entity name
        child_terms = ['child', 'children', 'son', 'daughter', 'offspring', 'baby', 'infant']
        
        for term in child_terms:
            # Look for term near entity name
            pattern = rf'({entity_name}.{{0,100}}{term}|{term}.{{0,100}}{entity_name})'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                context = self._get_context(text, match.span(), 100)
                
                # Try to extract dates
                dates = re.findall(r'\b\d{4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b', context)
                
                # Try to extract names
                names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', context)
                
                patterns.append({
                    'type': 'potential_child',
                    'term': term,
                    'entity': entity_name,
                    'context': context,
                    'dates': dates,
                    'potential_names': names,
                    'confidence': 0.5
                })
        
        return patterns
    
    def find_family_relationships(self, text: str, entity_name: str) -> List[Dict]:
        """
        Find family relationship mentions
        """
        relationships = []
        
        family_terms = {
            'parent': ['mother', 'father', 'parent'],
            'sibling': ['brother', 'sister', 'sibling'],
            'spouse': ['wife', 'husband', 'spouse', 'married', 'partner'],
            'child': ['son', 'daughter', 'child'],
            'extended': ['uncle', 'aunt', 'cousin', 'nephew', 'niece', 'grandchild', 'grandmother', 'grandfather']
        }
        
        for rel_type, terms in family_terms.items():
            for term in terms:
                pattern = rf'({entity_name}.{{0,80}}{term}|{term}.{{0,80}}{entity_name})'
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    context = self._get_context(text, match.span(), 100)
                    
                    # Try to extract names
                    names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', context)
                    
                    relationships.append({
                        'relationship_type': rel_type,
                        'term': term,
                        'entity': entity_name,
                        'context': context,
                        'potential_names': [n for n in names if n != entity_name],
                        'confidence': 0.6
                    })
        
        return relationships
    
    def find_temporal_connections(self, text: str, timeframe_start: str, 
                                  timeframe_end: str) -> List[Dict]:
        """
        Find events or people mentioned in a specific timeframe
        """
        connections = []
        
        # Extract all dates from text
        date_patterns = [
            r'\b\d{4}\b',  # Year
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',  # Month Day, Year
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b'  # MM/DD/YYYY
        ]
        
        for pattern in date_patterns:
            for match in re.finditer(pattern, text):
                date_str = match.group(0)
                context = self._get_context(text, match.span(), 100)
                
                # Extract names from context
                names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', context)
                
                connections.append({
                    'date': date_str,
                    'context': context,
                    'potential_entities': names,
                    'location': match.span()
                })
        
        return connections
    
    def _get_context(self, text: str, span: Tuple[int, int], window: int = 100) -> str:
        """Get context around a match"""
        start = max(0, span[0] - window)
        end = min(len(text), span[1] + window)
        return text[start:end]


class DocumentAnalyzer:
    """
    Main document analyzer combining all analysis capabilities
    """
    
    def __init__(self):
        self.redaction_detector = RedactionDetector()
        self.alias_tracker = AliasTracker()
        self.name_variation_detector = NameVariationDetector()
        self.connection_finder = HiddenConnectionFinder()
        self.analysis_results = []
    
    def analyze_document(self, text: str, entity_of_interest: Optional[str] = None) -> Dict:
        """
        Perform comprehensive analysis on a document
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'text_length': len(text),
            'entity_of_interest': entity_of_interest
        }
        
        # Detect redactions
        redactions = self.redaction_detector.detect_redactions(text)
        results['redactions'] = {
            'count': len(redactions),
            'items': redactions[:10],  # Limit to first 10
            'analysis': [
                self.redaction_detector.analyze_redaction_context(r)
                for r in redactions[:10]
            ]
        }
        
        # Detect cryptic identifiers
        cryptic = self.alias_tracker.detect_cryptic_patterns(text)
        results['cryptic_identifiers'] = {
            'count': len(cryptic),
            'items': cryptic[:20]
        }
        
        # Detect name variations
        if entity_of_interest:
            variations = self.name_variation_detector.detect_name_variations(entity_of_interest)
            results['name_variations'] = variations
            
            # Find potential children/family
            children = self.connection_finder.find_birth_patterns(text, entity_of_interest)
            family = self.connection_finder.find_family_relationships(text, entity_of_interest)
            
            results['potential_children'] = children
            results['family_relationships'] = family
        
        # Detect maiden names
        maiden_names = self.name_variation_detector.detect_maiden_name_pattern(text)
        results['maiden_names'] = maiden_names
        
        # Store results
        self.analysis_results.append(results)
        
        return results
    
    def generate_analysis_report(self, results: Dict) -> str:
        """Generate human-readable analysis report"""
        report = [
            "\n" + "="*70,
            "DOCUMENT ANALYSIS REPORT",
            "="*70,
            f"\nAnalysis Date: {results['timestamp']}",
            f"Document Length: {results['text_length']} characters",
        ]
        
        if results.get('entity_of_interest'):
            report.append(f"Entity of Interest: {results['entity_of_interest']}")
        
        # Redactions
        report.append("\n--- REDACTIONS DETECTED ---")
        report.append(f"Total Redactions: {results['redactions']['count']}")
        
        if results['redactions']['items']:
            report.append("\nRedaction Analysis:")
            for i, (redaction, analysis) in enumerate(zip(
                results['redactions']['items'][:5],
                results['redactions']['analysis'][:5]
            ), 1):
                report.append(f"\n{i}. Redaction Type: {analysis['likely_type']} "
                            f"(Confidence: {analysis['confidence']:.2f})")
                report.append(f"   Context: ...{redaction['before_context'][-30:]}"
                            f"[REDACTED]{redaction['after_context'][:30]}...")
                if analysis['clues']:
                    report.append(f"   Clues: {'; '.join(analysis['clues'])}")
        
        # Cryptic identifiers
        report.append("\n--- CRYPTIC IDENTIFIERS ---")
        report.append(f"Total Found: {results['cryptic_identifiers']['count']}")
        
        if results['cryptic_identifiers']['items']:
            for i, item in enumerate(results['cryptic_identifiers']['items'][:5], 1):
                report.append(f"\n{i}. Type: {item['type']}")
                report.append(f"   Identifier: {item['identifier']}")
                report.append(f"   Context: {item['context']}")
        
        # Children/Family
        if results.get('potential_children'):
            report.append("\n--- POTENTIAL CHILDREN/OFFSPRING ---")
            report.append(f"Total Patterns: {len(results['potential_children'])}")
            for i, child in enumerate(results['potential_children'][:3], 1):
                report.append(f"\n{i}. Pattern: {child['term']}")
                if child.get('dates'):
                    report.append(f"   Dates: {', '.join(child['dates'])}")
                if child.get('potential_names'):
                    report.append(f"   Names: {', '.join(child['potential_names'][:3])}")
        
        if results.get('family_relationships'):
            report.append("\n--- FAMILY RELATIONSHIPS ---")
            for i, rel in enumerate(results['family_relationships'][:3], 1):
                report.append(f"\n{i}. Relationship: {rel['relationship_type']} ({rel['term']})")
                if rel.get('potential_names'):
                    report.append(f"   Potential Names: {', '.join(rel['potential_names'][:3])}")
        
        # Maiden names
        if results.get('maiden_names'):
            report.append("\n--- NAME CHANGES DETECTED ---")
            for i, name in enumerate(results['maiden_names'], 1):
                if 'married_name' in name:
                    report.append(f"\n{i}. {name['married_name']} (née {name['maiden_name']})")
                else:
                    report.append(f"\n{i}. {name['current_name']} "
                                f"(formerly {name['former_name']})")
        
        report.append("\n" + "="*70)
        
        return "\n".join(report)


def main():
    """Demonstrate document analysis capabilities"""
    print("="*70)
    print("ADVANCED DOCUMENT ANALYSIS SYSTEM")
    print("="*70)
    print("\nCapabilities:")
    print("  • Redaction detection and context analysis")
    print("  • Cryptic identifier tracking")
    print("  • Name variation detection")
    print("  • Hidden connection discovery")
    print("  • Family relationship mapping")
    print("  • Temporal event tracking")
    print()
    
    # Example document with various patterns
    example_doc = """
    Flight logs show Subject-1 traveled with [REDACTED] on multiple occasions
    between 2000 and 2005. The individual known as "J.E." was accompanied by
    several associates including ███████ and another person referred to only
    as "G.M." in the documents.
    
    Records indicate that [REDACTED], daughter of Subject-1, was born in 2003.
    The mother's identity remains [WITHHELD] in official documents. Additional
    passengers listed include Mrs. Jane Smith (née Johnson) and her spouse.
    
    Financial transactions show payments to Individual-A totaling $███████
    on March 15, 2010. The recipient, formerly known as John Anderson, changed
    his name in 2009 according to court records.
    
    A child, referred to as "M" in communications, was mentioned in several
    emails from 2004. The relationship to Jeffrey Epstein remains unclear.
    """
    
    analyzer = DocumentAnalyzer()
    
    print("Analyzing example document...")
    results = analyzer.analyze_document(example_doc, entity_of_interest="Jeffrey Epstein")
    
    print(analyzer.generate_analysis_report(results))
    
    print("\n✓ Document analysis complete")
    print("✓ System ready for investigating redacted documents")
    print("✓ Cryptic identifier tracking operational")
    print("✓ Hidden connection discovery active")


if __name__ == "__main__":
    main()
