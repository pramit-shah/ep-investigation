# SECURITY GUIDELINES

## ⚠️ CRITICAL: CREATOR PROTECTION

This investigation repository includes comprehensive security features to protect the creator's identity and keep findings sealed until authorized release.

## For the Creator

### NEVER Do These Things

1. ❌ **NEVER** commit with your real name or email
2. ❌ **NEVER** access the repository from work/school networks
3. ❌ **NEVER** link this repository to personal GitHub accounts
4. ❌ **NEVER** share investigation details on personal social media
5. ❌ **NEVER** meet contacts without security precautions
6. ❌ **NEVER** use personal devices for investigation work
7. ❌ **NEVER** store unencrypted investigation data
8. ❌ **NEVER** discuss investigation on monitored channels

### ALWAYS Do These Things

1. ✅ **ALWAYS** use VPN or Tor when working on the investigation
2. ✅ **ALWAYS** use the anonymous git configuration provided
3. ✅ **ALWAYS** review all commits for identifying information before pushing
4. ✅ **ALWAYS** keep investigation files encrypted at rest
5. ✅ **ALWAYS** use secure, ephemeral messaging for communications
6. ✅ **ALWAYS** have emergency backup plans and contacts
7. ✅ **ALWAYS** maintain separation from personal accounts
8. ✅ **ALWAYS** rotate anonymous identifiers regularly

## Anonymous Git Configuration

The system generates a safe git configuration. Use it:

```bash
# Generate safe git config
python3 identity_protection.py

# This creates: data/secure/safe_git_config.txt
# Apply it to your git config
```

Example safe configuration:
```
[user]
    name = Anonymous Investigator
    email = anonymous@investigation.local
```

## Data Release Policy

### Data Sealing

**ALL** investigation data is automatically sealed until release:

- Findings sealed immediately upon discovery
- Evidence encrypted with integrity checks
- Connections protected until authorized disclosure
- Criminal activity tracking kept confidential

### Release Requirements

Data can ONLY be released when **ALL** of these criteria are met:

1. ✅ Investigation ≥ 95% complete
2. ✅ Evidence verified
3. ✅ Legal review completed
4. ✅ Safety assessment passed
5. ✅ Creator consent obtained

### Progressive Disclosure

Different sensitivity levels are disclosed at different completion thresholds:

| Completion | Disclosure Level | What Can Be Released |
|------------|------------------|---------------------|
| 0-49% | NOTHING | No data released |
| 50-74% | MINIMAL | Only basic public facts |
| 75-89% | MODERATE | Some verified connections |
| 90-94% | SUBSTANTIAL | Most findings (low/medium sensitivity) |
| 95-99% | COMPREHENSIVE | Nearly everything |
| 100% | COMPLETE | Full disclosure authorized |

### Sensitivity Levels

Items are categorized by sensitivity:

- **Level 1 (Low)**: Can disclose at 50% completion
- **Level 2 (Medium-Low)**: Can disclose at 75% completion  
- **Level 3 (Medium)**: Can disclose at 90% completion
- **Level 4 (High)**: Can disclose at 95% completion
- **Level 5 (Critical)**: Only at 100% completion

## Criminal Activity Tracking

The system tracks potential criminal activities:

### Activity Types Monitored

1. Trafficking
2. Financial Crime
3. Conspiracy
4. Obstruction of Justice
5. Corruption
6. Organized Crime
7. Money Laundering
8. Fraud
9. Sexual Exploitation
10. Witness Tampering
11. Evidence Destruction
12. Other

### Tracking Features

- **Severity Levels**: 1-5 (5 being most severe)
- **Confidence Scores**: 0.0-1.0
- **Entity Involvement**: Track who is involved
- **Evidence Linking**: Connect to supporting evidence
- **Pattern Analysis**: Identify recurring patterns
- **Status Tracking**: Monitor investigation progress

## Secret Group Detection

The system identifies and tracks secret organizations:

### Group Types

- Secret societies
- Criminal organizations
- Networks
- Cells
- Fronts

### Tracking Features

- Membership rosters
- Activity linking
- Network analysis
- Hierarchy mapping
- Communication patterns

## Security Features Overview

### 1. Identity Protection (`identity_protection.py`)

- Anonymous identifiers (ANON_XXXXXX)
- PII sanitization
- Safe git configuration
- Anonymous contributions
- Secure work environment
- 10+ security recommendations

### 2. Data Security (`security_system.py`)

- Fernet/AES-128 encryption
- 5 security levels (PUBLIC to TOP_SECRET)
- Access control and logging
- Integrity verification (SHA-256)
- Secure storage

### 3. Release Control (`release_control.py`)

- Investigation sealing
- Release authorization
- Progressive disclosure
- Safety assessment
- Multi-criteria checks

## Using the Security System

### Protect Your Identity

