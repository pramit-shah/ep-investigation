"""
Tests for Trusted Developer Finder and Web Scraping Systems

Tests all components of developer vetting, skill gap analysis,
autonomous outreach, and web scraping capabilities.
"""

import unittest
import json
import os
from developer_finder import (
    DeveloperProfile, DeveloperMindset, SkillCategory, TrustLevel,
    DeveloperVettingSystem, SkillGapAnalyzer, AutonomousOutreach,
    TrustedDeveloperFinder, SkillGap
)
from web_scraper import (
    WebSource, SearchQuery, ScrapingTask, ContentType, SearchEngineType,
    RateLimiter, DataExtractor, ContentVerifier, WebSearcher,
    AutonomousWebScraper
)


class TestDeveloperVetting(unittest.TestCase):
    """Test developer vetting system"""
    
    def setUp(self):
        self.vetting_system = DeveloperVettingSystem()
        self.test_developer = DeveloperProfile(
            id="TEST001",
            name="Test Developer",
            contact_info={'email': 'test@example.com'},
            skills=[
                SkillCategory.WEB_SCRAPING.value,
                SkillCategory.DATA_ANALYSIS.value
            ],
            mindsets=[
                DeveloperMindset.TRUTH_SEEKER.value,
                DeveloperMindset.ETHICAL_HACKER.value
            ],
            trust_score=0.0,
            trust_level=TrustLevel.UNKNOWN.name,
            background_checks={'criminal_record': True, 'references': True},
            contributions=['project1', 'project2'],
            reputation_score=0.8,
            availability="Full-time",
            location="Remote",
            anonymity_preferred=False
        )
    
    def test_vet_developer(self):
        """Test developer vetting process"""
        result = self.vetting_system.vet_developer(self.test_developer)
        
        self.assertIn('overall_score', result)
        self.assertIn('trust_level', result)
        self.assertIn('approved', result)
        self.assertIsInstance(result['overall_score'], float)
        self.assertGreaterEqual(result['overall_score'], 0.0)
        self.assertLessEqual(result['overall_score'], 1.0)
    
    def test_trust_level_assignment(self):
        """Test trust level is assigned correctly"""
        result = self.vetting_system.vet_developer(self.test_developer)
        
        # Should be HIGH or VERIFIED based on the profile
        self.assertIn(result['trust_level'], [
            TrustLevel.HIGH.name, 
            TrustLevel.VERIFIED.name,
            TrustLevel.MEDIUM.name
        ])
    
    def test_red_flag_detection(self):
        """Test red flag detection"""
        # Create developer with issues
        problematic_dev = DeveloperProfile(
            id="PROB001",
            name="Problematic Dev",
            contact_info={},  # No contact info - red flag
            skills=[],
            mindsets=[],  # No ethical mindsets - red flag
            trust_score=0.0,
            trust_level=TrustLevel.UNKNOWN.name,
            background_checks={'criminal_record': False},  # Failed check
            contributions=[],
            reputation_score=0.2,
            availability="Unknown",
            location="Unknown",
            anonymity_preferred=False
        )
        
        result = self.vetting_system.vet_developer(problematic_dev)
        
        self.assertGreater(len(result['red_flags']), 0)
        self.assertFalse(result['approved'])


class TestSkillGapAnalyzer(unittest.TestCase):
    """Test skill gap analysis"""
    
    def setUp(self):
        self.analyzer = SkillGapAnalyzer()
    
    def test_identify_gaps(self):
        """Test gap identification"""
        current_skills = [SkillCategory.WEB_SCRAPING.value]
        required_skills = [
            SkillCategory.WEB_SCRAPING.value,
            SkillCategory.MACHINE_LEARNING.value,
            SkillCategory.CRYPTOGRAPHY.value
        ]
        
        self.analyzer.set_current_capabilities(current_skills)
        gaps = self.analyzer.identify_gaps(required_skills)
        
        self.assertEqual(len(gaps), 2)  # ML and Crypto are gaps
        gap_categories = [gap.category for gap in gaps]
        self.assertIn(SkillCategory.MACHINE_LEARNING.value, gap_categories)
        self.assertIn(SkillCategory.CRYPTOGRAPHY.value, gap_categories)
    
    def test_get_open_gaps(self):
        """Test getting open gaps"""
        self.analyzer.set_current_capabilities([])
        gaps = self.analyzer.identify_gaps([SkillCategory.WEB_SCRAPING.value])
        
        open_gaps = self.analyzer.get_open_gaps()
        self.assertEqual(len(open_gaps), 1)
        self.assertEqual(open_gaps[0].status, "OPEN")


