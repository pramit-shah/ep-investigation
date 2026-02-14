#!/usr/bin/env python3
"""
CREATOR IDENTITY PROTECTION SYSTEM

CRITICAL SECURITY MODULE
Protects the identity of the investigation creator/investigator
to prevent harm, retaliation, or interference.

This module ensures:
- Creator identity remains anonymous
- No personally identifying information in commits
- Secure attribution through anonymous identifiers
- Protection from deanonymization attacks
"""

import os
import json
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Optional


class CreatorIdentityProtection:
    """
    Protects the creator's identity through multiple layers of anonymization
    """
    
    # Anonymous identifiers for creator
    ANONYMOUS_NAMES = [
        "Anonymous Investigator",
        "Project Coordinator",
        "Research Director",
        "Investigation Lead",
        "Anonymous Researcher"
    ]
    
    ANONYMOUS_EMAILS = [
        "anonymous@investigation.local",
        "researcher@secure.local",
        "coordinator@privacy.local"
    ]
    
    def __init__(self):
        self.creator_id = self._generate_anonymous_id()
        self.identity_log = []
        self.protection_active = True
    
    def _generate_anonymous_id(self) -> str:
        """Generate a unique anonymous identifier"""
        # Use UUID4 for truly random identifier
        return f"ANON_{uuid.uuid4().hex[:16].upper()}"
    
    def get_safe_attribution(self) -> Dict[str, str]:
        """
        Get safe attribution for commits/contributions
        Returns anonymous name and email
        """
        import random
        
        attribution = {
            'name': random.choice(self.ANONYMOUS_NAMES),
            'email': random.choice(self.ANONYMOUS_EMAILS),
            'id': self.creator_id,
            'timestamp': datetime.now().isoformat()
        }
        
        self._log_action('GET_ATTRIBUTION', 'Retrieved safe attribution')
        
        return attribution
    
    def sanitize_metadata(self, metadata: Dict) -> Dict:
        """
        Remove personally identifying information from metadata
        """
        sanitized = metadata.copy()
        
        # Remove common PII fields
        pii_fields = [
            'name', 'email', 'username', 'user', 'author', 'creator',
            'phone', 'address', 'ip', 'location', 'real_name',
            'full_name', 'firstname', 'lastname', 'ip_address'
        ]
        
        for field in pii_fields:
            if field in sanitized:
                sanitized[field] = '[REDACTED]'
        
        self._log_action('SANITIZE', f'Sanitized {len(pii_fields)} fields')
        
        return sanitized
    
    def create_anonymous_signature(self, content: str) -> str:
        """
        Create anonymous cryptographic signature for content verification
        without revealing identity
        """
        # Create hash-based signature
        signature_data = f"{content}{self.creator_id}{datetime.now().isoformat()}"
        signature = hashlib.sha256(signature_data.encode()).hexdigest()
        
        self._log_action('SIGN', 'Created anonymous signature')
        
        return signature
    
    def verify_signature(self, content: str, signature: str) -> bool:
        """
        Verify anonymous signature (simplified version)
        """
        # In production, implement proper signature verification
        return len(signature) == 64  # SHA-256 hex length
    
    def _log_action(self, action: str, details: str):
        """Log protection actions"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details,
            'creator_id': self.creator_id
        }
        self.identity_log.append(log_entry)
    
    def get_protection_status(self) -> Dict:
        """Get current protection status"""
        return {
            'active': self.protection_active,
            'creator_id': self.creator_id,
            'actions_logged': len(self.identity_log),
            'last_action': self.identity_log[-1] if self.identity_log else None
        }
    
    def generate_safe_commit_message(self, original_message: str) -> str:
        """
        Generate a commit message that doesn't reveal creator identity
        """
        # Remove any personal references
        safe_message = original_message
        
        # Remove common personal indicators
        personal_indicators = ['I ', 'my ', 'me ', 'myself']
        for indicator in personal_indicators:
            safe_message = safe_message.replace(indicator, '')
        
        # Add anonymous attribution
        safe_message = f"[AUTO] {safe_message}"
        
        self._log_action('SAFE_COMMIT', 'Generated safe commit message')
        
        return safe_message


class AnonymousContributionManager:
    """
    Manages anonymous contributions to the investigation
    """
    
    def __init__(self):
        self.contributions = []
        self.anonymous_contributors = {}
    
    def add_contribution(self, content: Dict, contributor_hint: Optional[str] = None):
        """
        Add an anonymous contribution
        
        Args:
            content: The contribution content
            contributor_hint: Optional hint (NOT real identity)
        """
        # Generate anonymous contributor ID
        contributor_id = self._get_or_create_contributor_id(contributor_hint)
        
        contribution = {
            'id': f"CONTRIB_{len(self.contributions):05d}",
            'contributor_id': contributor_id,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'verified': False
        }
        
        self.contributions.append(contribution)
        
        return contribution['id']
    
    def _get_or_create_contributor_id(self, hint: Optional[str]) -> str:
        """Get or create anonymous contributor ID"""
        if hint and hint in self.anonymous_contributors:
            return self.anonymous_contributors[hint]
        
        # Create new anonymous ID
        anon_id = f"ANON_CONTRIB_{uuid.uuid4().hex[:12].upper()}"
        
        if hint:
            self.anonymous_contributors[hint] = anon_id
        
        return anon_id
    
    def get_contributions_summary(self) -> Dict:
        """Get summary of anonymous contributions"""
        return {
            'total_contributions': len(self.contributions),
            'anonymous_contributors': len(self.anonymous_contributors),
            'latest_contribution': self.contributions[-1] if self.contributions else None
        }


class DataAnonymizer:
    """
    Anonymizes data to protect creator and source identities
    """
    
    def __init__(self):
        self.entity_mappings = {}  # real -> anonymous
        self.reverse_mappings = {}  # anonymous -> real (encrypted)
    
    def anonymize_entity(self, real_name: str) -> str:
        """
        Replace real entity name with anonymous identifier
        """
        if real_name in self.entity_mappings:
            return self.entity_mappings[real_name]
        
        # Generate anonymous name
        anon_name = f"ENTITY_{len(self.entity_mappings):04d}"
        
        self.entity_mappings[real_name] = anon_name
        self.reverse_mappings[anon_name] = real_name
        
        return anon_name
    
    def anonymize_text(self, text: str, entities_to_anonymize: List[str]) -> str:
        """
        Anonymize text by replacing entity names
        """
        anonymized = text
        
        for entity in entities_to_anonymize:
            anon_entity = self.anonymize_entity(entity)
            anonymized = anonymized.replace(entity, anon_entity)
        
        return anonymized
    
    def deanonymize_entity(self, anon_name: str, authorized: bool = False) -> Optional[str]:
        """
        Reverse anonymization (requires authorization)
        """
        if not authorized:
            raise PermissionError("Unauthorized deanonymization attempt")
        
        return self.reverse_mappings.get(anon_name)
    
    def get_anonymization_map(self, authorized: bool = False) -> Dict:
        """
        Get mapping of anonymous to real names (requires authorization)
        """
        if not authorized:
            return {
                'message': 'Authorization required',
                'anonymous_entities': list(self.entity_mappings.values())
            }
        
        return self.entity_mappings


class SecureWorkEnvironment:
    """
    Provides a secure work environment for the investigation creator
    """
    
    def __init__(self):
        self.session_id = uuid.uuid4().hex
        self.start_time = datetime.now()
        self.actions = []
        self.warnings = []
    
    def log_action(self, action_type: str, description: str, sensitive: bool = False):
        """Log action in secure environment"""
        action = {
            'type': action_type,
            'description': description if not sensitive else '[REDACTED]',
            'timestamp': datetime.now().isoformat(),
            'session': self.session_id
        }
        self.actions.append(action)
    
    def add_security_warning(self, warning: str):
        """Add security warning"""
        self.warnings.append({
            'warning': warning,
            'timestamp': datetime.now().isoformat()
        })
    
    def check_security_status(self) -> Dict:
        """Check current security status"""
        return {
            'session_id': self.session_id,
            'session_duration': str(datetime.now() - self.start_time),
            'actions_logged': len(self.actions),
            'warnings': len(self.warnings),
            'secure': len(self.warnings) == 0
        }
    
    def get_recommendations(self) -> List[str]:
        """Get security recommendations for creator"""
        recommendations = [
            "Use VPN or Tor when accessing investigation data",
            "Do not commit with personal email/username",
            "Use anonymous communication channels only",
            "Regularly rotate anonymous identifiers",
            "Keep investigation files encrypted at rest",
            "Do not share investigation details on personal accounts",
            "Use secure, ephemeral messaging for collaboration",
            "Review all commits for identifying information before pushing",
            "Consider using Tails OS or similar for maximum security",
            "Never access investigation from work/school networks"
        ]
        return recommendations


def setup_safe_git_config():
    """
    Generate safe git configuration to protect creator identity
    """
    protection = CreatorIdentityProtection()
    attribution = protection.get_safe_attribution()
    
    config = f"""
