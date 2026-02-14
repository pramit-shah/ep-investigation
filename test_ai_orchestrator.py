"""
Tests for AI Orchestration System with Full Autonomous Control
"""

import unittest
import json
import os
from datetime import datetime, timedelta

from ai_orchestrator import (
    AIOrchestrator,
    KnowledgeGapAnalyzer,
    AISystemCapabilityMatcher,
    LongGameStrategyPlanner,
    IncompleteDataHandler,
    KnowledgeGap,
    ResearchTask,
    ResearchHypothesis,
    AISystemType,
    InformationNeedPriority
)


class TestKnowledgeGapAnalyzer(unittest.TestCase):
    """Test knowledge gap identification"""
    
    def setUp(self):
        self.analyzer = KnowledgeGapAnalyzer()
    
    def test_analyze_entity_missing_fields(self):
        """Test detection of missing entity fields"""
        entity = {
            'id': 'E1',
            'name': 'Test Entity'
            # Missing type and description
        }
        
        gaps = self.analyzer.analyze_entity(entity)
        
        # Should find gaps for missing type and description
        self.assertGreater(len(gaps), 0)
        gap_descriptions = [g.description for g in gaps]
        self.assertTrue(any('type' in desc for desc in gap_descriptions))
    
    def test_analyze_entity_missing_connections(self):
        """Test detection of insufficient connections"""
        entity = {
            'id': 'E1',
            'name': 'Test',
            'type': 'person',
            'description': 'A test',
            'connections': []  # No connections
        }
        
        gaps = self.analyzer.analyze_entity(entity)
        
        # Should identify connection gap
        self.assertTrue(any('connection' in g.description.lower() for g in gaps))
    
    def test_identify_pattern_gaps(self):
        """Test pattern-based gap identification"""
        data = {
            'entities': [{'id': f'E{i}'} for i in range(20)],  # Many entities
            'connections': []  # But no connections - pattern issue
        }
        
        gaps = self.analyzer.identify_pattern_gaps(data)
        
        # Should detect sparse network
        self.assertGreater(len(gaps), 0)
        self.assertTrue(any('sparse' in g.description.lower() for g in gaps))
    
    def test_discover_undocumented_needs(self):
        """Test discovery of implicit information needs"""
        context = "Investigation of trafficking and transportation crimes"
        
        gaps = self.analyzer.discover_undocumented_needs(context)
        
        # Should identify need for travel records
        self.assertGreater(len(gaps), 0)
        self.assertTrue(any('travel' in g.description.lower() for g in gaps))


class TestAISystemCapabilityMatcher(unittest.TestCase):
    """Test AI system selection"""
    
    def setUp(self):
        self.matcher = AISystemCapabilityMatcher()
    
    def test_capabilities_defined(self):
        """Test that capabilities are properly defined"""
        self.assertGreater(len(self.matcher.capabilities), 0)
        
        # Check web search capabilities
        web_search = self.matcher.capabilities[AISystemType.WEB_SEARCH]
        self.assertIn('strengths', web_search)
        self.assertIn('weaknesses', web_search)
        self.assertIn('reliability', web_search)
    
    def test_select_ai_systems_for_network_gap(self):
        """Test selection for network-related gaps"""
        gap = KnowledgeGap(
            gap_id="test1",
            description="Missing connection information",
            context="Network analysis needed",
            priority=InformationNeedPriority.HIGH
        )
        
        systems = self.matcher.select_ai_systems(gap)
        
        self.assertIn(AISystemType.NETWORK_ANALYSIS, systems)
    
    def test_select_ai_systems_for_financial_gap(self):
        """Test selection for financial gaps"""
        gap = KnowledgeGap(
            gap_id="test2",
            description="Missing financial transaction data",
            context="Money flow analysis",
            priority=InformationNeedPriority.CRITICAL
        )
        
        systems = self.matcher.select_ai_systems(gap)
        
        self.assertIn(AISystemType.FINANCIAL_ANALYSIS, systems)
        # Critical priority should include cross-reference
        self.assertIn(AISystemType.CROSS_REFERENCE, systems)


