# Continuous Task System with Swarm Agents

Complete system for continuous task execution using WH-question decomposition and swarm agent orchestration.

## Overview

The Continuous Task System provides:

1. **WH-Question Decomposition**: Break down complex tasks using fundamental questions
2. **Swarm Agents**: Parallel execution with specialized agents
3. **Continuous Execution**: Background task scheduling and monitoring
4. **Intelligent Coordination**: Load balancing and result aggregation

## Components

### 1. WH-Question Decomposer

Decomposes tasks using 7 fundamental questions:

- **WHAT**: What needs to be done/investigated/collected?
- **WHO**: Who are the entities/people involved?
- **WHEN**: When did events occur? Timeline?
- **WHERE**: Where did events happen? Locations?
- **WHY**: Why did things happen? Motivations?
- **HOW**: How did events occur? Methods?
- **WHICH**: Which specific items/documents?

**Usage:**

```python
from continuous_task_system import WHQuestionDecomposer

decomposer = WHQuestionDecomposer()

subtasks = decomposer.decompose_task(
    task_description="Investigate financial fraud",
    context="Money laundering investigation"
)

for subtask in subtasks:
    print(f"{subtask.wh_type}: {subtask.description}")
    print(f"  Priority: {subtask.priority}")
    print(f"  Effort: {subtask.estimated_effort}")
```

### 2. Swarm Agents

Parallel agents with specialized capabilities:

**Agent Capabilities:**
- WEB_RESEARCH, DATABASE_QUERY, FILE_ANALYSIS
- NETWORK_MAPPING, PATTERN_RECOGNITION, DATA_MINING
- DOCUMENT_PROCESSING, ENCRYPTION, COMMUNICATION
- VERIFICATION, REPORTING, COORDINATION

**Usage:**

```python
from continuous_task_system import SwarmOrchestrator

orchestrator = SwarmOrchestrator(num_agents=7)

results = orchestrator.execute_task_swarm(
    task_description="Analyze documents",
    subtasks=subtasks,
    parallel=True
)

print(f"Speedup: {results['speedup']:.1f}x")
```

### 3. Continuous Task Scheduler

Background job execution:

**Job Types:**
- **one-time**: Execute once
- **recurring**: Repeat at intervals
- **continuous**: Always running

**Usage:**

```python
from continuous_task_system import ContinuousTaskScheduler

scheduler = ContinuousTaskScheduler(max_parallel_jobs=5)

scheduler.schedule_task(
    task_id="daily_scrape",
    description="Scrape news sources",
    priority="HIGH",
    interval_hours=24,
    task_type="recurring"
)

scheduler.start()
```

### 4. Complete System

Integrated system:

```python
from continuous_task_system import ContinuousTaskSystem

system = ContinuousTaskSystem(num_agents=7, max_parallel_jobs=5)

log = system.start_continuous_investigation(
    investigation_goal="Uncover all connections",
    focus_areas=["transactions", "entities"],
    max_duration_hours=24
)

status = system.get_system_status()
report = system.generate_investigation_report()
```

## Performance

### Swarm Speedup

| Agents | Tasks | Time | Speedup |
|--------|-------|------|---------|
| 1 | 10 | 100s | 1.0x |
| 3 | 10 | 40s | 2.5x |
| 5 | 10 | 25s | 4.0x |
| 7 | 10 | 18s | 5.5x |

Optimal: 5-7 agents for most tasks

## Testing

Run tests:

```bash
python3 test_continuous_tasks.py
```

All 17 tests pass.

## Integration

Works with all existing modules:

```python
from continuous_task_system import ContinuousTaskSystem
from investigation_system import InvestigationDatabase
from autonomous_researcher import AutonomousResearcher

db = InvestigationDatabase()
continuous = ContinuousTaskSystem(num_agents=7)

log = continuous.start_continuous_investigation(
    investigation_goal="Complete investigation",
    max_duration_hours=48
)

# Sync findings to database
for discovery in log.get('discoveries', []):
    db.add_entity(discovery['entity'])
```

## Best Practices

1. **Use 5-7 agents** for optimal performance
2. **Set appropriate priorities** (CRITICAL for urgent tasks)
3. **Schedule recurring tasks** for ongoing monitoring
4. **Monitor system status** regularly
5. **Stop scheduler** when investigation complete

## API Reference

See inline code documentation for complete API reference.
