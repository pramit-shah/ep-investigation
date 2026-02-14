#!/usr/bin/env python3
"""
Tests for Continuous Task System with Swarm Agents

Tests all components:
- WH-Question Decomposer
- Swarm Agents
- Swarm Orchestrator
- Continuous Task Scheduler
- Complete Continuous Task System
"""

import unittest
import time
from continuous_task_system import (
    WHQuestionDecomposer, SwarmAgent, SwarmOrchestrator,
    ContinuousTaskScheduler, ContinuousTaskSystem,
    WHType, Priority, TaskStatus, AgentStatus, AgentCapability,
    WHSubtask, Task
)


class TestWHQuestionDecomposer(unittest.TestCase):
    """Test WH-Question Decomposer"""
    
    def setUp(self):
        self.decomposer = WHQuestionDecomposer()
    
    def test_initialization(self):
        """Test decomposer initialization"""
        self.assertEqual(len(self.decomposer.wh_types), 7)
        self.assertIn("what", self.decomposer.wh_types)
        self.assertIn("who", self.decomposer.wh_types)
    
    def test_decompose_task(self):
        """Test task decomposition"""
        subtasks = self.decomposer.decompose_task(
            "Investigate financial transactions",
            "Money laundering case"
        )
        self.assertEqual(len(subtasks), 7)  # One for each WH-type
        
        # Check all WH-types are covered
        wh_types = [st.wh_type for st in subtasks]
        self.assertIn("WHAT", wh_types)
        self.assertIn("WHO", wh_types)
        self.assertIn("WHEN", wh_types)
        self.assertIn("WHERE", wh_types)
        self.assertIn("WHY", wh_types)
        self.assertIn("HOW", wh_types)
        self.assertIn("WHICH", wh_types)
    
    def test_priority_assignment(self):
        """Test priority assignment"""
        subtasks = self.decomposer.decompose_task("Test task")
        
        # Check priorities are assigned
        priorities = [st.priority for st in subtasks]
        self.assertIn("HIGH", priorities)
        self.assertIn("MEDIUM", priorities)
        self.assertIn("LOW", priorities)
    
    def test_execution_order(self):
        """Test execution order generation"""
        subtasks = self.decomposer.decompose_task("Test task")
        execution_order = self.decomposer.get_execution_order(subtasks)
        
        # Should have multiple levels
        self.assertGreater(len(execution_order), 0)
        self.assertLess(len(execution_order), 5)


class TestSwarmAgent(unittest.TestCase):
    """Test individual Swarm Agent"""
    
    def setUp(self):
        self.agent = SwarmAgent(
            "test_agent",
            [AgentCapability.WEB_RESEARCH.value, AgentCapability.DATA_MINING.value]
        )
    
    def test_initialization(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.agent_id, "test_agent")
        self.assertEqual(len(self.agent.capabilities), 2)
        self.assertEqual(self.agent.status, AgentStatus.IDLE)
    
    def test_can_handle(self):
        """Test capability checking"""
        self.assertTrue(self.agent.can_handle([AgentCapability.WEB_RESEARCH.value]))
        self.assertTrue(self.agent.can_handle([]))
        self.assertFalse(self.agent.can_handle([AgentCapability.ENCRYPTION.value]))
    
    def test_execute_task(self):
        """Test task execution"""
        task = Task(
            task_id="test_task",
            description="Test task",
            priority="HIGH"
        )
        
        result = self.agent.execute_task(task)
        
        self.assertEqual(result['status'], 'success')
        self.assertIn("test_agent", result['agent_id'])
        self.assertEqual(task.status, TaskStatus.COMPLETED.value)
        self.assertEqual(len(self.agent.completed_tasks), 1)