class TestLongGameStrategyPlanner(unittest.TestCase):
    """Test research strategy planning"""
    
    def setUp(self):
        self.planner = LongGameStrategyPlanner()
    
    def test_create_research_plan(self):
        """Test creation of research plan from gaps"""
        gaps = [
            KnowledgeGap(
                gap_id="g1",
                description="Gap 1",
                context="Test",
                priority=InformationNeedPriority.CRITICAL
            ),
            KnowledgeGap(
                gap_id="g2",
                description="Gap 2",
                context="Test",
                priority=InformationNeedPriority.LOW
            )
        ]
        
        tasks = self.planner.create_research_plan(gaps)
        
        self.assertEqual(len(tasks), 2)
        # Higher priority task should come first
        self.assertEqual(tasks[0].priority, InformationNeedPriority.CRITICAL)
    
    def test_get_next_executable_tasks(self):
        """Test getting tasks that can be executed"""
        # Create tasks with no dependencies
        task1 = ResearchTask(
            task_id="t1",
            objective="Task 1",
            ai_systems=[AISystemType.WEB_SEARCH],
            priority=InformationNeedPriority.HIGH
        )
        
        self.planner.research_tasks["t1"] = task1
        
        executable = self.planner.get_next_executable_tasks()
        
        self.assertEqual(len(executable), 1)
        self.assertEqual(executable[0].task_id, "t1")
    
    def test_update_task_status(self):
        """Test updating task status"""
        task = ResearchTask(
            task_id="t1",
            objective="Test",
            ai_systems=[AISystemType.WEB_SEARCH],
            priority=InformationNeedPriority.MEDIUM
        )
        
        self.planner.research_tasks["t1"] = task
        
        self.planner.update_task_status("t1", "completed", {"data": "found"})
        
        self.assertEqual(self.planner.research_tasks["t1"].status, "completed")
        self.assertIsNotNone(self.planner.research_tasks["t1"].completed_at)


class TestIncompleteDataHandler(unittest.TestCase):
    """Test handling of incomplete data"""
    
    def setUp(self):
        self.handler = IncompleteDataHandler()
    
    def test_assess_completeness_full(self):
        """Test completeness assessment of full data"""
        data = {
            'name': 'John',
            'type': 'person',
            'description': 'A person'
        }
        
        completeness = self.handler.assess_completeness(data)
        
        self.assertEqual(completeness, 1.0)
    
    def test_assess_completeness_partial(self):
        """Test completeness of partial data"""
        data = {
            'name': 'John',
            'type': '',  # Empty
            'description': 'A person'
        }
        
        completeness = self.handler.assess_completeness(data)
        
        self.assertLess(completeness, 1.0)
        self.assertGreater(completeness, 0.0)
    
    def test_generate_hypotheses(self):
        """Test hypothesis generation from partial data"""
        partial_data = {
            'name': 'Test',
            'connections': [{'to': 'Other'}]
            # Missing timeline
        }
        
        hypotheses = self.handler.generate_hypotheses(partial_data)
        
        self.assertGreater(len(hypotheses), 0)
        # Should generate hypothesis about missing timeline
        self.assertTrue(any('timeline' in h.statement.lower() for h in hypotheses))
    
    def test_infer_missing_data(self):
        """Test data inference from context"""
        partial_data = {
            'name': 'Test Corp'
            # Missing type
        }
        
        context = {
            'note': 'This company is involved...'
        }
        
        inferred = self.handler.infer_missing_data(partial_data, context)
        
        # Should infer organization type
        self.assertEqual(inferred.get('type'), 'organization')
        self.assertIn('_inferred', inferred)


class TestAIOrchestrator(unittest.TestCase):
    """Test the main AI orchestrator"""
    
    def setUp(self):
        self.orchestrator = AIOrchestrator(
            investigation_context="Test investigation"
        )
    
    def test_initialization(self):
        """Test orchestrator initialization"""
        self.assertIsNotNone(self.orchestrator.gap_analyzer)
        self.assertIsNotNone(self.orchestrator.strategy_planner)
        self.assertEqual(self.orchestrator.context, "Test investigation")
    
    def test_analyze_current_state(self):
        """Test analysis of investigation state"""
        data = {
            'entities': [
                {
                    'id': 'E1',
                    'name': 'Test'
                    # Missing other fields
                }
            ],
            'connections': []
        }
        
        analysis = self.orchestrator.analyze_current_state(data)
        
        self.assertIn('completeness', analysis)
        self.assertIn('gaps', analysis)
        self.assertIn('hypotheses', analysis)
        self.assertGreater(len(analysis['gaps']), 0)
    
    def test_create_research_strategy(self):
        """Test research strategy creation"""
        # First analyze to create gaps
        data = {
            'entities': [{'id': 'E1', 'name': 'Test'}],
            'connections': []
        }
        
        self.orchestrator.analyze_current_state(data)
        
        strategy = self.orchestrator.create_research_strategy(
            timeframe_days=30,
            max_parallel_tasks=3
        )
        
        self.assertIn('total_gaps', strategy)
        self.assertIn('total_tasks', strategy)
        self.assertIn('phases', strategy)
        self.assertGreater(strategy['total_tasks'], 0)
    
    def test_execute_autonomous_research(self):
        """Test autonomous research execution"""
        # Setup with some data
        data = {
            'entities': [{'id': 'E1', 'name': 'Test'}],
            'connections': []
        }
        
        self.orchestrator.analyze_current_state(data)
        self.orchestrator.create_research_strategy(timeframe_days=10)
        
        log = self.orchestrator.execute_autonomous_research(
            max_iterations=2,
            output_file="/tmp/test_research_log.json"
        )
        
        self.assertIn('started_at', log)
        self.assertIn('iterations', log)
        self.assertIn('status', log)
        self.assertGreater(len(log['iterations']), 0)
        
        # Check log file created
        self.assertTrue(os.path.exists("/tmp/test_research_log.json"))
    
    def test_generate_progress_report(self):
        """Test progress report generation"""
        # Create some tasks
        data = {'entities': [{'id': 'E1'}], 'connections': []}
        self.orchestrator.analyze_current_state(data)
        self.orchestrator.create_research_strategy()
        
        report = self.orchestrator.generate_progress_report()
        
        self.assertIn('total_gaps_identified', report)
        self.assertIn('total_research_tasks', report)
        self.assertIn('completion_percentage', report)


