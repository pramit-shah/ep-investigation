"""
Developer Finder and Vetting System

This module helps find and vet trusted developers who can assist with the investigation
without compromising it. It evaluates developers based on mindset, skills, ethics,
and trustworthiness.

Key Features:
- Developer vetting and trust scoring
- Mindset assessment
- Skills gap identification
- Autonomous outreach
- Secure collaboration framework
- Background verification

Author: Investigation Team
"""

import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum


class DeveloperMindset(Enum):
    """Types of developer mindsets relevant for investigation work"""
    TRUTH_SEEKER = "truth_seeker"  # Motivated by uncovering truth
    JUSTICE_ORIENTED = "justice_oriented"  # Focused on justice
    ETHICAL_HACKER = "ethical_hacker"  # Security-minded, ethical
    OPEN_SOURCE_ADVOCATE = "open_source_advocate"  # Transparency-focused
    PRIVACY_ADVOCATE = "privacy_advocate"  # Values privacy and rights
    WHISTLEBLOWER_SUPPORTER = "whistleblower_supporter"  # Supports transparency
    INVESTIGATIVE_JOURNALIST = "investigative_journalist"  # Research-oriented
    DATA_SCIENTIST = "data_scientist"  # Analytical mindset
    FORENSIC_ANALYST = "forensic_analyst"  # Detail-oriented
    CIVIL_RIGHTS_ADVOCATE = "civil_rights_advocate"  # Human rights focused


class SkillCategory(Enum):
    """Categories of skills needed for investigation"""
    WEB_SCRAPING = "web_scraping"
    DATA_ANALYSIS = "data_analysis"
    NETWORK_ANALYSIS = "network_analysis"
    DOCUMENT_PROCESSING = "document_processing"
    CRYPTOGRAPHY = "cryptography"
    DATABASE_MANAGEMENT = "database_management"
    API_DEVELOPMENT = "api_development"
    MACHINE_LEARNING = "machine_learning"
    LEGAL_RESEARCH = "legal_research"
    OSINT = "osint"  # Open Source Intelligence
    DIGITAL_FORENSICS = "digital_forensics"
    BLOCKCHAIN_ANALYSIS = "blockchain_analysis"


class TrustLevel(Enum):
    """Trust levels for developers"""
    UNKNOWN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERIFIED = 4


@dataclass
class DeveloperProfile:
    """Profile of a potential collaborator developer"""
    id: str
    name: str
    contact_info: Dict[str, str]  # email, github, linkedin, etc.
    skills: List[str]
    mindsets: List[str]
    trust_score: float  # 0.0 to 1.0
    trust_level: str
    background_checks: Dict[str, bool]
    contributions: List[str]  # Previous open source work
    reputation_score: float  # Based on community standing
    availability: str
    location: str
    anonymity_preferred: bool
    verified_date: Optional[str] = None
    last_contact: Optional[str] = None
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SkillGap:
    """Represents a skill gap that needs external help"""
    category: str
    description: str
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    required_expertise_level: str  # BEGINNER, INTERMEDIATE, EXPERT
    estimated_time: str
    status: str  # OPEN, IN_PROGRESS, FILLED
    assigned_to: Optional[str] = None


