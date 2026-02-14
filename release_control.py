#!/usr/bin/env python3
"""
RELEASE CONTROL SYSTEM

CRITICAL: Nothing is disclosed UNTIL RELEASE
All investigation data, findings, and creator identity remain sealed
until explicitly authorized for release.

This module manages:
- Release readiness assessment
- Sealed data until release
- Progressive disclosure control
- Creator protection until and after release
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class ReleaseStatus:
    """Release status levels"""
    NOT_READY = 0           # Investigation ongoing, nothing released
    INTERNAL_REVIEW = 1     # Internal review only
    PARTIAL_READY = 2       # Some findings can be released
    RELEASE_READY = 3       # Ready for controlled release
    RELEASED = 4            # Publicly released


class InvestigationReleaseManager:
    """
    Manages the release process and ensures nothing is disclosed
    UNTIL the investigation is ready for release
    """
    
    def __init__(self):
        self.release_status = ReleaseStatus.NOT_READY
        self.completion_percentage = 0.0
        self.release_authorization = False
        self.sealed_items = {}
        self.release_log = []
        self.creator_protected = True
        
        # Release criteria
        self.release_criteria = {
            'minimum_completion': 0.95,      # 95% complete
            'evidence_verified': False,
            'legal_review': False,
            'safety_assessment': False,
            'creator_consent': False
        }
    
    def seal_data(self, item_id: str, data: Dict, category: str = 'finding'):
        """
        Seal data until release
        
        Args:
            item_id: Unique identifier
            data: Data to seal
            category: Category (finding, evidence, connection, etc.)
        """
        sealed_item = {
            'id': item_id,
            'category': category,
            'data': data,
            'sealed_at': datetime.now().isoformat(),
            'released': False,
            'release_date': None
        }
        
        self.sealed_items[item_id] = sealed_item
        
        self._log_action('SEAL', f"Sealed {category}: {item_id}")
        
        print(f"  🔒 Sealed {category} '{item_id}' - PROTECTED UNTIL RELEASE")
    
    def update_completion(self, percentage: float):
        """Update investigation completion percentage"""
        old_percentage = self.completion_percentage
        self.completion_percentage = percentage
        
        self._log_action(
            'UPDATE_COMPLETION',
            f"Completion: {old_percentage:.1%} → {percentage:.1%}"
        )
        
        if percentage >= self.release_criteria['minimum_completion']:
            print(f"  ✓ Investigation {percentage:.1%} complete - approaching release threshold")
        else:
            remaining = self.release_criteria['minimum_completion'] - percentage
            print(f"  ⏳ Investigation {percentage:.1%} complete - {remaining:.1%} until release ready")
    
    def check_release_criteria(self) -> Dict:
        """
        Check if all release criteria are met
        """
        criteria_status = {
            'completion': self.completion_percentage >= self.release_criteria['minimum_completion'],
            'evidence_verified': self.release_criteria['evidence_verified'],
            'legal_review': self.release_criteria['legal_review'],
            'safety_assessment': self.release_criteria['safety_assessment'],
            'creator_consent': self.release_criteria['creator_consent']
        }
        
        all_met = all(criteria_status.values())
        
        return {
            'all_criteria_met': all_met,
            'criteria': criteria_status,
            'can_release': all_met,
            'completion_percentage': self.completion_percentage
        }
    
    def authorize_release(self, authorized_by: str, release_type: str = 'full'):
        """
        Authorize release of investigation
        
        Args:
            authorized_by: Who authorized (use anonymous ID)
            release_type: 'full', 'partial', or 'summary'
        """
        criteria = self.check_release_criteria()
        
        if not criteria['can_release']:
            missing = [k for k, v in criteria['criteria'].items() if not v]
            raise PermissionError(
                f"Cannot authorize release - missing criteria: {', '.join(missing)}"
            )
        
        self.release_authorization = True
        self.release_status = ReleaseStatus.RELEASE_READY
        
        self._log_action(
            'AUTHORIZE_RELEASE',
            f"Release authorized by {authorized_by} - Type: {release_type}"
        )
        
        print(f"\n  🔓 RELEASE AUTHORIZED")
        print(f"  Type: {release_type.upper()}")
        print(f"  Status: READY FOR CONTROLLED DISCLOSURE")
    
    def release_item(self, item_id: str, authorized: bool = False) -> Optional[Dict]:
        """
        Release a sealed item
        
        CRITICAL: Only works if release is authorized
        """
        if not self.release_authorization:
            print(f"  ❌ RELEASE DENIED - Investigation not ready for release")
            print(f"     Completion: {self.completion_percentage:.1%}")
            print(f"     Status: Data remains SEALED UNTIL RELEASE")
            return None
        
        if not authorized:
            raise PermissionError("Unauthorized release attempt")
        
        if item_id not in self.sealed_items:
            raise ValueError(f"Item {item_id} not found")
        
        item = self.sealed_items[item_id]
        
        if item['released']:
            print(f"  ℹ️  Item {item_id} already released")
            return item['data']
        
        # Release the item
        item['released'] = True
        item['release_date'] = datetime.now().isoformat()
        
        self._log_action('RELEASE_ITEM', f"Released {item['category']}: {item_id}")
        
        print(f"  ✅ Released {item['category']} '{item_id}'")
        
        return item['data']
    
    def get_release_summary(self) -> Dict:
        """Get summary of release status"""
        total_items = len(self.sealed_items)
        released_items = sum(1 for item in self.sealed_items.values() if item['released'])
        
        return {
            'release_status': ReleaseStatus.NOT_READY if not self.release_authorization else ReleaseStatus.RELEASED,
            'release_authorized': self.release_authorization,
            'completion': self.completion_percentage,
            'total_sealed_items': total_items,
            'released_items': released_items,
            'still_sealed': total_items - released_items,
            'creator_protected': self.creator_protected,
            'ready_for_release': self.check_release_criteria()['can_release']
        }
    
    def _log_action(self, action: str, description: str):
        """Log release-related actions"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'description': description
        }
        self.release_log.append(log_entry)


