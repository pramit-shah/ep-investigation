#!/usr/bin/env python3
"""
Network Analysis Module for Epstein Investigation
Analyzes relationships and connections between entities
"""

import json
import os
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque


class NetworkAnalyzer:
    """Analyzes the network of connections in the investigation"""
    
    def __init__(self, entities: Dict, evidence: Dict):
        self.entities = entities
        self.evidence = evidence
        self.adjacency_list = self._build_adjacency_list()
    
    def _build_adjacency_list(self) -> Dict[str, List[Tuple[str, str, float]]]:
        """Build adjacency list from entity connections"""
        adj_list = defaultdict(list)
        
        for entity_name, entity in self.entities.items():
            for conn in entity.connections:
                connected_entity = conn['entity']
                relationship = conn['relationship']
                confidence = conn.get('confidence', 1.0)
                adj_list[entity_name].append((connected_entity, relationship, confidence))
        
        return dict(adj_list)
    
    def find_shortest_path(self, start: str, end: str) -> List[str]:
        """Find shortest path between two entities using BFS"""
        if start not in self.entities or end not in self.entities:
            return []
        
        if start == end:
            return [start]
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current in self.adjacency_list:
                for neighbor, _, _ in self.adjacency_list[current]:
                    if neighbor == end:
                        return path + [neighbor]
                    
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))
        
        return []  # No path found
    
    def find_all_paths(self, start: str, end: str, max_depth: int = 4) -> List[List[str]]:
        """Find all paths between two entities up to max_depth"""
        if start not in self.entities or end not in self.entities:
            return []
        
        all_paths = []
        
        def dfs(current: str, target: str, path: List[str], visited: Set[str], depth: int):
            if depth > max_depth:
                return
            
            if current == target:
                all_paths.append(path.copy())
                return
            
            if current in self.adjacency_list:
                for neighbor, _, _ in self.adjacency_list[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        path.append(neighbor)
                        dfs(neighbor, target, path, visited, depth + 1)
                        path.pop()
                        visited.remove(neighbor)
        
        dfs(start, end, [start], {start}, 0)
        return all_paths
    
    def calculate_centrality(self) -> Dict[str, float]:
        """Calculate degree centrality for each entity"""
        centrality = {}
        
        for entity_name in self.entities:
            # Count incoming and outgoing connections
            outgoing = len(self.adjacency_list.get(entity_name, []))
            incoming = sum(
                1 for neighbors in self.adjacency_list.values()
                for neighbor, _, _ in neighbors
                if neighbor == entity_name
            )
            
            centrality[entity_name] = outgoing + incoming
        
        # Normalize
        max_centrality = max(centrality.values()) if centrality else 1
        if max_centrality > 0:
            centrality = {k: v / max_centrality for k, v in centrality.items()}
        
        return centrality
    
    def find_clusters(self, min_cluster_size: int = 3) -> List[Set[str]]:
        """Identify clusters of highly connected entities"""
        visited = set()
        clusters = []
        
        def explore_cluster(start: str, cluster: Set[str]):
            if start in visited:
                return
            
            visited.add(start)
            cluster.add(start)
            
            if start in self.adjacency_list:
                for neighbor, _, confidence in self.adjacency_list[start]:
                    if neighbor not in visited and confidence >= 0.7:
                        explore_cluster(neighbor, cluster)
        
        for entity_name in self.entities:
            if entity_name not in visited:
                cluster = set()
                explore_cluster(entity_name, cluster)
                if len(cluster) >= min_cluster_size:
                    clusters.append(cluster)
        
        return clusters
    
    def identify_key_connectors(self, top_n: int = 10) -> List[Dict]:
        """Identify entities that connect different parts of the network"""
        centrality = self.calculate_centrality()
        
        connectors = []
        for entity_name, cent_score in centrality.items():
            if entity_name in self.entities:
                entity = self.entities[entity_name]
                connectors.append({
                    'name': entity_name,
                    'type': entity.entity_type,
                    'centrality_score': cent_score,
                    'connection_count': len(entity.connections),
                    'evidence_count': len(entity.evidence_ids)
                })
        
        return sorted(connectors, key=lambda x: x['centrality_score'], reverse=True)[:top_n]
    
    def analyze_connection_strength(self, entity1: str, entity2: str) -> Dict:
        """Analyze the strength of connection between two entities"""
        paths = self.find_all_paths(entity1, entity2, max_depth=3)
        
        # Find shared evidence
        shared_evidence = []
        if entity1 in self.entities and entity2 in self.entities:
            evidence1 = set(self.entities[entity1].evidence_ids)
            evidence2 = set(self.entities[entity2].evidence_ids)
            shared_evidence = list(evidence1 & evidence2)
        
        return {
            'entity1': entity1,
            'entity2': entity2,
            'direct_connection': any(
                entity2 == neighbor for neighbor, _, _ in self.adjacency_list.get(entity1, [])
            ),
            'path_count': len(paths),
            'shortest_path_length': len(min(paths, default=[])) - 1 if paths else -1,
            'shared_evidence_count': len(shared_evidence),
            'shared_evidence_ids': shared_evidence,
            'connection_strength': self._calculate_strength_score(paths, shared_evidence)
        }
    
    def _calculate_strength_score(self, paths: List[List[str]], 
                                  shared_evidence: List[str]) -> float:
        """Calculate overall connection strength score"""
        if not paths:
            return 0.0
        
        # Score based on path count, path lengths, and shared evidence
        path_score = min(len(paths) / 5.0, 1.0)  # Normalize to max of 1
        length_score = 1.0 / (len(min(paths, default=[1])))  # Shorter paths score higher
        evidence_score = min(len(shared_evidence) / 3.0, 1.0)  # Normalize to max of 1
        
        return (path_score + length_score + evidence_score) / 3.0
    
    def generate_network_report(self) -> str:
        """Generate a comprehensive network analysis report"""
        centrality = self.calculate_centrality()
        clusters = self.find_clusters()
        key_connectors = self.identify_key_connectors()
        
        report = [
            "\n" + "="*60,
            "NETWORK ANALYSIS REPORT",
            "="*60,
            f"\nTotal Entities: {len(self.entities)}",
            f"Total Connections: {sum(len(conns) for conns in self.adjacency_list.values())}",
            f"\nIdentified Clusters: {len(clusters)}",
        ]
        
        for i, cluster in enumerate(clusters, 1):
            report.append(f"  Cluster {i}: {len(cluster)} entities")
            if len(cluster) <= 5:
                report.append(f"    Members: {', '.join(cluster)}")
        
        report.append("\nTop Key Connectors:")
        for connector in key_connectors:
            report.append(
                f"  • {connector['name']} ({connector['type']}): "
                f"Centrality={connector['centrality_score']:.3f}, "
                f"Connections={connector['connection_count']}"
            )
        
        report.append("\n" + "="*60)
        return "\n".join(report)


class RelationshipMapper:
    """Maps and categorizes relationships between entities"""
    
    def __init__(self):
        self.relationship_types = {
            'business': ['business_partner', 'employer', 'employee', 'investor'],
            'social': ['friend', 'acquaintance', 'associate'],
            'legal': ['attorney', 'client', 'co-defendant', 'witness'],
            'family': ['spouse', 'child', 'parent', 'sibling', 'relative'],
            'institutional': ['member', 'board_member', 'donor', 'beneficiary'],
            'location': ['resident', 'visitor', 'owner', 'traveled_to'],
            'other': ['unknown', 'unspecified']
        }
    
    def categorize_relationship(self, relationship: str) -> str:
        """Categorize a relationship type"""
        relationship_lower = relationship.lower()
        
        for category, types in self.relationship_types.items():
            if any(rel_type in relationship_lower for rel_type in types):
                return category
        
        return 'other'
    
    def get_relationship_statistics(self, entities: Dict) -> Dict:
        """Get statistics on relationship types"""
        stats = defaultdict(int)
        
        for entity in entities.values():
            for conn in entity.connections:
                category = self.categorize_relationship(conn['relationship'])
                stats[category] += 1
        
        return dict(stats)


def main():
    """Demonstrate network analysis functionality"""
    print("Network Analysis Module for Epstein Investigation")
    print("="*50)
    
    # This would typically load from the investigation database
    print("\nThis module provides:")
    print("- Path finding between entities")
    print("- Network centrality analysis")
    print("- Cluster identification")
    print("- Connection strength analysis")
    print("- Key connector identification")


if __name__ == "__main__":
    main()
