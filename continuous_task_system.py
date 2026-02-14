#!/usr/bin/env python3
"""
Continuous Task System with Swarm Agents and WH-Question Decomposition

This module provides a comprehensive system for:
1. Decomposing complex tasks using WH-questions (What, Who, When, Where, Why, How, Which)
2. Distributing work to swarms of parallel agents for faster completion
3. Executing tasks continuously in background
4. Coordinating agent activities and monitoring progress

Author: Investigation Team
License: MIT
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field, asdict
import queue
import hashlib


class WHType(Enum):
    """Types of WH-questions for task decomposition"""
    WHAT = "what"      # What needs to be done/investigated?
    WHO = "who"        # Who is involved/affected?
    WHEN = "when"      # When did it happen/should it be done?
    WHERE = "where"    # Where did it happen/should it be done?
    WHY = "why"        # Why did it happen/is it important?
    HOW = "how"        # How did it happen/should it be done?
    WHICH = "which"    # Which specific items/people/places?


class Priority(Enum):
    """Task priority levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    EXPLORATORY = 1


class TaskStatus(Enum):
    """Status of a task"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentStatus(Enum):
    """Status of an agent"""
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentCapability(Enum):
    """Agent capabilities"""
    WEB_RESEARCH = "web_research"
    DATABASE_QUERY = "database_query"
    FILE_ANALYSIS = "file_analysis"
    NETWORK_MAPPING = "network_mapping"
    PATTERN_RECOGNITION = "pattern_recognition"
    DATA_MINING = "data_mining"
    DOCUMENT_PROCESSING = "document_processing"
    ENCRYPTION = "encryption"
    COMMUNICATION = "communication"
    VERIFICATION = "verification"
    REPORTING = "reporting"
    COORDINATION = "coordination"


@dataclass
class WHSubtask:
    """Represents a subtask generated from WH-question decomposition"""
    wh_type: str
    description: str
    priority: str = "MEDIUM"
    estimated_effort: str = "medium"  # low, medium, high
    dependencies: List[str] = field(default_factory=list)
    required_capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class Task:
    """Represents a task to be executed"""
    task_id: str
    description: str
    priority: str = "MEDIUM"
    status: str = "PENDING"
    assigned_agent: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class WHQuestionDecomposer:
    """
    Decomposes complex investigation tasks into subtasks based on WH-questions.
    
    Uses the fundamental questions: What, Who, When, Where, Why, How, Which
    to break down a complex task into actionable subtasks.
    """
    
    def __init__(self):
        self.wh_types = [wh.value for wh in WHType]
        self.question_templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize question templates for each WH-type"""
        return {
            "what": {
                "keywords": ["investigate", "collect", "analyze", "identify", "document"],
                "focus": "actions, objects, items, events",
                "capabilities": [AgentCapability.DATA_MINING.value, AgentCapability.FILE_ANALYSIS.value]
            },
            "who": {
                "keywords": ["identify", "track", "map", "profile", "investigate"],
                "focus": "people, entities, organizations, groups",
                "capabilities": [AgentCapability.DATABASE_QUERY.value, AgentCapability.WEB_RESEARCH.value]
            },
            "when": {
                "keywords": ["timeline", "sequence", "date", "time", "chronology"],
                "focus": "time, dates, sequences, duration",
                "capabilities": [AgentCapability.PATTERN_RECOGNITION.value, AgentCapability.DATA_MINING.value]
            },
            "where": {
                "keywords": ["location", "place", "region", "geography", "map"],
                "focus": "locations, places, addresses, regions",
                "capabilities": [AgentCapability.NETWORK_MAPPING.value, AgentCapability.WEB_RESEARCH.value]
            },
            "why": {
                "keywords": ["motive", "reason", "cause", "purpose", "intent"],
                "focus": "motivations, reasons, causes, purposes",
                "capabilities": [AgentCapability.PATTERN_RECOGNITION.value, AgentCapability.VERIFICATION.value]
            },
            "how": {
                "keywords": ["method", "process", "mechanism", "technique", "approach"],
                "focus": "methods, processes, techniques, mechanisms",
                "capabilities": [AgentCapability.FILE_ANALYSIS.value, AgentCapability.PATTERN_RECOGNITION.value]
            },
            "which": {
                "keywords": ["specific", "particular", "exact", "individual", "distinct"],
                "focus": "specific items, documents, connections, details",
                "capabilities": [AgentCapability.DATABASE_QUERY.value, AgentCapability.VERIFICATION.value]
            }
        }
    
    def decompose_task(self, task_description: str, context: str = "") -> List[WHSubtask]:
        """
        Decompose a complex task into WH-question based subtasks.
        
        Args:
            task_description: The main task to decompose
            context: Additional context for the task
            
        Returns:
            List of WHSubtask objects, one for each WH-question type
        """
        subtasks = []
        
        for wh_type in self.wh_types:
            template = self.question_templates[wh_type]
            
            # Generate subtask description
            subtask_desc = self._generate_subtask_description(
                wh_type, task_description, template, context
            )
            
            # Determine priority based on WH-type importance
            priority = self._determine_priority(wh_type, task_description)
            
            # Estimate effort
            effort = self._estimate_effort(wh_type, task_description)
            
            # Create subtask
            subtask = WHSubtask(
                wh_type=wh_type.upper(),
                description=subtask_desc,
                priority=priority,
                estimated_effort=effort,
                required_capabilities=template['capabilities'],
                metadata={
                    "keywords": template['keywords'],
                    "focus": template['focus'],
                    "context": context
                }
            )
            
            subtasks.append(subtask)
        
        # Add dependencies
        subtasks = self._add_dependencies(subtasks)
        
        return subtasks
    
    def _generate_subtask_description(self, wh_type: str, task: str, 
                                     template: Dict, context: str) -> str:
        """Generate description for a WH-subtask"""
        focus = template['focus']
        
        descriptions = {
            "what": f"What needs to be investigated, collected, or analyzed in: {task}?",
            "who": f"Who are the people, entities, or organizations involved in: {task}?",
            "when": f"When did events occur? What is the timeline for: {task}?",
            "where": f"Where did events take place? What locations are relevant to: {task}?",
            "why": f"Why did things happen? What are the motivations behind: {task}?",
            "how": f"How did events occur? What methods or mechanisms were used in: {task}?",
            "which": f"Which specific items, documents, or connections are relevant to: {task}?"
        }
        
        return descriptions.get(wh_type, f"{wh_type.upper()}: {task}")
    
    def _determine_priority(self, wh_type: str, task: str) -> str:
        """Determine priority for a WH-subtask"""
        # WHAT, WHO, WHEN are typically highest priority
        high_priority = ["what", "who", "when"]
        medium_priority = ["where", "how"]
        low_priority = ["why", "which"]
        
        if wh_type in high_priority:
            return "HIGH"
        elif wh_type in medium_priority:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _estimate_effort(self, wh_type: str, task: str) -> str:
        """Estimate effort required for a WH-subtask"""
        # Simple heuristic based on WH-type
        high_effort = ["what", "how", "why"]
        medium_effort = ["who", "where"]
        low_effort = ["when", "which"]
        
        if wh_type in high_effort:
            return "high"
        elif wh_type in medium_effort:
            return "medium"
        else:
            return "low"
    
    def _add_dependencies(self, subtasks: List[WHSubtask]) -> List[WHSubtask]:
        """Add dependencies between subtasks"""
        # WHO and WHAT should be done first
        # WHEN depends on WHO and WHAT
        # WHERE depends on WHO and WHAT
        # HOW and WHY depend on WHAT, WHO, WHEN, WHERE
        # WHICH can run in parallel with others
        
        dependency_map = {
            "WHEN": ["WHAT", "WHO"],
            "WHERE": ["WHAT", "WHO"],
            "HOW": ["WHAT", "WHO", "WHEN", "WHERE"],
            "WHY": ["WHAT", "WHO", "WHEN", "WHERE"],
            "WHICH": ["WHAT"]
        }
        
        for subtask in subtasks:
            if subtask.wh_type in dependency_map:
                subtask.dependencies = dependency_map[subtask.wh_type]
        
        return subtasks
    
    def get_execution_order(self, subtasks: List[WHSubtask]) -> List[List[WHSubtask]]:
        """
        Get execution order for subtasks based on dependencies.
        Returns list of lists, where each inner list can be executed in parallel.
        """
        # Build dependency graph
        tasks_by_type = {task.wh_type: task for task in subtasks}
        
        # Level 0: No dependencies (WHAT, WHO, WHICH)
        level0 = [t for t in subtasks if not t.dependencies]
        
        # Level 1: Depend only on level 0 (WHEN, WHERE)
        level1 = [t for t in subtasks if t.dependencies and 
                 all(d in [x.wh_type for x in level0] for d in t.dependencies)]
        
        # Level 2: Everything else (HOW, WHY)
        level2 = [t for t in subtasks if t not in level0 and t not in level1]
        
        return [level0, level1, level2]


