#!/usr/bin/env python3
"""
Workflow Deployment Bootstrap
Generates and installs GitHub Actions workflows
Run this to set up continuous investigation on GitHub Actions
"""

import os
import sys
from pathlib import Path


CONTINUOUS_INVESTIGATION_WORKFLOW = """name: Continuous Investigation System

on:
  schedule:
    # Run every 6 hours
    - cron: '0 */6 * * *'
  workflow_dispatch:  # Allow manual triggering
  push:
    branches:
      - main
      - copilot/investigate-epstein-connections

permissions:
  contents: write
  issues: write

jobs:
  autonomous-research:
    runs-on: ubuntu-latest
    timeout-minutes: 55  # GitHub Actions has 60 min limit for free tier
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Configure Git
        run: |
          git config --global user.name "Investigation Bot"
          git config --global user.email "investigation-bot@users.noreply.github.com"
      
      - name: Initialize Investigation System
        run: |
          python3 setup.py
          echo "✓ Investigation system initialized"
      
      - name: Run Error Recovery Check
        id: recovery
        continue-on-error: true
        run: |
          echo "Running pre-flight error recovery..."
          python3 autonomous_error_recovery.py
          echo "recovery_status=$?" >> $GITHUB_OUTPUT
      
      - name: Run Autonomous Investigation Cycle
        id: investigation
        continue-on-error: true
        run: |
          echo "Starting autonomous investigation cycle..."
          python3 run_autonomous_cycle.py \\
            --research-duration 15 \\
            --orchestration-duration 15 \\
            --tasks-duration 15
          echo "investigation_status=$?" >> $GITHUB_OUTPUT
      
      - name: Check for Updates
        id: check_updates
        run: |
          git add -A
          if git diff --staged --quiet; then
            echo "has_updates=false" >> $GITHUB_OUTPUT
            echo "No new findings to commit"
          else
            echo "has_updates=true" >> $GITHUB_OUTPUT
            echo "New findings detected"
            git diff --staged --stat
          fi
      
      - name: Commit and Push Findings
        if: steps.check_updates.outputs.has_updates == 'true'
        run: |
          timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
          
          # Count changes
          files_changed=$(git diff --staged --numstat | wc -l)
          
          git commit -m "🤖 Autonomous Investigation Update - $timestamp

          Files changed: $files_changed
          Recovery status: ${{ steps.recovery.outputs.recovery_status || 'N/A' }}
          Investigation status: ${{ steps.investigation.outputs.investigation_status || 'N/A' }}
          
          Auto-committed by continuous investigation system
          Workflow: ${{ github.workflow }}
          Run: ${{ github.run_number }}"
          
          # Push with retry logic
          max_retries=3
          retry_count=0
          
          while [ $retry_count -lt $max_retries ]; do
            if git push origin HEAD:${{ github.ref_name }}; then
              echo "✓ Findings committed and pushed successfully"
              break
            else
              retry_count=$((retry_count + 1))
              echo "Push failed, retry $retry_count/$max_retries..."
              sleep 5
              git pull --rebase origin ${{ github.ref_name }}
            fi
          done
      
      - name: Create Investigation Report
        if: always()
        run: |
          echo "# Investigation Cycle Report" > cycle_report.md
          echo "" >> cycle_report.md
          echo "**Timestamp:** $(date -u)" >> cycle_report.md
          echo "**Workflow Run:** #${{ github.run_number }}" >> cycle_report.md
          echo "" >> cycle_report.md
          echo "## Status" >> cycle_report.md
          echo "" >> cycle_report.md
          echo "| Component | Status |" >> cycle_report.md
          echo "|-----------|--------|" >> cycle_report.md
          echo "| Error Recovery | ${{ steps.recovery.outcome }} |" >> cycle_report.md
          echo "| Investigation Cycle | ${{ steps.investigation.outcome }} |" >> cycle_report.md
          echo "| Updates Committed | ${{ steps.check_updates.outputs.has_updates || 'none' }} |" >> cycle_report.md
          echo "" >> cycle_report.md
          
          # Add data summary if available
          if [ -f "data/cycle_log.json" ]; then
            echo "## Cycle Log" >> cycle_report.md
            echo '```json' >> cycle_report.md
            tail -20 data/cycle_log.json >> cycle_report.md
            echo '```' >> cycle_report.md
          fi
          
          cat cycle_report.md
      
      - name: Upload Report Artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: investigation-report-${{ github.run_number }}
          path: |
            cycle_report.md
            data/cycle_log.json
            data/recovery_log.json
          retention-days: 30
      
      - name: Post-Cycle Cleanup
        if: always()
        run: |
          echo "Performing cleanup..."
          # Remove temporary files
          find . -name "*.pyc" -delete
          find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
          echo "✓ Cleanup completed"
"""


