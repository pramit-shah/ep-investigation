#!/usr/bin/env python3
"""
Autonomous Investigation Cycle Runner
Wrapper to run autonomous systems with command-line arguments
"""

import sys
import argparse
import time
from datetime import datetime
from pathlib import Path


def run_autonomous_research(max_duration=50):
    """Run autonomous researcher"""
    print(f"Starting Autonomous Research (max {max_duration} minutes)...")
    
    try:
        from autonomous_researcher import AutonomousResearcher
        
        researcher = AutonomousResearcher()
        
        # Run research cycle
        start_time = time.time()
        max_seconds = max_duration * 60
        
        while (time.time() - start_time) < max_seconds:
            try:
                # Collect data from various sources
                researcher.collect_all_data()
                
                # Process and analyze
                researcher.process_collected_data()
                
                print(f"  ✓ Research cycle completed")
                break  # Exit after one successful cycle
                
            except Exception as e:
                print(f"  ⚠ Research error: {e}")
                # Continue despite errors
                break
        
        return True
        
    except ImportError:
        print("  ⚠ Autonomous researcher module not available")
        return False
    except Exception as e:
        print(f"  ✗ Research failed: {e}")
        return False


def run_ai_orchestration(duration=45):
    """Run AI orchestration"""
    print(f"Starting AI Orchestration (max {duration} minutes)...")
    
    try:
        from ai_orchestrator import AIOrchestrator
        
        orchestrator = AIOrchestrator()
        
        # Run orchestration cycle
        start_time = time.time()
        max_seconds = duration * 60
        
        try:
            # Discover knowledge gaps
            gaps = orchestrator.discover_knowledge_gaps()
            print(f"  Found {len(gaps)} knowledge gaps")
            
            # Plan research strategy
            strategy = orchestrator.plan_long_game_strategy(gaps)
            print(f"  Planned {len(strategy.get('tasks', []))} research tasks")
            
            # Execute high-priority tasks within time limit
            orchestrator.execute_strategy(strategy, max_duration=duration)
            
            print(f"  ✓ Orchestration cycle completed")
            return True
            
        except Exception as e:
            print(f"  ⚠ Orchestration error: {e}")
            return False
        
    except ImportError:
        print("  ⚠ AI orchestrator module not available")
        return False
    except Exception as e:
        print(f"  ✗ Orchestration failed: {e}")
        return False


def run_continuous_tasks(max_time=40):
    """Run continuous task system"""
    print(f"Starting Continuous Task System (max {max_time} minutes)...")
    
    try:
        from continuous_task_system import ContinuousTaskSystem
        
        system = ContinuousTaskSystem(num_agents=7, max_parallel_jobs=5)
        
        # Run investigation cycle
        try:
            log = system.start_continuous_investigation(
                investigation_goal="Uncover all connections and evidence",
                focus_areas=["transactions", "entities", "connections", "evidence"],
                max_duration_hours=max_time / 60.0
            )
            
            print(f"  ✓ Continuous tasks completed")
            print(f"  Tasks executed: {log.get('tasks_executed', 0)}")
            print(f"  Discoveries: {len(log.get('discoveries', []))}")
            
            return True
            
        except Exception as e:
            print(f"  ⚠ Task system error: {e}")
            return False
        
    except ImportError:
        print("  ⚠ Continuous task system module not available")
        return False
    except Exception as e:
        print(f"  ✗ Task system failed: {e}")
        return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Run autonomous investigation cycle'
    )
    parser.add_argument(
        '--research-duration',
        type=int,
        default=50,
        help='Max duration for research in minutes (default: 50)'
    )
    parser.add_argument(
        '--orchestration-duration',
        type=int,
        default=45,
        help='Max duration for orchestration in minutes (default: 45)'
    )
    parser.add_argument(
        '--tasks-duration',
        type=int,
        default=40,
        help='Max duration for tasks in minutes (default: 40)'
    )
    parser.add_argument(
        '--skip-research',
        action='store_true',
        help='Skip autonomous research'
    )
    parser.add_argument(
        '--skip-orchestration',
        action='store_true',
        help='Skip AI orchestration'
    )
    parser.add_argument(
        '--skip-tasks',
        action='store_true',
        help='Skip continuous tasks'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("Autonomous Investigation Cycle")
    print(f"Started: {datetime.utcnow().isoformat()} UTC")
    print("="*60)
    print()
    
    results = {
        'research': None,
        'orchestration': None,
        'tasks': None
    }
    
    # Run autonomous research
    if not args.skip_research:
        results['research'] = run_autonomous_research(args.research_duration)
        print()
    
    # Run AI orchestration
    if not args.skip_orchestration:
        results['orchestration'] = run_ai_orchestration(args.orchestration_duration)
        print()
    
    # Run continuous tasks
    if not args.skip_tasks:
        results['tasks'] = run_continuous_tasks(args.tasks_duration)
        print()
    
    # Summary
    print("="*60)
    print("Cycle Summary")
    print("="*60)
    print(f"Research: {results['research']}")
    print(f"Orchestration: {results['orchestration']}")
    print(f"Tasks: {results['tasks']}")
    print()
    
    # Save cycle log
    log_file = Path('data/cycle_log.json')
    try:
        import json
        
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'results': results,
            'duration': {
                'research': args.research_duration,
                'orchestration': args.orchestration_duration,
                'tasks': args.tasks_duration
            }
        }
        
        # Append to existing log
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_data)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"Cycle log saved to {log_file}")
    except Exception as e:
        print(f"Failed to save cycle log: {e}")
    
    # Exit with appropriate code
    if any(results.values()):
        print("\n✓ Cycle completed")
        sys.exit(0)
    else:
        print("\n⚠ Cycle completed with warnings")
        sys.exit(1)


if __name__ == "__main__":
    main()