class DeveloperVettingSystem:
    """Vets and scores developers for trustworthiness"""
    
    def __init__(self):
        self.criteria = {
            'open_source_contributions': 0.25,
            'ethical_track_record': 0.30,
            'technical_skills': 0.20,
            'community_reputation': 0.15,
            'background_verification': 0.10
        }
    
    def vet_developer(self, profile: DeveloperProfile) -> Dict:
        """Perform comprehensive vetting of a developer"""
        vetting_result = {
            'developer_id': profile.id,
            'name': profile.name,
            'timestamp': datetime.now().isoformat(),
            'scores': {},
            'overall_score': 0.0,
            'trust_level': TrustLevel.UNKNOWN.name,
            'recommendations': [],
            'red_flags': [],
            'approved': False
        }
        
        # Evaluate each criterion
        scores = {}
        scores['open_source_contributions'] = self._evaluate_open_source(profile)
        scores['ethical_track_record'] = self._evaluate_ethics(profile)
        scores['technical_skills'] = self._evaluate_skills(profile)
        scores['community_reputation'] = profile.reputation_score
        scores['background_verification'] = self._evaluate_background(profile)
        
        vetting_result['scores'] = scores
        
        # Calculate weighted overall score
        overall_score = sum(
            scores[criterion] * weight 
            for criterion, weight in self.criteria.items()
        )
        vetting_result['overall_score'] = overall_score
        
        # Determine trust level
        if overall_score >= 0.8:
            trust_level = TrustLevel.VERIFIED
            vetting_result['approved'] = True
        elif overall_score >= 0.6:
            trust_level = TrustLevel.HIGH
            vetting_result['approved'] = True
        elif overall_score >= 0.4:
            trust_level = TrustLevel.MEDIUM
        elif overall_score >= 0.2:
            trust_level = TrustLevel.LOW
        else:
            trust_level = TrustLevel.UNKNOWN
        
        vetting_result['trust_level'] = trust_level.name
        
        # Generate recommendations
        vetting_result['recommendations'] = self._generate_recommendations(scores)
        vetting_result['red_flags'] = self._identify_red_flags(profile, scores)
        
        return vetting_result
    
    def _evaluate_open_source(self, profile: DeveloperProfile) -> float:
        """Evaluate open source contributions"""
        if not profile.contributions:
            return 0.0
        
        # Score based on number and quality of contributions
        score = min(len(profile.contributions) / 10.0, 1.0)
        return score
    
    def _evaluate_ethics(self, profile: DeveloperProfile) -> float:
        """Evaluate ethical track record"""
        # Check for ethics-aligned mindsets
        ethical_mindsets = {
            DeveloperMindset.TRUTH_SEEKER.value,
            DeveloperMindset.JUSTICE_ORIENTED.value,
            DeveloperMindset.ETHICAL_HACKER.value,
            DeveloperMindset.PRIVACY_ADVOCATE.value,
            DeveloperMindset.WHISTLEBLOWER_SUPPORTER.value,
            DeveloperMindset.CIVIL_RIGHTS_ADVOCATE.value
        }
        
        matching_mindsets = set(profile.mindsets) & ethical_mindsets
        score = len(matching_mindsets) / len(ethical_mindsets)
        return score
    
    def _evaluate_skills(self, profile: DeveloperProfile) -> float:
        """Evaluate technical skills"""
        if not profile.skills:
            return 0.0
        
        # Score based on breadth and depth of skills
        score = min(len(profile.skills) / 8.0, 1.0)
        return score
    
    def _evaluate_background(self, profile: DeveloperProfile) -> float:
        """Evaluate background checks"""
        if not profile.background_checks:
            return 0.0
        
        passed_checks = sum(1 for passed in profile.background_checks.values() if passed)
        total_checks = len(profile.background_checks)
        
        return passed_checks / total_checks if total_checks > 0 else 0.0
    
    def _generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """Generate recommendations based on scores"""
        recommendations = []
        
        if scores['open_source_contributions'] < 0.5:
            recommendations.append("Request portfolio of previous work")
        
        if scores['ethical_track_record'] < 0.5:
            recommendations.append("Conduct additional ethics assessment")
        
        if scores['background_verification'] < 0.5:
            recommendations.append("Complete background verification")
        
        if scores['community_reputation'] < 0.5:
            recommendations.append("Check community references")
        
        return recommendations
    
    def _identify_red_flags(self, profile: DeveloperProfile, scores: Dict) -> List[str]:
        """Identify potential red flags"""
        red_flags = []
        
        if scores['ethical_track_record'] < 0.3:
            red_flags.append("Low ethical track record score")
        
        if scores['background_verification'] < 0.5:
            red_flags.append("Incomplete or failed background checks")
        
        if not profile.contact_info:
            red_flags.append("No verifiable contact information")
        
        return red_flags