class TestDataModels(unittest.TestCase):
    """Test data models and serialization"""
    
    def test_knowledge_gap_to_dict(self):
        """Test KnowledgeGap serialization"""
        gap = KnowledgeGap(
            gap_id="test",
            description="Test gap",
            context="Test context",
            priority=InformationNeedPriority.HIGH,
            potential_sources=[AISystemType.WEB_SEARCH]
        )
        
        data = gap.to_dict()
        
        self.assertEqual(data['gap_id'], "test")
        self.assertEqual(data['priority'], "HIGH")
        self.assertIn('discovered_at', data)
    
    def test_research_task_to_dict(self):
        """Test ResearchTask serialization"""
        task = ResearchTask(
            task_id="t1",
            objective="Test objective",
            ai_systems=[AISystemType.WEB_SEARCH, AISystemType.NETWORK_ANALYSIS],
            priority=InformationNeedPriority.CRITICAL
        )
        
        data = task.to_dict()
        
        self.assertEqual(data['task_id'], "t1")
        self.assertEqual(data['status'], "pending")
        self.assertEqual(len(data['ai_systems']), 2)
    
    def test_research_hypothesis_to_dict(self):
        """Test ResearchHypothesis serialization"""
        hyp = ResearchHypothesis(
            hypothesis_id="h1",
            statement="Test hypothesis",
            confidence=0.75,
            supporting_evidence=["Evidence 1"]
        )
        
        data = hyp.to_dict()
        
        self.assertEqual(data['hypothesis_id'], "h1")
        self.assertEqual(data['confidence'], 0.75)
        self.assertTrue(data['requires_verification'])


class TestFullWorkflow(unittest.TestCase):
    """Test complete workflow from start to finish"""
    
    def test_complete_autonomous_workflow(self):
        """Test the complete autonomous research workflow"""
        # Initialize orchestrator
        orchestrator = AIOrchestrator(
            investigation_context="Complete workflow test"
        )
        
        # Step 1: Provide incomplete data
        incomplete_data = {
            'entities': [
                {'id': 'E1', 'name': 'Entity One'},
                {'id': 'E2', 'name': 'Entity Two', 'type': 'organization'}
            ],
            'connections': []
        }
        
        # Step 2: Analyze state
        analysis = orchestrator.analyze_current_state(incomplete_data)
        self.assertLess(analysis['completeness'], 1.0)
        self.assertGreater(len(analysis['gaps']), 0)
        
        # Step 3: Create strategy
        strategy = orchestrator.create_research_strategy(
            timeframe_days=14,
            max_parallel_tasks=2
        )
        self.assertGreater(strategy['total_tasks'], 0)
        
        # Step 4: Execute research
        log = orchestrator.execute_autonomous_research(
            max_iterations=3,
            output_file="/tmp/workflow_test_log.json"
        )
        self.assertIn('status', log)
        
        # Step 5: Check progress
        report = orchestrator.generate_progress_report()
        self.assertGreaterEqual(report['completion_percentage'], 0)
        
        print(f"\nWorkflow Test Results:")
        print(f"  - Initial completeness: {analysis['completeness']:.1%}")
        print(f"  - Gaps identified: {len(analysis['gaps'])}")
        print(f"  - Tasks created: {strategy['total_tasks']}")
        print(f"  - Completion: {report['completion_percentage']:.1f}%")


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