class SwarmAgent:
    """
    Represents an individual agent in the swarm.
    Each agent has specific capabilities and can execute tasks.
    """
    
    def __init__(self, agent_id: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.current_task: Optional[Task] = None
        self.completed_tasks: List[str] = []
        self.failed_tasks: List[str] = []
        self.total_execution_time = 0.0
    
    def can_handle(self, required_capabilities: List[str]) -> bool:
        """Check if agent can handle tasks requiring specific capabilities"""
        if not required_capabilities:
            return True
        return any(cap in self.capabilities for cap in required_capabilities)
    
    def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task (simulated)"""
        self.status = AgentStatus.WORKING
        self.current_task = task
        task.status = TaskStatus.RUNNING.value
        task.assigned_agent = self.agent_id
        task.start_time = time.time()
        
        try:
            # Simulate task execution
            # In real implementation, this would call actual task logic
            execution_time = self._simulate_execution()
            
            result = {
                "status": "success",
                "agent_id": self.agent_id,
                "execution_time": execution_time,
                "findings": f"Completed: {task.description}",
                "timestamp": datetime.now().isoformat()
            }
            
            task.result = result
            task.status = TaskStatus.COMPLETED.value
            task.end_time = time.time()
            
            self.completed_tasks.append(task.task_id)
            self.total_execution_time += execution_time
            self.status = AgentStatus.COMPLETED
            
            return result
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED.value
            task.end_time = time.time()
            self.failed_tasks.append(task.task_id)
            self.status = AgentStatus.FAILED
            raise
        finally:
            self.current_task = None
            self.status = AgentStatus.IDLE
    
    def _simulate_execution(self) -> float:
        """Simulate task execution with random time"""
        # Simulate work (0.1-0.5 seconds)
        import random
        execution_time = random.uniform(0.1, 0.5)
        time.sleep(execution_time)
        return execution_time
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_id": self.agent_id,
            "status": self.status.value,
            "capabilities": self.capabilities,
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "total_execution_time": self.total_execution_time,
            "current_task": self.current_task.task_id if self.current_task else None
        }


class SwarmOrchestrator:
    """
    Orchestrates a swarm of agents to execute tasks in parallel.
    Handles task distribution, load balancing, and result aggregation.
    """
    
    def __init__(self, num_agents: int = 5):
        self.num_agents = num_agents
        self.agents: List[SwarmAgent] = []
        self.task_queue: queue.Queue = queue.Queue()
        self.results: List[Dict[str, Any]] = []
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize swarm agents with diverse capabilities"""
        capability_sets = [
            [AgentCapability.WEB_RESEARCH.value, AgentCapability.DATA_MINING.value],
            [AgentCapability.DATABASE_QUERY.value, AgentCapability.VERIFICATION.value],
            [AgentCapability.FILE_ANALYSIS.value, AgentCapability.DOCUMENT_PROCESSING.value],
            [AgentCapability.NETWORK_MAPPING.value, AgentCapability.PATTERN_RECOGNITION.value],
            [AgentCapability.ENCRYPTION.value, AgentCapability.COMMUNICATION.value],
            [AgentCapability.REPORTING.value, AgentCapability.COORDINATION.value],
            [AgentCapability.WEB_RESEARCH.value, AgentCapability.PATTERN_RECOGNITION.value],
            [AgentCapability.DATA_MINING.value, AgentCapability.VERIFICATION.value],
            [AgentCapability.FILE_ANALYSIS.value, AgentCapability.NETWORK_MAPPING.value],
            [AgentCapability.DATABASE_QUERY.value, AgentCapability.REPORTING.value],
        ]
        
        for i in range(self.num_agents):
            capabilities = capability_sets[i % len(capability_sets)]
            agent = SwarmAgent(f"agent_{i+1}", capabilities)
            self.agents.append(agent)
    
    def execute_task_swarm(self, task_description: str, 
                          subtasks: List[WHSubtask],
                          parallel: bool = True) -> Dict[str, Any]:
        """
        Execute tasks using the swarm of agents.
        
        Args:
            task_description: Main task description
            subtasks: List of subtasks to execute
            parallel: Whether to execute in parallel
            
        Returns:
            Execution results and metrics
        """
        start_time = time.time()
        self.results = []
        
        # Convert WHSubtasks to Tasks
        tasks = []
        for i, subtask in enumerate(subtasks):
            task = Task(
                task_id=f"task_{i+1}",
                description=subtask.description,
                priority=subtask.priority,
                metadata={
                    "wh_type": subtask.wh_type,
                    "required_capabilities": subtask.required_capabilities
                }
            )
            tasks.append(task)
        
        if parallel:
            self._execute_parallel(tasks)
        else:
            self._execute_sequential(tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculate speedup (assuming single-threaded would take sum of all task times)
        single_threaded_time = sum(r.get('execution_time', 0) for r in self.results)
        speedup = single_threaded_time / total_time if total_time > 0 else 1.0
        
        return {
            "task_description": task_description,
            "total_tasks": len(tasks),
            "tasks_completed": len([r for r in self.results if r.get('status') == 'success']),
            "tasks_failed": len([r for r in self.results if r.get('status') != 'success']),
            "total_time": total_time,
            "single_threaded_time": single_threaded_time,
            "speedup": speedup,
            "results": self.results,
            "agent_utilization": self._calculate_utilization()
        }
    
    def _execute_parallel(self, tasks: List[Task]):
        """Execute tasks in parallel using threading"""
        threads = []
        
        # Distribute tasks to agents
        for i, task in enumerate(tasks):
            agent = self._select_agent(task)
            
            if agent:
                thread = threading.Thread(
                    target=self._execute_task_thread,
                    args=(agent, task)
                )
                threads.append(thread)
                thread.start()
            else:
                # No suitable agent, execute sequentially
                idle_agent = self._get_idle_agent()
                if idle_agent:
                    result = idle_agent.execute_task(task)
                    self.results.append(result)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
    
    def _execute_sequential(self, tasks: List[Task]):
        """Execute tasks sequentially"""
        for task in tasks:
            agent = self._select_agent(task)
            if agent:
                result = agent.execute_task(task)
                self.results.append(result)
    
    def _execute_task_thread(self, agent: SwarmAgent, task: Task):
        """Execute task in a thread"""
        try:
            result = agent.execute_task(task)
            self.results.append(result)
        except Exception as e:
            self.results.append({
                "status": "failed",
                "error": str(e),
                "task_id": task.task_id
            })
    
    def _select_agent(self, task: Task) -> Optional[SwarmAgent]:
        """Select best agent for a task based on capabilities and availability"""
        required_caps = task.metadata.get('required_capabilities', [])
        
        # Find idle agents that can handle the task
        capable_agents = [
            agent for agent in self.agents
            if agent.status == AgentStatus.IDLE and agent.can_handle(required_caps)
        ]
        
        if not capable_agents:
            # Wait for an agent to become idle
            return self._get_idle_agent()
        
        # Select agent with least completed tasks (load balancing)
        return min(capable_agents, key=lambda a: len(a.completed_tasks))
    
    def _get_idle_agent(self) -> Optional[SwarmAgent]:
        """Get first idle agent"""
        for agent in self.agents:
            if agent.status == AgentStatus.IDLE:
                return agent
        return None
    
    def _calculate_utilization(self) -> Dict[str, float]:
        """Calculate agent utilization metrics"""
        total_tasks = sum(len(a.completed_tasks) + len(a.failed_tasks) for a in self.agents)
        
        if total_tasks == 0:
            return {"average_utilization": 0.0, "agents": []}
        
        utilizations = []
        for agent in self.agents:
            agent_tasks = len(agent.completed_tasks) + len(agent.failed_tasks)
            utilization = agent_tasks / total_tasks if total_tasks > 0 else 0
            utilizations.append({
                "agent_id": agent.agent_id,
                "utilization": utilization,
                "tasks": agent_tasks
            })
        
        avg_utilization = sum(u['utilization'] for u in utilizations) / len(utilizations)
        
        return {
            "average_utilization": avg_utilization,
            "agents": utilizations
        }
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """Get status of entire swarm"""
        return {
            "total_agents": len(self.agents),
            "idle_agents": len([a for a in self.agents if a.status == AgentStatus.IDLE]),
            "working_agents": len([a for a in self.agents if a.status == AgentStatus.WORKING]),
            "total_completed": sum(len(a.completed_tasks) for a in self.agents),
            "total_failed": sum(len(a.failed_tasks) for a in self.agents),
            "agents": [a.get_status() for a in self.agents]
        }


class ContinuousTaskScheduler:
    """
    Schedules and executes tasks continuously in background.
    Supports one-time, recurring, and continuous tasks.
    """
    
    def __init__(self, max_parallel_jobs: int = 5):
        self.max_parallel_jobs = max_parallel_jobs
        self.task_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.scheduled_tasks: Dict[str, Task] = {}
        self.running_tasks: Dict[str, Task] = {}
        self.completed_tasks: List[Task] = []
        self.is_running = False
        self.scheduler_thread: Optional[threading.Thread] = None
    
    def schedule_task(self, task_id: str, description: str,
                     priority: str = "MEDIUM",
                     interval_hours: Optional[float] = None,
                     task_type: str = "one-time") -> Task:
        """
        Schedule a task for execution.
        
        Args:
            task_id: Unique task identifier
            description: Task description
            priority: Task priority (CRITICAL, HIGH, MEDIUM, LOW, EXPLORATORY)
            interval_hours: For recurring tasks, interval in hours
            task_type: one-time, recurring, or continuous
            
        Returns:
            Task object
        """
        priority_value = Priority[priority].value if priority in Priority.__members__ else 3
        
        task = Task(
            task_id=task_id,
            description=description,
            priority=priority,
            metadata={
                "task_type": task_type,
                "interval_hours": interval_hours,
                "scheduled_time": datetime.now().isoformat()
            }
        )
        
        self.scheduled_tasks[task_id] = task
        
        # Add to priority queue (lower number = higher priority)
        self.task_queue.put((6 - priority_value, task_id))
        
        return task
    
    def start(self):
        """Start the continuous task scheduler"""
        if self.is_running:
            return
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
    
    def stop(self):
        """Stop the continuous task scheduler"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.is_running:
            # Check if we can run more tasks
            if len(self.running_tasks) < self.max_parallel_jobs:
                try:
                    # Get highest priority task
                    priority, task_id = self.task_queue.get(timeout=1)
                    
                    if task_id in self.scheduled_tasks:
                        task = self.scheduled_tasks[task_id]
                        
                        # Execute task in background thread
                        thread = threading.Thread(
                            target=self._execute_task_background,
                            args=(task,)
                        )
                        thread.daemon = True
                        thread.start()
                    
                except queue.Empty:
                    pass
            
            time.sleep(0.1)
    
    def _execute_task_background(self, task: Task):
        """Execute task in background"""
        task.status = TaskStatus.RUNNING.value
        task.start_time = time.time()
        self.running_tasks[task.task_id] = task
        
        try:
            # Simulate task execution
            result = self._execute_task(task)
            task.result = result
            task.status = TaskStatus.COMPLETED.value
            
            # Handle recurring tasks
            if task.metadata.get('task_type') == 'recurring':
                self._reschedule_recurring(task)
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED.value
        finally:
            task.end_time = time.time()
            self.running_tasks.pop(task.task_id, None)
            self.completed_tasks.append(task)
            self.scheduled_tasks.pop(task.task_id, None)
    
    def _execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task (simulated)"""
        # Simulate work
        time.sleep(0.5)
        
        return {
            "status": "success",
            "message": f"Completed: {task.description}",
            "timestamp": datetime.now().isoformat()
        }
    
    def _reschedule_recurring(self, task: Task):
        """Reschedule a recurring task"""
        interval_hours = task.metadata.get('interval_hours', 24)
        
        # Create new task with same parameters
        new_task_id = f"{task.task_id}_{int(time.time())}"
        self.schedule_task(
            task_id=new_task_id,
            description=task.description,
            priority=task.priority,
            interval_hours=interval_hours,
            task_type='recurring'
        )
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a scheduled task"""
        if task_id in self.scheduled_tasks:
            task = self.scheduled_tasks.pop(task_id)
            task.status = TaskStatus.CANCELLED.value
            return True
        return False
    
    def get_scheduler_status(self) -> Dict[str, Any]:
        """Get scheduler status"""
        return {
            "is_running": self.is_running,
            "queued_tasks": self.task_queue.qsize(),
            "scheduled_tasks": len(self.scheduled_tasks),
            "running_tasks": len(self.running_tasks),
            "completed_tasks": len(self.completed_tasks),
            "max_parallel_jobs": self.max_parallel_jobs,
            "active_tasks": [t.to_dict() for t in self.running_tasks.values()]
        }


class ContinuousTaskSystem:
    """
    Complete continuous task system integrating WH-decomposition, 
    swarm agents, and continuous scheduling.
    """
    
    def __init__(self, num_agents: int = 5, max_parallel_jobs: int = 5):
        self.decomposer = WHQuestionDecomposer()
        self.orchestrator = SwarmOrchestrator(num_agents=num_agents)
        self.scheduler = ContinuousTaskScheduler(max_parallel_jobs=max_parallel_jobs)
        self.investigation_logs: List[Dict[str, Any]] = []
    
    def start_continuous_investigation(self, investigation_goal: str,
                                      focus_areas: Optional[List[str]] = None,
                                      max_duration_hours: float = 24) -> Dict[str, Any]:
        """
        Start a continuous investigation that runs in background.
        
        Args:
            investigation_goal: Main investigation goal
            focus_areas: Specific areas to focus on
            max_duration_hours: Maximum duration for investigation
            
        Returns:
            Investigation execution log
        """
        start_time = time.time()
        
        # Step 1: Decompose investigation into WH-questions
        subtasks = self.decomposer.decompose_task(
            task_description=investigation_goal,
            context=f"Focus areas: {focus_areas}" if focus_areas else ""
        )
        
        # Step 2: Execute tasks using swarm
        swarm_results = self.orchestrator.execute_task_swarm(
            task_description=investigation_goal,
            subtasks=subtasks,
            parallel=True
        )
        
        # Step 3: Schedule continuous monitoring tasks
        self.scheduler.start()
        
        for i, subtask in enumerate(subtasks):
            self.scheduler.schedule_task(
                task_id=f"continuous_{i+1}",
                description=subtask.description,
                priority=subtask.priority,
                interval_hours=1.0,  # Check every hour
                task_type="recurring"
            )
        
        end_time = time.time()
        
        log_entry = {
            "investigation_goal": investigation_goal,
            "focus_areas": focus_areas,
            "start_time": datetime.fromtimestamp(start_time).isoformat(),
            "end_time": datetime.fromtimestamp(end_time).isoformat(),
            "duration_seconds": end_time - start_time,
            "subtasks_generated": len(subtasks),
            "swarm_results": swarm_results,
            "scheduler_started": self.scheduler.is_running,
            "continuous_tasks_scheduled": len(subtasks)
        }
        
        self.investigation_logs.append(log_entry)
        
        return log_entry
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        return {
            "decomposer": {
                "wh_types": len(self.decomposer.wh_types)
            },
            "orchestrator": self.orchestrator.get_swarm_status(),
            "scheduler": self.scheduler.get_scheduler_status(),
            "investigation_logs": len(self.investigation_logs),
            "total_agents": len(self.orchestrator.agents),
            "active_agents": len([a for a in self.orchestrator.agents 
                                 if a.status != AgentStatus.IDLE]),
            "active_jobs": self.scheduler.get_scheduler_status()['running_tasks'],
            "completed_tasks": self.scheduler.get_scheduler_status()['completed_tasks'],
            "investigation_complete": not self.scheduler.is_running
        }
    
    def generate_investigation_report(self) -> Dict[str, Any]:
        """Generate comprehensive investigation report"""
        swarm_status = self.orchestrator.get_swarm_status()
        scheduler_status = self.scheduler.get_scheduler_status()
        
        return {
            "report_generated": datetime.now().isoformat(),
            "total_investigations": len(self.investigation_logs),
            "total_agents": swarm_status['total_agents'],
            "total_completed_tasks": swarm_status['total_completed'],
            "total_failed_tasks": swarm_status['total_failed'],
            "continuous_tasks_completed": scheduler_status['completed_tasks'],
            "investigation_logs": self.investigation_logs,
            "swarm_performance": self.orchestrator._calculate_utilization(),
            "scheduler_metrics": scheduler_status
        }
    
    def stop_all(self):
        """Stop all continuous operations"""
        self.scheduler.stop()


def main():
    """Demo of continuous task system"""
    print("=" * 80)
    print("Continuous Task System with Swarm Agents - Demo")
    print("=" * 80)
    
    # Initialize system
    system = ContinuousTaskSystem(num_agents=7, max_parallel_jobs=5)
    
    # Start continuous investigation
    print("\n1. Starting continuous investigation...")
    log = system.start_continuous_investigation(
        investigation_goal="Investigate offshore financial transactions and connections",
        focus_areas=["transactions", "entities", "locations"],
        max_duration_hours=24
    )
    
    print(f"   ✓ Investigation started")
    print(f"   ✓ Subtasks generated: {log['subtasks_generated']}")
    print(f"   ✓ Swarm execution time: {log['swarm_results']['total_time']:.2f}s")
    print(f"   ✓ Speedup: {log['swarm_results']['speedup']:.1f}x")
    print(f"   ✓ Continuous tasks scheduled: {log['continuous_tasks_scheduled']}")
    
    # Monitor for a bit
    print("\n2. Monitoring system status...")
    time.sleep(2)
    
    status = system.get_system_status()
    print(f"   ✓ Total agents: {status['total_agents']}")
    print(f"   ✓ Active agents: {status['active_agents']}")
    print(f"   ✓ Active jobs: {status['active_jobs']}")
    print(f"   ✓ Completed tasks: {status['completed_tasks']}")
    
    # Generate report
    print("\n3. Generating investigation report...")
    report = system.generate_investigation_report()
    print(f"   ✓ Total investigations: {report['total_investigations']}")
    print(f"   ✓ Total completed tasks: {report['total_completed_tasks']}")
    print(f"   ✓ Continuous tasks: {report['continuous_tasks_completed']}")
    
    # Stop
    print("\n4. Stopping continuous tasks...")
    system.stop_all()
    print("   ✓ All tasks stopped")
    
    print("\n" + "=" * 80)
    print("Demo complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