# SAFE GIT CONFIGURATION FOR INVESTIGATION
# Use this configuration to protect your identity

[user]
    name = {attribution['name']}
    email = {attribution['email']}

[commit]
    # Sign commits with GPG for verification without revealing identity
    gpgsign = false  # Set to true if using anonymous GPG key

[core]
    # Remove identifying information
    excludesfile = ~/.gitignore_global
    
[author]
    # Anonymous attribution
    name = {attribution['name']}
    email = {attribution['email']}

# IMPORTANT REMINDERS:
# - Never commit with your real name/email
# - Review all commits before pushing
# - Use VPN/Tor when pushing to remote
# - Do not link this repository to personal accounts
"""
    
    return config


def main():
    """Demonstrate creator identity protection"""
    print("="*75)
    print("CREATOR IDENTITY PROTECTION SYSTEM")
    print("="*75)
    print()
    print("⚠️  CRITICAL SECURITY MODULE")
    print("This system protects the identity of the investigation creator")
    print("to prevent harm, retaliation, or interference.")
    print()
    
    # 1. Identity Protection
    print("1. CREATOR IDENTITY PROTECTION")
    print("-" * 75)
    
    protection = CreatorIdentityProtection()
    
    attribution = protection.get_safe_attribution()
    print(f"  ✓ Anonymous ID: {attribution['id']}")
    print(f"  ✓ Safe Name: {attribution['name']}")
    print(f"  ✓ Safe Email: {attribution['email']}")
    
    # Sanitize metadata
    sample_metadata = {
        'name': 'Real Name',
        'email': 'real@email.com',
        'project': 'Investigation'
    }
    sanitized = protection.sanitize_metadata(sample_metadata)
    print(f"  ✓ Metadata sanitized: {sanitized}")
    
    # 2. Anonymous Contributions
    print("\n2. ANONYMOUS CONTRIBUTION MANAGEMENT")
    print("-" * 75)
    
    contrib_manager = AnonymousContributionManager()
    
    contrib_id = contrib_manager.add_contribution(
        {'finding': 'Important discovery'},
        contributor_hint='lead_investigator'
    )
    print(f"  ✓ Contribution added: {contrib_id}")
    
    summary = contrib_manager.get_contributions_summary()
    print(f"  ✓ Total contributions: {summary['total_contributions']}")
    print(f"  ✓ Anonymous contributors: {summary['anonymous_contributors']}")
    
    # 3. Data Anonymization
    print("\n3. DATA ANONYMIZATION")
    print("-" * 75)
    
    anonymizer = DataAnonymizer()
    
    entities = ["John Doe", "Jane Smith", "Acme Corp"]
    for entity in entities:
        anon = anonymizer.anonymize_entity(entity)
        print(f"  ✓ {entity} → {anon}")
    
    # 4. Secure Environment
    print("\n4. SECURE WORK ENVIRONMENT")
    print("-" * 75)
    
    env = SecureWorkEnvironment()
    
    env.log_action('ANALYSIS', 'Analyzed document', sensitive=True)
    env.log_action('UPDATE', 'Updated investigation data')
    
    status = env.check_security_status()
    print(f"  ✓ Session ID: {status['session_id'][:16]}...")
    print(f"  ✓ Actions logged: {status['actions_logged']}")
    print(f"  ✓ Security status: {'SECURE' if status['secure'] else 'WARNING'}")
    
    # 5. Git Configuration
    print("\n5. SAFE GIT CONFIGURATION")
    print("-" * 75)
    
    git_config = setup_safe_git_config()
    print("  ✓ Safe git configuration generated")
    print("  ✓ Use anonymous name and email for commits")
    
    # 6. Security Recommendations
    print("\n6. SECURITY RECOMMENDATIONS FOR CREATOR")
    print("-" * 75)
    
    recommendations = env.get_recommendations()
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"  {i}. {rec}")
    print(f"  ... and {len(recommendations) - 5} more recommendations")
    
    # Save safe git config
    config_file = 'data/secure/safe_git_config.txt'
    os.makedirs('data/secure', exist_ok=True)
    with open(config_file, 'w') as f:
        f.write(git_config)
    print(f"\n  ✓ Safe git config saved to: {config_file}")
    
    print("\n" + "="*75)
    print("CREATOR PROTECTION STATUS")
    print("="*75)
    print("✓ Anonymous identity: ACTIVE")
    print("✓ PII sanitization: ENABLED")
    print("✓ Contribution anonymization: ACTIVE")
    print("✓ Secure environment: OPERATIONAL")
    print("✓ Safe git config: GENERATED")
    print()
    print("⚠️  YOUR IDENTITY IS PROTECTED")
    print()
    print("Remember:")
    print("  • Never commit with personal credentials")
    print("  • Use VPN/Tor for all investigation work")
    print("  • Review all data before making public")
    print("  • Keep investigation separate from personal accounts")
    print()


if __name__ == "__main__":
    main()