SELF_HEALING_WORKFLOW = """name: Self-Healing System

on:
  schedule:
    # Run every 2 hours to check system health
    - cron: '0 */2 * * *'
  workflow_dispatch:
  workflow_run:
    workflows: ["Continuous Investigation System"]
    types:
      - completed

permissions:
  contents: write
  issues: write
  actions: write

jobs:
  health-check:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Configure Git
        run: |
          git config --global user.name "Self-Healing Bot"
          git config --global user.email "self-healing-bot@users.noreply.github.com"
      
      - name: Run System Health Check
        id: health
        continue-on-error: true
        run: |
          echo "Running health diagnostics..."
          python3 autonomous_error_recovery.py
          echo "health_status=$?" >> $GITHUB_OUTPUT
      
      - name: Check for Fixes
        id: check_fixes
        run: |
          git add -A
          if git diff --staged --quiet; then
            echo "has_fixes=false" >> $GITHUB_OUTPUT
            echo "No fixes needed"
          else
            echo "has_fixes=true" >> $GITHUB_OUTPUT
            echo "Fixes applied"
          fi
      
      - name: Commit Fixes
        if: steps.check_fixes.outputs.has_fixes == 'true'
        run: |
          timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
          git commit -m "🔧 Self-Healing: Auto-fixed system issues - $timestamp

          Health status: ${{ steps.health.outputs.health_status }}
          
          Auto-committed by self-healing system"
          
          git push origin HEAD:${{ github.ref_name }}
          echo "✓ Fixes committed and pushed"
      
      - name: Upload Health Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: health-report-${{ github.run_number }}
          path: data/recovery_log.json
          retention-days: 30
"""


def deploy_workflows():
    """Deploy GitHub Actions workflows"""
    print("="*60)
    print("Workflow Deployment Bootstrap")
    print("="*60)
    print()
    
    # Create workflows directory
    workflows_dir = Path('.github/workflows')
    workflows_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created {workflows_dir}")
    
    # Write continuous investigation workflow
    continuous_file = workflows_dir / 'continuous-investigation.yml'
    with open(continuous_file, 'w') as f:
        f.write(CONTINUOUS_INVESTIGATION_WORKFLOW)
    print(f"✓ Created {continuous_file}")
    
    # Write self-healing workflow
    healing_file = workflows_dir / 'self-healing.yml'
    with open(healing_file, 'w') as f:
        f.write(SELF_HEALING_WORKFLOW)
    print(f"✓ Created {healing_file}")
    
    print()
    print("="*60)
    print("Deployment Complete!")
    print("="*60)
    print()
    print("Workflows created:")
    print(f"  - {continuous_file}")
    print(f"  - {healing_file}")
    print()
    print("Next steps:")
    print("  1. Commit these workflow files to your repository")
    print("  2. Push to GitHub")
    print("  3. Workflows will start running automatically")
    print()
    print("Commands:")
    print("  git add .github/workflows/")
    print('  git commit -m "Add continuous investigation workflows"')
    print("  git push")
    print()


if __name__ == "__main__":
    try:
        deploy_workflows()
        sys.exit(0)
    except Exception as e:
        print(f"✗ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