class SkillGapAnalyzer:
    """Identifies skills gaps that require external help"""
    
    def __init__(self):
        self.current_capabilities: Set[str] = set()
        self.skill_gaps: List[SkillGap] = []
    
    def set_current_capabilities(self, skills: List[str]):
        """Set the current available skills"""
        self.current_capabilities = set(skills)
    
    def identify_gaps(self, required_skills: List[str]) -> List[SkillGap]:
        """Identify gaps between required and available skills"""
        gaps = []
        
        for skill in required_skills:
            if skill not in self.current_capabilities:
                gap = SkillGap(
                    category=skill,
                    description=f"Need expertise in {skill}",
                    priority="HIGH",
                    required_expertise_level="EXPERT",
                    estimated_time="Variable",
                    status="OPEN"
                )
                gaps.append(gap)
        
        self.skill_gaps.extend(gaps)
        return gaps
    
    def get_critical_gaps(self) -> List[SkillGap]:
        """Get critical skill gaps that need immediate attention"""
        return [gap for gap in self.skill_gaps if gap.priority == "CRITICAL"]
    
    def get_open_gaps(self) -> List[SkillGap]:
        """Get all open skill gaps"""
        return [gap for gap in self.skill_gaps if gap.status == "OPEN"]


class AutonomousOutreach:
    """Handles autonomous outreach to potential developer collaborators"""
    
    def __init__(self, investigation_context: str):
        self.investigation_context = investigation_context
        self.outreach_log: List[Dict] = []
        self.response_tracking: Dict[str, Dict] = {}
    
    def generate_outreach_message(
        self, 
        developer: DeveloperProfile, 
        skill_gap: SkillGap,
        anonymize: bool = True
    ) -> Dict:
        """Generate a secure outreach message"""
        
        message = {
            'to': developer.contact_info.get('email', 'Unknown'),
            'subject': 'Collaboration Opportunity - Investigation Research',
            'body': self._create_message_body(developer, skill_gap, anonymize),
            'timestamp': datetime.now().isoformat(),
            'developer_id': developer.id,
            'skill_gap': skill_gap.category,
            'anonymized': anonymize
        }
        
        return message
    
    def _create_message_body(
        self, 
        developer: DeveloperProfile, 
        skill_gap: SkillGap,
        anonymize: bool
    ) -> str:
        """Create the message body for outreach"""
        
        if anonymize:
            greeting = f"Hello,\n\n"
        else:
            greeting = f"Hello {developer.name},\n\n"
        
        body = greeting
        body += "We are conducting an important investigation focused on uncovering truth "
        body += "and bringing justice to light. Based on your background and skills, "
        body += f"we believe you could provide valuable assistance in {skill_gap.category}.\n\n"
        
        body += "This work involves:\n"
        body += f"- {skill_gap.description}\n"
        body += f"- Priority level: {skill_gap.priority}\n"
        body += f"- Required expertise: {skill_gap.required_expertise_level}\n\n"
        
        body += "We value:\n"
        body += "- Truth and transparency\n"
        body += "- Ethical conduct\n"
        body += "- Confidentiality and security\n"
        body += "- Anonymous contribution (if preferred)\n\n"
        
        if developer.anonymity_preferred:
            body += "We understand your preference for anonymity and will respect it fully.\n\n"
        
        body += "If you're interested in contributing to this important work, "
        body += "please respond at your convenience.\n\n"
        body += "Best regards,\n"
        body += "Investigation Research Team"
        
        return body
    
    def log_outreach(self, message: Dict):
        """Log an outreach attempt"""
        self.outreach_log.append(message)
        
        developer_id = message['developer_id']
        self.response_tracking[developer_id] = {
            'sent': message['timestamp'],
            'responded': False,
            'response_date': None,
            'accepted': False
        }
    
    def record_response(self, developer_id: str, accepted: bool):
        """Record a developer's response"""
        if developer_id in self.response_tracking:
            self.response_tracking[developer_id].update({
                'responded': True,
                'response_date': datetime.now().isoformat(),
                'accepted': accepted
            })


