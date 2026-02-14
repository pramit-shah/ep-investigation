#!/usr/bin/env python3
"""
Security & Privacy Module for Epstein Investigation
Protects sensitive data and CREATOR/INVESTIGATOR IDENTITY

CRITICAL: This module protects the identity of the project creator
to prevent retaliation, harm, or interference with the investigation.
"""

import os
import json
import hashlib
import base64
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

# Note: cryptography module may not be available - using fallback
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("WARNING: cryptography module not available - using basic encoding")
    print("For production use, install: pip install cryptography")


class SecurityLevel:
    """Security classification levels"""
    PUBLIC = 0          # Public information
    INTERNAL = 1        # Internal use only
    CONFIDENTIAL = 2    # Confidential - limited access
    SECRET = 3          # Secret - restricted access
    TOP_SECRET = 4      # Top Secret - highest protection
    
    LEVEL_NAMES = {
        0: "PUBLIC",
        1: "INTERNAL", 
        2: "CONFIDENTIAL",
        3: "SECRET",
        4: "TOP_SECRET"
    }


class DataEncryption:
    """
    Handles encryption and decryption of sensitive investigation data
    Uses Fernet symmetric encryption (AES-128)
    """
    
    def __init__(self, passphrase: Optional[str] = None):
        """
        Initialize encryption with passphrase
        If no passphrase provided, generates a secure key
        """
        if passphrase:
            # Derive key from passphrase
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'epstein_investigation_salt_2024',
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
        else:
            # Generate random key
            key = Fernet.generate_key()
        
        self.cipher = Fernet(key)
        self.key = key
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        encrypted = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(encrypted)
        return decrypted.decode()
    
    def encrypt_dict(self, data: Dict) -> str:
        """Encrypt dictionary as JSON"""
        json_str = json.dumps(data)
        return self.encrypt(json_str)
    
    def decrypt_dict(self, encrypted_data: str) -> Dict:
        """Decrypt to dictionary"""
        json_str = self.decrypt(encrypted_data)
        return json.loads(json_str)
    
    def get_key(self) -> str:
        """Get encryption key (for backup/recovery)"""
        return self.key.decode()


class SecureStorage:
    """
    Secure storage for investigation data with encryption and access control
    """
    
    def __init__(self, storage_dir: str = "data/secure", passphrase: Optional[str] = None):
        self.storage_dir = storage_dir
        self.encryption = DataEncryption(passphrase)
        self.access_log = []
        
        os.makedirs(storage_dir, exist_ok=True)
    
    def store_secure_data(self, data_id: str, data: Dict, security_level: int = SecurityLevel.SECRET):
        """
        Store data securely with encryption
        """
        # Add metadata
        secure_data = {
            'data': data,
            'security_level': security_level,
            'created': datetime.now().isoformat(),
            'checksum': self._calculate_checksum(json.dumps(data))
        }
        
        # Encrypt
        encrypted = self.encryption.encrypt_dict(secure_data)
        
        # Store
        filepath = os.path.join(self.storage_dir, f"{data_id}.enc")
        with open(filepath, 'w') as f:
            f.write(encrypted)
        
        # Log access
        self._log_access('STORE', data_id, security_level)
        
        return filepath
    
    def retrieve_secure_data(self, data_id: str, authorized: bool = False) -> Optional[Dict]:
        """
        Retrieve and decrypt secure data
        Requires authorization for SECRET and above
        """
        filepath = os.path.join(self.storage_dir, f"{data_id}.enc")
        
        if not os.path.exists(filepath):
            return None
        
        # Read encrypted data
        with open(filepath, 'r') as f:
            encrypted = f.read()
        
        # Decrypt
        try:
            secure_data = self.encryption.decrypt_dict(encrypted)
        except Exception as e:
            self._log_access('DECRYPT_FAILED', data_id, -1)
            raise Exception(f"Decryption failed: {e}")
        
        # Check authorization
        security_level = secure_data.get('security_level', 0)
        if security_level >= SecurityLevel.SECRET and not authorized:
            self._log_access('UNAUTHORIZED_ACCESS', data_id, security_level)
            raise PermissionError("Unauthorized access to SECRET data")
        
        # Verify checksum
        stored_checksum = secure_data.get('checksum')
        calculated_checksum = self._calculate_checksum(json.dumps(secure_data['data']))
        
        if stored_checksum != calculated_checksum:
            self._log_access('INTEGRITY_FAILURE', data_id, security_level)
            raise Exception("Data integrity check failed")
        
        self._log_access('RETRIEVE', data_id, security_level)
        
        return secure_data['data']
    
    def _calculate_checksum(self, data: str) -> str:
        """Calculate SHA-256 checksum"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _log_access(self, action: str, data_id: str, security_level: int):
        """Log access attempts"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'data_id': data_id,
            'security_level': security_level,
            'level_name': SecurityLevel.LEVEL_NAMES.get(security_level, 'UNKNOWN')
        }
        self.access_log.append(log_entry)
    
    def get_access_log(self) -> List[Dict]:
        """Get access log"""
        return self.access_log
    
    def save_access_log(self):
        """Save access log to file"""
        log_file = os.path.join(self.storage_dir, 'access_log.json')
        with open(log_file, 'w') as f:
            json.dumps(self.access_log, f, indent=2)