class TestSwarmOrchestrator(unittest.TestCase):
    """Test Swarm Orchestrator"""
    
    def setUp(self):
        self.orchestrator = SwarmOrchestrator(num_agents=5)
    
    def test_initialization(self):
        """Test orchestrator initialization"""
        self.assertEqual(len(self.orchestrator.agents), 5)
        for agent in self.orchestrator.agents:
            self.assertIsInstance(agent, SwarmAgent)
    
    def test_execute_task_swarm(self):
        """Test swarm task execution"""
        decomposer = WHQuestionDecomposer()
        subtasks = decomposer.decompose_task("Test investigation")
        
        results = self.orchestrator.execute_task_swarm(
            "Test investigation",
            subtasks,
            parallel=True
        )
        
        self.assertEqual(results['total_tasks'], len(subtasks))
        self.assertGreater(results['tasks_completed'], 0)
        self.assertGreater(results['speedup'], 1.0)  # Should be faster with parallel
    
    def test_swarm_status(self):
        """Test swarm status"""
        status = self.orchestrator.get_swarm_status()
        
        self.assertEqual(status['total_agents'], 5)
        self.assertIn('idle_agents', status)
        self.assertIn('agents', status)


class TestContinuousTaskScheduler(unittest.TestCase):
    """Test Continuous Task Scheduler"""
    
    def setUp(self):
        self.scheduler = ContinuousTaskScheduler(max_parallel_jobs=3)
    
    def test_initialization(self):
        """Test scheduler initialization"""
        self.assertEqual(self.scheduler.max_parallel_jobs, 3)
        self.assertFalse(self.scheduler.is_running)
    
    def test_schedule_task(self):
        """Test task scheduling"""
        task = self.scheduler.schedule_task(
            task_id="test_task",
            description="Test task",
            priority="HIGH",
            task_type="one-time"
        )
        
        self.assertEqual(task.task_id, "test_task")
        self.assertEqual(task.priority, "HIGH")
        self.assertIn("test_task", self.scheduler.scheduled_tasks)
    
    def test_scheduler_status(self):
        """Test scheduler status"""
        self.scheduler.schedule_task("task1", "Task 1")
        self.scheduler.schedule_task("task2", "Task 2")
        
        status = self.scheduler.get_scheduler_status()
        
        self.assertIn('scheduled_tasks', status)
        self.assertIn('running_tasks', status)
        self.assertIn('completed_tasks', status)


class TestContinuousTaskSystem(unittest.TestCase):
    """Test Complete Continuous Task System"""
    
    def setUp(self):
        self.system = ContinuousTaskSystem(num_agents=7, max_parallel_jobs=5)
    
    def test_initialization(self):
        """Test system initialization"""
        self.assertIsNotNone(self.system.decomposer)
        self.assertIsNotNone(self.system.orchestrator)
        self.assertIsNotNone(self.system.scheduler)
    
    def test_start_continuous_investigation(self):
        """Test starting continuous investigation"""
        log = self.system.start_continuous_investigation(
            investigation_goal="Test investigation",
            focus_areas=["area1", "area2"],
            max_duration_hours=24
        )
        
        self.assertIn('investigation_goal', log)
        self.assertIn('subtasks_generated', log)
        self.assertIn('swarm_results', log)
        self.assertGreater(log['subtasks_generated'], 0)
        
        # Cleanup
        self.system.stop_all()
    
    def test_system_status(self):
        """Test system status"""
        status = self.system.get_system_status()
        
        self.assertIn('decomposer', status)
        self.assertIn('orchestrator', status)
        self.assertIn('scheduler', status)
        self.assertIn('total_agents', status)
    
    def test_generate_report(self):
        """Test report generation"""
        self.system.start_continuous_investigation("Test")
        time.sleep(0.5)
        
        report = self.system.generate_investigation_report()
        
        self.assertIn('total_investigations', report)
        self.assertIn('investigation_logs', report)
        
        # Cleanup
        self.system.stop_all()


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWHQuestionDecomposer))
    suite.addTests(loader.loadTestsFromTestCase(TestSwarmAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestSwarmOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestContinuousTaskScheduler))
    suite.addTests(loader.loadTestsFromTestCase(TestContinuousTaskSystem))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 80)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