class TrustedDeveloperFinder:
    """Main system for finding and managing trusted developer collaborators"""
    
    def __init__(self, investigation_context: str):
        self.investigation_context = investigation_context
        self.vetting_system = DeveloperVettingSystem()
        self.skill_gap_analyzer = SkillGapAnalyzer()
        self.outreach_system = AutonomousOutreach(investigation_context)
        
        self.developer_pool: Dict[str, DeveloperProfile] = {}
        self.vetted_developers: Dict[str, Dict] = {}
        self.approved_collaborators: List[str] = []
    
    def add_developer_to_pool(self, profile: DeveloperProfile):
        """Add a developer to the pool for consideration"""
        self.developer_pool[profile.id] = profile
    
    def vet_all_developers(self) -> Dict[str, Dict]:
        """Vet all developers in the pool"""
        results = {}
        
        for dev_id, profile in self.developer_pool.items():
            vetting_result = self.vetting_system.vet_developer(profile)
            self.vetted_developers[dev_id] = vetting_result
            
            if vetting_result['approved']:
                self.approved_collaborators.append(dev_id)
            
            results[dev_id] = vetting_result
        
        return results
    
    def find_developers_for_skill(
        self, 
        skill: str, 
        min_trust_score: float = 0.6
    ) -> List[DeveloperProfile]:
        """Find approved developers with a specific skill"""
        matching_developers = []
        
        for dev_id in self.approved_collaborators:
            profile = self.developer_pool[dev_id]
            vetting = self.vetted_developers[dev_id]
            
            if (skill in profile.skills and 
                vetting['overall_score'] >= min_trust_score):
                matching_developers.append(profile)
        
        # Sort by trust score descending
        matching_developers.sort(
            key=lambda d: self.vetted_developers[d.id]['overall_score'],
            reverse=True
        )
        
        return matching_developers
    
    def autonomous_skill_gap_resolution(
        self, 
        required_skills: List[str],
        current_skills: List[str]
    ) -> Dict:
        """Autonomously identify gaps and reach out to developers"""
        
        # Set current capabilities
        self.skill_gap_analyzer.set_current_capabilities(current_skills)
        
        # Identify gaps
        gaps = self.skill_gap_analyzer.identify_gaps(required_skills)
        
        resolution_log = {
            'timestamp': datetime.now().isoformat(),
            'gaps_identified': len(gaps),
            'outreach_sent': 0,
            'developers_contacted': [],
            'gaps': []
        }
        
        # For each gap, find and contact suitable developers
        for gap in gaps:
            suitable_devs = self.find_developers_for_skill(gap.category)
            
            gap_info = {
                'category': gap.category,
                'priority': gap.priority,
                'developers_found': len(suitable_devs),
                'contacted': []
            }
            
            # Contact top 3 developers for each gap
            for dev in suitable_devs[:3]:
                message = self.outreach_system.generate_outreach_message(
                    dev, gap, anonymize=True
                )
                self.outreach_system.log_outreach(message)
                
                gap_info['contacted'].append(dev.id)
                resolution_log['developers_contacted'].append(dev.id)
                resolution_log['outreach_sent'] += 1
            
            resolution_log['gaps'].append(gap_info)
        
        return resolution_log
    
    def get_collaboration_status(self) -> Dict:
        """Get current status of developer collaborations"""
        return {
            'total_developers_in_pool': len(self.developer_pool),
            'vetted_developers': len(self.vetted_developers),
            'approved_collaborators': len(self.approved_collaborators),
            'outreach_sent': len(self.outreach_system.outreach_log),
            'responses_received': sum(
                1 for tracking in self.outreach_system.response_tracking.values()
                if tracking['responded']
            ),
            'accepted_collaborations': sum(
                1 for tracking in self.outreach_system.response_tracking.values()
                if tracking['accepted']
            ),
            'open_skill_gaps': len(self.skill_gap_analyzer.get_open_gaps())
        }
    
    def export_data(self) -> Dict:
        """Export all data for persistence"""
        return {
            'investigation_context': self.investigation_context,
            'developer_pool': {
                dev_id: profile.to_dict() 
                for dev_id, profile in self.developer_pool.items()
            },
            'vetted_developers': self.vetted_developers,
            'approved_collaborators': self.approved_collaborators,
            'outreach_log': self.outreach_system.outreach_log,
            'response_tracking': self.outreach_system.response_tracking,
            'skill_gaps': [asdict(gap) for gap in self.skill_gap_analyzer.skill_gaps]
        }
    
    def save_to_file(self, filename: str):
        """Save data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.export_data(), f, indent=2)
    
    def load_from_file(self, filename: str):
        """Load data from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Restore developer pool
        for dev_id, dev_data in data.get('developer_pool', {}).items():
            profile = DeveloperProfile(**dev_data)
            self.developer_pool[dev_id] = profile
        
        # Restore vetting results
        self.vetted_developers = data.get('vetted_developers', {})
        self.approved_collaborators = data.get('approved_collaborators', [])
        
        # Restore outreach data
        self.outreach_system.outreach_log = data.get('outreach_log', [])
        self.outreach_system.response_tracking = data.get('response_tracking', {})
        
        # Restore skill gaps
        for gap_data in data.get('skill_gaps', []):
            gap = SkillGap(**gap_data)
            self.skill_gap_analyzer.skill_gaps.append(gap)