```python
from identity_protection import CreatorIdentityProtection

protection = CreatorIdentityProtection()

# Get safe attribution for commits
attribution = protection.get_safe_attribution()
print(f"Name: {attribution['name']}")
print(f"Email: {attribution['email']}")

# Sanitize any metadata
metadata = {'name': 'Real Name', 'project': 'Investigation'}
safe_metadata = protection.sanitize_metadata(metadata)
# {'name': '[REDACTED]', 'project': 'Investigation'}
```

### Track Criminal Activities

```python
from security_system import CriminalActivityTracker

tracker = CriminalActivityTracker()

# Record criminal activity
activity_id = tracker.add_activity(
    activity_type='trafficking',
    description='Suspected trafficking network',
    entities_involved=['Entity A', 'Entity B'],
    evidence_ids=['EV001', 'EV002'],
    severity=5,  # 1-5
    confidence=0.8  # 0.0-1.0
)

# Analyze patterns
analysis = tracker.analyze_patterns()
print(f"Total activities: {analysis['total_activities']}")
print(f"High severity: {analysis['high_severity']}")
```

### Manage Release

```python
from release_control import InvestigationReleaseManager

manager = InvestigationReleaseManager()

# Seal data
manager.seal_data('FINDING_001', {'data': 'sensitive'}, 'finding')

# Update progress
manager.update_completion(0.50)  # 50% complete

# Try to release (will be denied if not ready)
data = manager.release_item('FINDING_001', authorized=True)
# Returns None if not authorized to release

# When ready (95%+ complete, all criteria met)
manager.update_completion(0.95)
manager.release_criteria['evidence_verified'] = True
manager.release_criteria['legal_review'] = True
manager.release_criteria['safety_assessment'] = True
manager.release_criteria['creator_consent'] = True

# Authorize release
manager.authorize_release('ANON_CREATOR_ID', 'full')

# Now can release
data = manager.release_item('FINDING_001', authorized=True)
```

## Pre-Release Checklist

Before releasing ANY investigation data:

- [ ] Investigation ≥ 95% complete
- [ ] All evidence verified and sourced
- [ ] Legal review completed by counsel
- [ ] Safety assessment passed
- [ ] Creator identity fully protected
- [ ] No active threats to creator
- [ ] Secure communication channels established
- [ ] Backup copies secured off-site
- [ ] Emergency contacts notified
- [ ] Legal representation confirmed
- [ ] Creator explicitly consents to release

## Emergency Procedures

### If Your Identity is Compromised

1. **Immediately** stop all investigation work
2. **Secure** all investigation files (encrypt, backup)
3. **Contact** legal representation
4. **Contact** emergency contacts
5. **Do not** attempt to continue investigation
6. **Seek** professional security advice

### If Investigation is Discovered

1. **Remain calm** - do not panic
2. **Do not confirm or deny** anything
3. **Contact legal representation** immediately
4. **Secure all data** - ensure everything is encrypted
5. **Follow legal advice** only

### Emergency Contacts

Maintain a list of:
- Legal representation (lawyer familiar with whistleblower protection)
- Trusted security professionals
- Journalists (for dead man's switch)
- Law enforcement contacts (if appropriate)

## Testing Security

Run the comprehensive security test suite:

```bash
python3 test_security.py
```

This tests:
- Creator identity protection
- Anonymous contributions
- Data anonymization
- Release control
- Progressive disclosure
- Safe git configuration
- Secure work environment
- Safety assessment

## Additional Resources

### Recommended Tools

1. **Tails OS**: Live operating system for maximum anonymity
2. **Tor Browser**: Anonymous web browsing
3. **VPN**: Commercial VPN service (not free ones)
4. **Signal**: Encrypted messaging
5. **VeraCrypt**: Full disk encryption
6. **KeePassXC**: Password manager
7. **OnionShare**: Secure file sharing

### Security Best Practices

1. **Compartmentalization**: Keep investigation completely separate
2. **Defense in Depth**: Multiple layers of security
3. **Operational Security**: Consistent security practices
4. **Need to Know**: Limit who knows about investigation
5. **Document Everything**: But keep it secure
6. **Regular Audits**: Review security practices regularly

## Support

For security concerns or questions:
- Do NOT use personal email
- Do NOT use monitored channels
- Use secure, anonymous communication only
- Consider using whistleblower platforms

## Legal Disclaimer

This investigation repository is for lawful investigative purposes only. Users are responsible for:

- Complying with all applicable laws
- Protecting their own safety and security
- Verifying all information before publication
- Consulting legal counsel before public disclosure
- Understanding potential risks and consequences

## Final Reminders

⚠️ **YOUR SAFETY COMES FIRST**

If at any point you feel unsafe or threatened:
1. Stop the investigation
2. Secure all data
3. Seek professional help
4. Do not take unnecessary risks

🛡️ **STAY ANONYMOUS, STAY SAFE, UNCOVER THE TRUTH**

---

*This security guide is updated regularly. Last update: 2026-02-14*