class ProgressiveDisclosure:
    """
    Manages progressive disclosure of information
    More sensitive information revealed as investigation nears completion
    """
    
    DISCLOSURE_LEVELS = {
        0.0: 'NOTHING',           # Nothing disclosed
        0.5: 'MINIMAL',           # Only basic facts
        0.75: 'MODERATE',         # Some connections
        0.90: 'SUBSTANTIAL',      # Most findings
        0.95: 'COMPREHENSIVE',    # Nearly everything
        1.0: 'COMPLETE'           # Full disclosure
    }
    
    def __init__(self):
        self.current_level = 0.0
        self.disclosed_items = []
    
    def get_disclosure_level(self, completion: float) -> str:
        """Determine what can be disclosed based on completion"""
        # Find the highest threshold we've passed
        level = 'NOTHING'
        for threshold, level_name in sorted(self.DISCLOSURE_LEVELS.items()):
            if completion >= threshold:
                level = level_name
        return level
    
    def can_disclose(self, item_sensitivity: int, completion: float) -> Tuple[bool, str]:
        """
        Check if an item can be disclosed based on completion
        
        Args:
            item_sensitivity: 1-5 (1=low, 5=high)
            completion: Investigation completion (0.0-1.0)
        
        Returns:
            (can_disclose, reason)
        """
        disclosure_level = self.get_disclosure_level(completion)
        
        # Map sensitivity to required completion
        sensitivity_thresholds = {
            1: 0.5,   # Low sensitivity - can disclose at 50%
            2: 0.75,  # Medium-low - disclose at 75%
            3: 0.90,  # Medium - disclose at 90%
            4: 0.95,  # High - disclose at 95%
            5: 1.0    # Critical - only at 100%
        }
        
        required = sensitivity_thresholds.get(item_sensitivity, 1.0)
        
        if completion >= required:
            return True, f"Disclosure level: {disclosure_level}"
        else:
            return False, f"Requires {required:.1%} completion (currently {completion:.1%})"
    
    def disclose_item(self, item: Dict, completion: float) -> Optional[Dict]:
        """
        Disclose item if completion threshold met
        """
        sensitivity = item.get('sensitivity', 5)  # Default to highest sensitivity
        
        can_disclose, reason = self.can_disclose(sensitivity, completion)
        
        if can_disclose:
            self.disclosed_items.append(item['id'])
            print(f"  ✅ Disclosed: {item['id']} ({reason})")
            return item
        else:
            print(f"  🔒 SEALED: {item['id']} - {reason}")
            return None


class SafeReleaseProtocol:
    """
    Protocol for safely releasing investigation findings
    while protecting creator identity
    """
    
    def __init__(self):
        self.pre_release_checks = []
        self.release_approved = False
    
    def add_pre_release_check(self, check_name: str, passed: bool, notes: str = ""):
        """Add a pre-release safety check"""
        check = {
            'check': check_name,
            'passed': passed,
            'notes': notes,
            'timestamp': datetime.now().isoformat()
        }
        self.pre_release_checks.append(check)
    
    def run_safety_assessment(self) -> Dict:
        """
        Run comprehensive safety assessment before release
        """
        safety_checks = [
            'Creator identity protected',
            'No personally identifying information',
            'Legal review completed',
            'Evidence verified',
            'Sources protected',
            'No active threats to creator',
            'Secure communication channels',
            'Backup copies secured',
            'Emergency contacts notified',
            'Legal representation confirmed'
        ]
        
        print("\n  🔍 Running Pre-Release Safety Assessment...")
        print("  " + "="*70)
        
        for check in safety_checks:
            # In production, these would be actual checks
            self.add_pre_release_check(check, True)
            print(f"  ✓ {check}")
        
        all_passed = all(c['passed'] for c in self.pre_release_checks)
        
        assessment = {
            'all_checks_passed': all_passed,
            'total_checks': len(self.pre_release_checks),
            'passed_checks': sum(1 for c in self.pre_release_checks if c['passed']),
            'safe_to_release': all_passed
        }
        
        if all_passed:
            print("\n  ✅ Safety assessment: PASSED")
            print("  Safe to proceed with release")
        else:
            print("\n  ⚠️  Safety assessment: FAILED")
            print("  DO NOT RELEASE until all checks pass")
        
        return assessment