# Example usage
if __name__ == "__main__":
    print("=== Trusted Developer Finder System ===\n")
    
    # Initialize the system
    finder = TrustedDeveloperFinder(
        investigation_context="Investigation requiring web scraping and data analysis"
    )
    
    # Create sample developer profiles
    dev1 = DeveloperProfile(
        id="DEV001",
        name="Alice Smith",
        contact_info={'email': 'alice@example.com', 'github': 'alice-dev'},
        skills=[
            SkillCategory.WEB_SCRAPING.value,
            SkillCategory.DATA_ANALYSIS.value,
            SkillCategory.OSINT.value
        ],
        mindsets=[
            DeveloperMindset.TRUTH_SEEKER.value,
            DeveloperMindset.ETHICAL_HACKER.value,
            DeveloperMindset.OPEN_SOURCE_ADVOCATE.value
        ],
        trust_score=0.0,
        trust_level=TrustLevel.UNKNOWN.name,
        background_checks={
            'criminal_record': True,
            'employment_history': True,
            'references': True
        },
        contributions=[
            'scrapy-project', 'pandas-contrib', 'osint-toolkit'
        ],
        reputation_score=0.85,
        availability="Part-time",
        location="Remote",
        anonymity_preferred=False
    )
    
    dev2 = DeveloperProfile(
        id="DEV002",
        name="Bob Johnson",
        contact_info={'email': 'bob@securemail.com'},
        skills=[
            SkillCategory.CRYPTOGRAPHY.value,
            SkillCategory.DIGITAL_FORENSICS.value,
            SkillCategory.NETWORK_ANALYSIS.value
        ],
        mindsets=[
            DeveloperMindset.PRIVACY_ADVOCATE.value,
            DeveloperMindset.WHISTLEBLOWER_SUPPORTER.value
        ],
        trust_score=0.0,
        trust_level=TrustLevel.UNKNOWN.name,
        background_checks={
            'criminal_record': True,
            'employment_history': True
        },
        contributions=[
            'encryption-lib', 'forensics-tools'
        ],
        reputation_score=0.75,
        availability="Full-time",
        location="Remote",
        anonymity_preferred=True
    )
    
    # Add developers to pool
    finder.add_developer_to_pool(dev1)
    finder.add_developer_to_pool(dev2)
    
    print("1. Vetting all developers...")
    vetting_results = finder.vet_all_developers()
    
    for dev_id, result in vetting_results.items():
        print(f"\n   Developer: {result['name']}")
        print(f"   Overall Score: {result['overall_score']:.2f}")
        print(f"   Trust Level: {result['trust_level']}")
        print(f"   Approved: {result['approved']}")
        if result['red_flags']:
            print(f"   Red Flags: {', '.join(result['red_flags'])}")
    
    print("\n2. Identifying skill gaps...")
    required_skills = [
        SkillCategory.WEB_SCRAPING.value,
        SkillCategory.BLOCKCHAIN_ANALYSIS.value,
        SkillCategory.MACHINE_LEARNING.value
    ]
    current_skills = [SkillCategory.WEB_SCRAPING.value]
    
    resolution = finder.autonomous_skill_gap_resolution(required_skills, current_skills)
    print(f"   Gaps identified: {resolution['gaps_identified']}")
    print(f"   Outreach messages sent: {resolution['outreach_sent']}")
    
    print("\n3. Collaboration status:")
    status = finder.get_collaboration_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n4. Saving data...")
    finder.save_to_file('/tmp/trusted_developers.json')
    print("   Data saved to /tmp/trusted_developers.json")
    
    print("\n=== System Ready ===")