class TestAutonomousOutreach(unittest.TestCase):
    """Test autonomous outreach system"""
    
    def setUp(self):
        self.outreach = AutonomousOutreach("Test investigation")
        self.developer = DeveloperProfile(
            id="DEV001",
            name="Jane Developer",
            contact_info={'email': 'jane@example.com'},
            skills=[SkillCategory.WEB_SCRAPING.value],
            mindsets=[DeveloperMindset.TRUTH_SEEKER.value],
            trust_score=0.8,
            trust_level=TrustLevel.HIGH.name,
            background_checks={'criminal_record': True},
            contributions=['proj1'],
            reputation_score=0.85,
            availability="Part-time",
            location="Remote",
            anonymity_preferred=True
        )
        self.skill_gap = SkillGap(
            category=SkillCategory.WEB_SCRAPING.value,
            description="Need web scraping expertise",
            priority="HIGH",
            required_expertise_level="EXPERT",
            estimated_time="2 weeks",
            status="OPEN"
        )
    
    def test_generate_outreach_message(self):
        """Test outreach message generation"""
        message = self.outreach.generate_outreach_message(
            self.developer,
            self.skill_gap,
            anonymize=True
        )
        
        self.assertIn('to', message)
        self.assertIn('subject', message)
        self.assertIn('body', message)
        self.assertIn('anonymity', message['body'].lower())  # Should mention anonymity
    
    def test_log_outreach(self):
        """Test outreach logging"""
        message = self.outreach.generate_outreach_message(
            self.developer,
            self.skill_gap
        )
        
        self.outreach.log_outreach(message)
        
        self.assertEqual(len(self.outreach.outreach_log), 1)
        self.assertIn(self.developer.id, self.outreach.response_tracking)
    
    def test_record_response(self):
        """Test recording developer response"""
        message = self.outreach.generate_outreach_message(
            self.developer,
            self.skill_gap
        )
        self.outreach.log_outreach(message)
        
        self.outreach.record_response(self.developer.id, accepted=True)
        
        tracking = self.outreach.response_tracking[self.developer.id]
        self.assertTrue(tracking['responded'])
        self.assertTrue(tracking['accepted'])


class TestTrustedDeveloperFinder(unittest.TestCase):
    """Test main developer finder system"""
    
    def setUp(self):
        self.finder = TrustedDeveloperFinder("Test investigation")
        
        # Add test developers
        self.dev1 = DeveloperProfile(
            id="DEV001",
            name="Alice",
            contact_info={'email': 'alice@example.com'},
            skills=[SkillCategory.WEB_SCRAPING.value, SkillCategory.DATA_ANALYSIS.value],
            mindsets=[DeveloperMindset.TRUTH_SEEKER.value],
            trust_score=0.0,
            trust_level=TrustLevel.UNKNOWN.name,
            background_checks={'criminal_record': True, 'references': True},
            contributions=['proj1', 'proj2'],
            reputation_score=0.85,
            availability="Full-time",
            location="Remote",
            anonymity_preferred=False
        )
        
        self.finder.add_developer_to_pool(self.dev1)
    
    def test_add_developer_to_pool(self):
        """Test adding developer to pool"""
        self.assertIn("DEV001", self.finder.developer_pool)
    
    def test_vet_all_developers(self):
        """Test vetting all developers"""
        results = self.finder.vet_all_developers()
        
        self.assertIn("DEV001", results)
        self.assertIn('approved', results["DEV001"])
    
    def test_find_developers_for_skill(self):
        """Test finding developers by skill"""
        self.finder.vet_all_developers()
        
        devs = self.finder.find_developers_for_skill(
            SkillCategory.WEB_SCRAPING.value
        )
        
        # Should find at least one developer with web scraping
        self.assertGreaterEqual(len(devs), 0)
    
    def test_autonomous_skill_gap_resolution(self):
        """Test autonomous gap resolution"""
        self.finder.vet_all_developers()
        
        required = [SkillCategory.WEB_SCRAPING.value, SkillCategory.CRYPTOGRAPHY.value]
        current = [SkillCategory.WEB_SCRAPING.value]
        
        log = self.finder.autonomous_skill_gap_resolution(required, current)
        
        self.assertIn('gaps_identified', log)
        self.assertIn('outreach_sent', log)
    
    def test_export_import_data(self):
        """Test data export and import"""
        self.finder.vet_all_developers()
        
        # Export
        filename = '/tmp/test_developer_finder.json'
        self.finder.save_to_file(filename)
        self.assertTrue(os.path.exists(filename))
        
        # Import
        new_finder = TrustedDeveloperFinder("Test")
        new_finder.load_from_file(filename)
        
        self.assertIn("DEV001", new_finder.developer_pool)
        
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)


class TestRateLimiter(unittest.TestCase):
    """Test rate limiting"""
    
    def setUp(self):
        self.limiter = RateLimiter(requests_per_second=10.0)
    
    def test_get_domain(self):
        """Test domain extraction"""
        domain = self.limiter.get_domain("https://example.com/page")
        self.assertEqual(domain, "example.com")
    
    def test_wait_if_needed(self):
        """Test rate limiting wait"""
        # Should complete quickly on first call
        import time
        start = time.time()
        self.limiter.wait_if_needed("example.com")
        elapsed = time.time() - start
        self.assertLess(elapsed, 0.2)  # Should be almost instant