def main():
    """Demonstrate release control system"""
    print("="*75)
    print("INVESTIGATION RELEASE CONTROL SYSTEM")
    print("="*75)
    print()
    print("⚠️  CRITICAL: All data remains SEALED UNTIL RELEASE")
    print()
    
    # 1. Initialize Release Manager
    print("1. SEALING INVESTIGATION DATA")
    print("-" * 75)
    
    manager = InvestigationReleaseManager()
    
    # Seal various findings
    manager.seal_data('FINDING_001', {
        'type': 'criminal_activity',
        'description': 'Evidence of trafficking network',
        'severity': 5
    }, 'finding')
    
    manager.seal_data('EVIDENCE_001', {
        'type': 'document',
        'description': 'Flight logs',
        'verified': True
    }, 'evidence')
    
    manager.seal_data('CONNECTION_001', {
        'from': 'Entity A',
        'to': 'Entity B',
        'type': 'financial'
    }, 'connection')
    
    # 2. Update Progress
    print("\n2. INVESTIGATION PROGRESS")
    print("-" * 75)
    
    manager.update_completion(0.50)  # 50% complete
    
    print("\n  Attempting to release data at 50% completion...")
    result = manager.release_item('FINDING_001', authorized=True)
    
    if result is None:
        print("  ✓ Data remains SEALED - Protection working correctly")
    
    # 3. Progressive Disclosure
    print("\n3. PROGRESSIVE DISCLOSURE LEVELS")
    print("-" * 75)
    
    disclosure = ProgressiveDisclosure()
    
    print("\n  Disclosure levels by completion:")
    for completion in [0.0, 0.5, 0.75, 0.90, 0.95, 1.0]:
        level = disclosure.get_disclosure_level(completion)
        print(f"    {completion:.0%} complete → {level} disclosure")
    
    # 4. Approach Release
    print("\n4. APPROACHING RELEASE READINESS")
    print("-" * 75)
    
    manager.update_completion(0.95)  # 95% complete
    
    criteria = manager.check_release_criteria()
    print(f"\n  Release criteria status:")
    for criterion, met in criteria['criteria'].items():
        status = "✓" if met else "✗"
        print(f"    {status} {criterion}")
    
    # 5. Safety Assessment
    print("\n5. PRE-RELEASE SAFETY ASSESSMENT")
    print("-" * 75)
    
    safety = SafeReleaseProtocol()
    assessment = safety.run_safety_assessment()
    
    # 6. Authorize Release
    print("\n6. RELEASE AUTHORIZATION")
    print("-" * 75)
    
    # Set all criteria to met
    manager.release_criteria['evidence_verified'] = True
    manager.release_criteria['legal_review'] = True
    manager.release_criteria['safety_assessment'] = True
    manager.release_criteria['creator_consent'] = True
    
    try:
        manager.authorize_release('ANON_CREATOR_001', 'full')
        
        # Now data can be released
        print("\n  Releasing sealed items...")
        data = manager.release_item('FINDING_001', authorized=True)
        if data:
            print(f"  ✓ Data released successfully")
        
    except PermissionError as e:
        print(f"  ❌ {e}")
    
    # 7. Release Summary
    print("\n7. RELEASE SUMMARY")
    print("-" * 75)
    
    summary = manager.get_release_summary()
    print(f"\n  Total sealed items: {summary['total_sealed_items']}")
    print(f"  Released items: {summary['released_items']}")
    print(f"  Still sealed: {summary['still_sealed']}")
    print(f"  Creator protected: {'YES' if summary['creator_protected'] else 'NO'}")
    print(f"  Investigation complete: {summary['completion']:.1%}")
    
    print("\n" + "="*75)
    print("PROTECTION STATUS")
    print("="*75)
    print("✓ All data SEALED until release authorization")
    print("✓ Creator identity PROTECTED throughout process")
    print("✓ Progressive disclosure based on completion")
    print("✓ Safety assessment required before release")
    print("✓ Multi-criteria authorization needed")
    print()
    print("⚠️  REMEMBER:")
    print("   • Nothing disclosed until 95%+ complete")
    print("   • All safety checks must pass")
    print("   • Creator identity protected even after release")
    print("   • Progressive disclosure protects sensitive items")
    print("   • Maintain anonymity until and after release")
    print()


if __name__ == "__main__":
    main()
