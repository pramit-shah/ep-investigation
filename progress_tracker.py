#!/usr/bin/env python3
"""
Progress Tracking System
Continuously tracks and stores investigation progress
"""

import json
import os
from datetime import datetime
from pathlib import Path


class ProgressTracker:
    """Track investigation progress continuously"""
    
    def __init__(self, progress_file='data/progress.json'):
        self.progress_file = Path(progress_file)
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        self.progress = self.load_progress()
    
    def load_progress(self):
        """Load existing progress"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load progress: {e}")
                return self.create_initial_progress()
        else:
            return self.create_initial_progress()
    
    def create_initial_progress(self):
        """Create initial progress structure"""
        return {
            'created': datetime.utcnow().isoformat(),
            'last_updated': datetime.utcnow().isoformat(),
            'total_cycles': 0,
            'successful_cycles': 0,
            'failed_cycles': 0,
            'entities_discovered': 0,
            'connections_found': 0,
            'evidence_collected': 0,
            'knowledge_gaps_identified': 0,
            'knowledge_gaps_filled': 0,
            'errors_detected': 0,
            'errors_fixed': 0,
            'last_cycle': None,
            'cycle_history': []
        }
    
    def save_progress(self):
        """Save progress to file"""
        self.progress['last_updated'] = datetime.utcnow().isoformat()
        
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.progress, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save progress: {e}")
            return False
    
    def record_cycle(self, cycle_data):
        """Record a completed cycle"""
        self.progress['total_cycles'] += 1
        
        if cycle_data.get('success', False):
            self.progress['successful_cycles'] += 1
        else:
            self.progress['failed_cycles'] += 1
        
        # Update counters
        self.progress['entities_discovered'] += cycle_data.get('entities_discovered', 0)
        self.progress['connections_found'] += cycle_data.get('connections_found', 0)
        self.progress['evidence_collected'] += cycle_data.get('evidence_collected', 0)
        self.progress['knowledge_gaps_identified'] += cycle_data.get('knowledge_gaps_identified', 0)
        self.progress['knowledge_gaps_filled'] += cycle_data.get('knowledge_gaps_filled', 0)
        self.progress['errors_detected'] += cycle_data.get('errors_detected', 0)
        self.progress['errors_fixed'] += cycle_data.get('errors_fixed', 0)
        
        # Record cycle
        cycle_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'cycle_number': self.progress['total_cycles'],
            'success': cycle_data.get('success', False),
            'duration_minutes': cycle_data.get('duration_minutes', 0),
            'data': cycle_data
        }
        
        self.progress['cycle_history'].append(cycle_record)
        self.progress['last_cycle'] = cycle_record
        
        # Keep only last 100 cycles in history
        if len(self.progress['cycle_history']) > 100:
            self.progress['cycle_history'] = self.progress['cycle_history'][-100:]
        
        self.save_progress()
    
    def get_summary(self):
        """Get progress summary"""
        return {
            'total_cycles': self.progress['total_cycles'],
            'success_rate': (
                self.progress['successful_cycles'] / self.progress['total_cycles']
                if self.progress['total_cycles'] > 0 else 0
            ),
            'entities_discovered': self.progress['entities_discovered'],
            'connections_found': self.progress['connections_found'],
            'evidence_collected': self.progress['evidence_collected'],
            'knowledge_gaps': {
                'identified': self.progress['knowledge_gaps_identified'],
                'filled': self.progress['knowledge_gaps_filled'],
                'remaining': max(0, 
                    self.progress['knowledge_gaps_identified'] - 
                    self.progress['knowledge_gaps_filled']
                )
            },
            'errors': {
                'detected': self.progress['errors_detected'],
                'fixed': self.progress['errors_fixed'],
                'fix_rate': (
                    self.progress['errors_fixed'] / self.progress['errors_detected']
                    if self.progress['errors_detected'] > 0 else 0
                )
            },
            'last_cycle': self.progress['last_cycle']
        }
    
    def print_summary(self):
        """Print formatted progress summary"""
        summary = self.get_summary()
        
        print("="*60)
        print("Investigation Progress Summary")
        print("="*60)
        print()
        print(f"Total Cycles: {summary['total_cycles']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print()
        print("Discoveries:")
        print(f"  Entities: {summary['entities_discovered']}")
        print(f"  Connections: {summary['connections_found']}")
        print(f"  Evidence: {summary['evidence_collected']}")
        print()
        print("Knowledge Gaps:")
        print(f"  Identified: {summary['knowledge_gaps']['identified']}")
        print(f"  Filled: {summary['knowledge_gaps']['filled']}")
        print(f"  Remaining: {summary['knowledge_gaps']['remaining']}")
        print()
        print("Error Recovery:")
        print(f"  Detected: {summary['errors']['detected']}")
        print(f"  Fixed: {summary['errors']['fixed']}")
        print(f"  Fix Rate: {summary['errors']['fix_rate']:.1%}")
        print()
        
        if summary['last_cycle']:
            print("Last Cycle:")
            print(f"  Time: {summary['last_cycle']['timestamp']}")
            print(f"  Success: {summary['last_cycle']['success']}")
            print(f"  Duration: {summary['last_cycle']['duration_minutes']} minutes")
        
        print()
    
    def export_report(self, output_file='data/reports/progress_report.md'):
        """Export progress report as Markdown"""
        summary = self.get_summary()
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("# Investigation Progress Report\n\n")
            f.write(f"**Generated:** {datetime.utcnow().isoformat()} UTC\n\n")
            
            f.write("## Overview\n\n")
            f.write(f"- **Total Cycles:** {summary['total_cycles']}\n")
            f.write(f"- **Success Rate:** {summary['success_rate']:.1%}\n")
            f.write(f"- **Created:** {self.progress['created']}\n")
            f.write(f"- **Last Updated:** {self.progress['last_updated']}\n\n")
            
            f.write("## Discoveries\n\n")
            f.write("| Category | Count |\n")
            f.write("|----------|-------|\n")
            f.write(f"| Entities | {summary['entities_discovered']} |\n")
            f.write(f"| Connections | {summary['connections_found']} |\n")
            f.write(f"| Evidence | {summary['evidence_collected']} |\n\n")
            
            f.write("## Knowledge Gaps\n\n")
            f.write("| Status | Count |\n")
            f.write("|--------|-------|\n")
            f.write(f"| Identified | {summary['knowledge_gaps']['identified']} |\n")
            f.write(f"| Filled | {summary['knowledge_gaps']['filled']} |\n")
            f.write(f"| Remaining | {summary['knowledge_gaps']['remaining']} |\n\n")
            
            f.write("## Error Recovery\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| Errors Detected | {summary['errors']['detected']} |\n")
            f.write(f"| Errors Fixed | {summary['errors']['fixed']} |\n")
            f.write(f"| Fix Rate | {summary['errors']['fix_rate']:.1%} |\n\n")
            
            if summary['last_cycle']:
                f.write("## Last Cycle\n\n")
                f.write(f"- **Timestamp:** {summary['last_cycle']['timestamp']}\n")
                f.write(f"- **Cycle Number:** {summary['last_cycle']['cycle_number']}\n")
                f.write(f"- **Success:** {summary['last_cycle']['success']}\n")
                f.write(f"- **Duration:** {summary['last_cycle']['duration_minutes']} minutes\n\n")
            
            f.write("## Recent Cycle History\n\n")
            f.write("| Cycle | Timestamp | Success | Duration |\n")
            f.write("|-------|-----------|---------|----------|\n")
            
            for cycle in self.progress['cycle_history'][-10:]:
                f.write(f"| {cycle['cycle_number']} | {cycle['timestamp']} | ")
                f.write(f"{'✓' if cycle['success'] else '✗'} | ")
                f.write(f"{cycle['duration_minutes']} min |\n")
        
        print(f"Progress report exported to {output_path}")
        return output_path


def main():
    """Main entry point for testing"""
    tracker = ProgressTracker()
    tracker.print_summary()
    tracker.export_report()


if __name__ == "__main__":
    main()