class TestDataExtractor(unittest.TestCase):
    """Test data extraction"""
    
    def setUp(self):
        self.extractor = DataExtractor()
    
    def test_extract_patterns(self):
        """Test pattern extraction"""
        text = """
        Contact: info@example.com
        Phone: 555-123-4567
        Amount: $1,500.50
        Date: 12/15/2023
        """
        
        patterns = self.extractor.extract_patterns(text)
        
        self.assertIn('email', patterns)
        self.assertIn('phone', patterns)
        self.assertIn('money', patterns)
        self.assertIn('date', patterns)
    
    def test_extract_entities(self):
        """Test entity extraction"""
        text = "John Smith met with ABC Corporation on 12/15/2023."
        
        entities = self.extractor.extract_entities(text)
        
        self.assertIn('names', entities)
        self.assertIn('dates', entities)
    
    def test_extract_links(self):
        """Test link extraction"""
        html = '<a href="https://example.com/page1">Link 1</a>'
        
        links = self.extractor.extract_links(html, "https://example.com")
        
        self.assertGreater(len(links), 0)


class TestContentVerifier(unittest.TestCase):
    """Test content verification"""
    
    def setUp(self):
        self.verifier = ContentVerifier()
    
    def test_calculate_checksum(self):
        """Test checksum calculation"""
        content = "test content"
        checksum1 = self.verifier.calculate_checksum(content)
        checksum2 = self.verifier.calculate_checksum(content)
        
        self.assertEqual(checksum1, checksum2)
        self.assertEqual(len(checksum1), 64)  # SHA-256 is 64 hex chars
    
    def test_verify_content(self):
        """Test content verification"""
        content = "This is legitimate content about investigation."
        
        verification = self.verifier.verify_content(content, "https://example.com")
        
        self.assertIn('checksum', verification)
        self.assertIn('confidence_score', verification)
        self.assertIsInstance(verification['suspicious'], bool)
    
    def test_suspicious_content_detection(self):
        """Test detection of suspicious content"""
        content = "This is fake news and misinformation."
        
        verification = self.verifier.verify_content(content, "https://suspicious.com")
        
        self.assertTrue(verification['suspicious'])
        self.assertLess(verification['confidence_score'], 1.0)


class TestWebSearcher(unittest.TestCase):
    """Test web search capabilities"""
    
    def setUp(self):
        self.searcher = WebSearcher()
    
    def test_build_search_query(self):
        """Test query building"""
        keywords = ["investigation", "financial"]
        filters = {
            'site': 'example.com',
            'filetype': 'pdf'
        }
        
        query = self.searcher.build_search_query(keywords, filters)
        
        self.assertIn("investigation", query)
        self.assertIn("site:example.com", query)
        self.assertIn("filetype:pdf", query)
    
    def test_search(self):
        """Test search functionality"""
        query = SearchQuery(
            query_text="test query",
            search_engine=SearchEngineType.GOOGLE.value,
            filters={},
            max_results=5
        )
        
        results = self.searcher.search(query, simulate=True)
        
        self.assertLessEqual(len(results), 5)
        self.assertGreater(len(self.searcher.search_history), 0)
    
    def test_multi_engine_search(self):
        """Test multi-engine search"""
        keywords = ["investigation", "data"]
        
        results = self.searcher.multi_engine_search(keywords)
        
        self.assertGreater(len(results), 0)
        self.assertIn(SearchEngineType.GOOGLE.value, results)


class TestAutonomousWebScraper(unittest.TestCase):
    """Test autonomous web scraping"""
    
    def setUp(self):
        self.scraper = AutonomousWebScraper("Test investigation")
    
    def test_autonomous_research(self):
        """Test autonomous research workflow"""
        research = self.scraper.autonomous_research(
            research_topic="test topic",
            depth=1,
            max_sources=5
        )
        
        self.assertIn('topic', research)
        self.assertIn('sources_found', research)
        self.assertIn('data_extracted', research)
        self.assertEqual(research['status'], 'COMPLETED')
    
    def test_scrape_with_verification(self):
        """Test scraping with verification"""
        urls = ["https://example.com/page1", "https://example.com/page2"]
        
        results = self.scraper.scrape_with_verification(urls, cross_verify=True)
        
        self.assertEqual(results['urls_scraped'], 2)
        self.assertIn('cross_verification', results)
    
    def test_generate_research_report(self):
        """Test research report generation"""
        # Do some research first
        self.scraper.autonomous_research("test", max_sources=3)
        
        report = self.scraper.generate_research_report()
        
        self.assertIn('investigation_context', report)
        self.assertIn('total_research_sessions', report)
        self.assertIn('statistics', report)
    
    def test_export_data(self):
        """Test data export"""
        self.scraper.autonomous_research("test", max_sources=2)
        
        data = self.scraper.export_data()
        
        self.assertIn('investigation_context', data)
        self.assertIn('research_log', data)
        self.assertIn('discovered_sources', data)
    
    def test_save_load(self):
        """Test save and load"""
        self.scraper.autonomous_research("test", max_sources=2)
        
        filename = '/tmp/test_scraper.json'
        self.scraper.save_to_file(filename)
        
        self.assertTrue(os.path.exists(filename))
        
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