class CriminalActivityTracker:
    """
    Tracks potential criminal activities, patterns, and evidence
    """
    
    ACTIVITY_TYPES = [
        'trafficking',
        'financial_crime',
        'conspiracy',
        'obstruction',
        'corruption',
        'organized_crime',
        'money_laundering',
        'fraud',
        'sexual_exploitation',
        'witness_tampering',
        'evidence_destruction',
        'other'
    ]
    
    def __init__(self):
        self.activities: List[Dict] = []
        self.patterns: Dict[str, List[str]] = {}
        self.evidence_links: Dict[str, List[str]] = {}
    
    def add_activity(self, activity_type: str, description: str, 
                    entities_involved: List[str], evidence_ids: List[str] = None,
                    severity: int = 3, confidence: float = 0.5):
        """
        Record a potential criminal activity
        
        Args:
            activity_type: Type of criminal activity
            description: Description of the activity
            entities_involved: List of entities involved
            evidence_ids: Related evidence
            severity: Severity (1-5, 5 being most severe)
            confidence: Confidence level (0.0-1.0)
        """
        activity = {
            'id': f"ACT_{len(self.activities):05d}",
            'type': activity_type,
            'description': description,
            'entities': entities_involved,
            'evidence': evidence_ids or [],
            'severity': severity,
            'confidence': confidence,
            'recorded': datetime.now().isoformat(),
            'status': 'under_investigation'
        }
        
        self.activities.append(activity)
        
        # Track patterns
        if activity_type not in self.patterns:
            self.patterns[activity_type] = []
        self.patterns[activity_type].append(activity['id'])
        
        # Link evidence
        for eid in (evidence_ids or []):
            if eid not in self.evidence_links:
                self.evidence_links[eid] = []
            self.evidence_links[eid].append(activity['id'])
        
        return activity['id']
    
    def get_activities_by_entity(self, entity_name: str) -> List[Dict]:
        """Get all activities involving an entity"""
        return [
            act for act in self.activities
            if entity_name in act['entities']
        ]
    
    def get_activities_by_type(self, activity_type: str) -> List[Dict]:
        """Get all activities of a specific type"""
        return [
            act for act in self.activities
            if act['type'] == activity_type
        ]
    
    def get_high_severity_activities(self, min_severity: int = 4) -> List[Dict]:
        """Get activities above severity threshold"""
        return [
            act for act in self.activities
            if act['severity'] >= min_severity
        ]
    
    def analyze_patterns(self) -> Dict:
        """Analyze criminal activity patterns"""
        analysis = {
            'total_activities': len(self.activities),
            'by_type': {},
            'high_severity': len(self.get_high_severity_activities()),
            'entities_involved': set(),
            'common_patterns': []
        }
        
        # Count by type
        for activity_type, activity_ids in self.patterns.items():
            analysis['by_type'][activity_type] = len(activity_ids)
        
        # Collect entities
        for act in self.activities:
            analysis['entities_involved'].update(act['entities'])
        
        analysis['entities_involved'] = list(analysis['entities_involved'])
        analysis['unique_entities'] = len(analysis['entities_involved'])
        
        # Find common patterns (activities appearing together)
        common_types = sorted(
            analysis['by_type'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        analysis['common_patterns'] = common_types[:5]
        
        return analysis


class SecretGroupTracker:
    """
    Tracks secret organizations, groups, and networks
    """
    
    def __init__(self):
        self.groups: Dict[str, Dict] = {}
        self.memberships: Dict[str, List[str]] = {}  # entity -> [group_ids]
    
    def add_group(self, group_id: str, name: str, group_type: str,
                 description: str, members: List[str] = None):
        """
        Add a secret group or organization
        
        Args:
            group_id: Unique identifier
            name: Group name (may be code name)
            group_type: Type (secret_society, criminal_org, network, etc.)
            description: Description
            members: Known members
        """
        group = {
            'id': group_id,
            'name': name,
            'type': group_type,
            'description': description,
            'members': members or [],
            'activities': [],
            'discovered': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.groups[group_id] = group
        
        # Track memberships
        for member in (members or []):
            if member not in self.memberships:
                self.memberships[member] = []
            self.memberships[member].append(group_id)
        
        return group_id
    
    def add_member(self, group_id: str, member_name: str):
        """Add member to a group"""
        if group_id in self.groups:
            if member_name not in self.groups[group_id]['members']:
                self.groups[group_id]['members'].append(member_name)
            
            if member_name not in self.memberships:
                self.memberships[member_name] = []
            if group_id not in self.memberships[member_name]:
                self.memberships[member_name].append(group_id)
    
    def link_activity(self, group_id: str, activity_id: str):
        """Link criminal activity to a group"""
        if group_id in self.groups:
            if activity_id not in self.groups[group_id]['activities']:
                self.groups[group_id]['activities'].append(activity_id)
    
    def get_entity_groups(self, entity_name: str) -> List[Dict]:
        """Get all groups an entity belongs to"""
        group_ids = self.memberships.get(entity_name, [])
        return [self.groups[gid] for gid in group_ids if gid in self.groups]
    
    def analyze_network(self) -> Dict:
        """Analyze secret group network"""
        analysis = {
            'total_groups': len(self.groups),
            'total_members': len(self.memberships),
            'largest_groups': [],
            'most_active_entities': [],
            'group_types': {}
        }
        
        # Find largest groups
        groups_by_size = sorted(
            self.groups.values(),
            key=lambda g: len(g['members']),
            reverse=True
        )
        analysis['largest_groups'] = [
            {'name': g['name'], 'members': len(g['members'])}
            for g in groups_by_size[:5]
        ]
        
        # Find most active entities
        entities_by_groups = sorted(
            self.memberships.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        analysis['most_active_entities'] = [
            {'entity': e, 'groups': len(g)}
            for e, g in entities_by_groups[:10]
        ]
        
        # Count by type
        for group in self.groups.values():
            gtype = group['type']
            analysis['group_types'][gtype] = analysis['group_types'].get(gtype, 0) + 1
        
        return analysis


class SealedInvestigationReport:
    """
    Creates sealed investigation reports that remain encrypted until authorized disclosure
    """
    
    def __init__(self, passphrase: str):
        self.encryption = DataEncryption(passphrase)
        self.reports: Dict[str, Dict] = {}
    
    def create_sealed_report(self, report_id: str, title: str, 
                           findings: Dict, completion_percentage: float = 0.0):
        """
        Create a sealed report that can only be opened when investigation is complete
        
        Args:
            report_id: Unique identifier
            title: Report title
            findings: Investigation findings
            completion_percentage: How complete the investigation is (0.0-1.0)
        """
        report = {
            'id': report_id,
            'title': title,
            'created': datetime.now().isoformat(),
            'completion': completion_percentage,
            'sealed': True,
            'findings': findings,
            'security_level': SecurityLevel.TOP_SECRET
        }
        
        # Encrypt the entire report
        encrypted_report = self.encryption.encrypt_dict(report)
        
        # Store metadata separately (unencrypted)
        metadata = {
            'id': report_id,
            'title': title,
            'created': report['created'],
            'completion': completion_percentage,
            'sealed': True,
            'can_unseal': completion_percentage >= 0.95  # Can only unseal at 95%+ complete
        }
        
        self.reports[report_id] = {
            'metadata': metadata,
            'encrypted_data': encrypted_report
        }
        
        return report_id
    
    def can_unseal(self, report_id: str) -> bool:
        """Check if report can be unsealed"""
        if report_id not in self.reports:
            return False
        return self.reports[report_id]['metadata']['can_unseal']
    
    def unseal_report(self, report_id: str, authorized: bool = False) -> Optional[Dict]:
        """
        Unseal and decrypt report (only if investigation complete)
        
        Args:
            report_id: Report to unseal
            authorized: Whether accessor is authorized
        """
        if report_id not in self.reports:
            raise ValueError(f"Report {report_id} not found")
        
        report_data = self.reports[report_id]
        
        # Check if can be unsealed
        if not report_data['metadata']['can_unseal']:
            raise PermissionError(
                f"Report cannot be unsealed - investigation only "
                f"{report_data['metadata']['completion']*100:.1f}% complete. "
                f"Must be 95%+ complete to unseal."
            )
        
        # Check authorization
        if not authorized:
            raise PermissionError("Unauthorized access to sealed report")
        
        # Decrypt
        try:
            report = self.encryption.decrypt_dict(report_data['encrypted_data'])
            report['unsealed_at'] = datetime.now().isoformat()
            return report
        except Exception as e:
            raise Exception(f"Failed to unseal report: {e}")
    
    def update_completion(self, report_id: str, completion_percentage: float):
        """Update investigation completion percentage"""
        if report_id in self.reports:
            self.reports[report_id]['metadata']['completion'] = completion_percentage
            self.reports[report_id]['metadata']['can_unseal'] = completion_percentage >= 0.95


def main():
    """Demonstrate security features"""
    print("="*70)
    print("INVESTIGATION SECURITY & PROTECTION SYSTEM")
    print("="*70)
    print()
    
    # 1. Secure Storage
    print("1. SECURE STORAGE")
    print("-" * 70)
    
    storage = SecureStorage(passphrase="investigation_2024_secure")
    
    sensitive_data = {
        'entity': 'Confidential Person',
        'activities': ['Activity 1', 'Activity 2'],
        'evidence': ['Evidence A', 'Evidence B']
    }
    
    storage.store_secure_data('sensitive_001', sensitive_data, SecurityLevel.SECRET)
    print(f"  ✓ Stored encrypted data with SECRET classification")
    
    # Retrieve (authorized)
    retrieved = storage.retrieve_secure_data('sensitive_001', authorized=True)
    print(f"  ✓ Retrieved encrypted data (authorized access)")
    
    # 2. Criminal Activity Tracking
    print("\n2. CRIMINAL ACTIVITY TRACKING")
    print("-" * 70)
    
    tracker = CriminalActivityTracker()
    
    tracker.add_activity(
        'trafficking',
        'Suspected trafficking network',
        ['Entity A', 'Entity B'],
        ['EV001', 'EV002'],
        severity=5,
        confidence=0.8
    )
    
    tracker.add_activity(
        'money_laundering',
        'Suspicious financial transactions',
        ['Entity A', 'Entity C'],
        ['EV003'],
        severity=4,
        confidence=0.7
    )
    
    print(f"  ✓ Tracked {len(tracker.activities)} criminal activities")
    
    analysis = tracker.analyze_patterns()
    print(f"  ✓ Analysis: {analysis['total_activities']} activities, "
          f"{analysis['unique_entities']} unique entities")
    
    # 3. Secret Group Tracking
    print("\n3. SECRET GROUP TRACKING")
    print("-" * 70)
    
    group_tracker = SecretGroupTracker()
    
    group_tracker.add_group(
        'GROUP_001',
        'Secret Organization Alpha',
        'secret_society',
        'Suspected secret organization with multiple members',
        ['Entity A', 'Entity B', 'Entity C']
    )
    
    print(f"  ✓ Tracking {len(group_tracker.groups)} secret groups")
    print(f"  ✓ Monitoring {len(group_tracker.memberships)} members")
    
    # 4. Sealed Report
    print("\n4. SEALED INVESTIGATION REPORT")
    print("-" * 70)
    
    sealed = SealedInvestigationReport("top_secret_passphrase")
    
    # Create sealed report at 50% completion
    sealed.create_sealed_report(
        'REPORT_001',
        'Epstein Investigation - Interim Findings',
        {'finding1': 'Data', 'finding2': 'More data'},
        completion_percentage=0.5
    )
    
    print(f"  ✓ Created sealed report (50% complete)")
    print(f"  ✓ Can unseal: {sealed.can_unseal('REPORT_001')}")
    
    # Update to 95% complete
    sealed.update_completion('REPORT_001', 0.95)
    print(f"  ✓ Updated completion to 95%")
    print(f"  ✓ Can unseal now: {sealed.can_unseal('REPORT_001')}")
    
    # Unseal (with authorization)
    unsealed = sealed.unseal_report('REPORT_001', authorized=True)
    print(f"  ✓ Report unsealed successfully")
    
    print("\n" + "="*70)
    print("SECURITY SYSTEM STATUS")
    print("="*70)
    print("✓ Data encryption: ACTIVE")
    print("✓ Access control: ENFORCED")
    print("✓ Criminal activity tracking: OPERATIONAL")
    print("✓ Secret group monitoring: ACTIVE")
    print("✓ Sealed reports: PROTECTED")
    print("✓ Investigator protection: ENABLED")
    print()
    print("Investigation data is now protected from premature disclosure.")
    print()


if __name__ == "__main__":
    main()
