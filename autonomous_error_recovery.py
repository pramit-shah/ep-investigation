#!/usr/bin/env python3
"""
Autonomous Error Recovery System
Detects, diagnoses, and fixes errors automatically
"""

import os
import sys
import json
import traceback
import subprocess
from datetime import datetime
from pathlib import Path


class ErrorRecoverySystem:
    """Autonomous error detection and recovery"""
    
    def __init__(self):
        self.recovery_log = []
        self.errors_fixed = 0
        self.errors_detected = 0
        
    def log_recovery(self, error_type, action, success):
        """Log recovery attempt"""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'error_type': error_type,
            'action': action,
            'success': success
        }
        self.recovery_log.append(entry)
        
        if success:
            self.errors_fixed += 1
    
    def check_python_syntax(self):
        """Check all Python files for syntax errors"""
        print("Checking Python syntax...")
        errors = []
        
        for py_file in Path('.').glob('*.py'):
            try:
                with open(py_file, 'r') as f:
                    compile(f.read(), py_file, 'exec')
            except SyntaxError as e:
                errors.append({
                    'file': str(py_file),
                    'error': str(e),
                    'line': e.lineno
                })
                self.errors_detected += 1
        
        return errors
    
    def check_data_integrity(self):
        """Check data files for corruption"""
        print("Checking data integrity...")
        errors = []
        
        # Check main database
        db_file = Path('data/investigation_data.json')
        if db_file.exists():
            try:
                with open(db_file, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                errors.append({
                    'file': str(db_file),
                    'error': 'JSON corruption',
                    'details': str(e)
                })
                self.errors_detected += 1
        
        return errors
    
    def check_directory_structure(self):
        """Verify required directories exist"""
        print("Checking directory structure...")
        required_dirs = [
            'data',
            'data/entities',
            'data/evidence',
            'data/connections',
            'data/reports',
            'data/timeline',
            'data/analysis',
            'data/collected'
        ]
        
        missing = []
        for directory in required_dirs:
            if not Path(directory).exists():
                missing.append(directory)
                self.errors_detected += 1
        
        return missing
    
    def fix_directory_structure(self, missing_dirs):
        """Recreate missing directories"""
        print(f"Fixing {len(missing_dirs)} missing directories...")
        
        for directory in missing_dirs:
            try:
                Path(directory).mkdir(parents=True, exist_ok=True)
                self.log_recovery('missing_directory', f'Created {directory}', True)
                print(f"  ✓ Created {directory}")
            except Exception as e:
                self.log_recovery('missing_directory', f'Failed to create {directory}', False)
                print(f"  ✗ Failed to create {directory}: {e}")
    
    def fix_corrupted_database(self):
        """Attempt to recover or reinitialize corrupted database"""
        print("Attempting to fix corrupted database...")
        
        db_file = Path('data/investigation_data.json')
        backup_file = Path('data/investigation_data.json.backup')
        
        # Try to restore from backup
        if backup_file.exists():
            try:
                with open(backup_file, 'r') as f:
                    data = json.load(f)
                with open(db_file, 'w') as f:
                    json.dump(data, f, indent=2)
                self.log_recovery('database_corruption', 'Restored from backup', True)
                print("  ✓ Restored database from backup")
                return True
            except Exception as e:
                print(f"  ✗ Failed to restore from backup: {e}")
        
        # Reinitialize if no backup
        try:
            subprocess.run(['python3', 'setup.py'], check=True, capture_output=True)
            self.log_recovery('database_corruption', 'Reinitialized database', True)
            print("  ✓ Reinitialized database")
            return True
        except Exception as e:
            self.log_recovery('database_corruption', 'Failed to reinitialize', False)
            print(f"  ✗ Failed to reinitialize: {e}")
            return False
    
    def run_system_tests(self):
        """Run all test files to verify system health"""
        print("Running system tests...")
        
        test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        
        for test_file in Path('.').glob('test_*.py'):
            try:
                result = subprocess.run(
                    ['python3', str(test_file)],
                    capture_output=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    test_results['passed'] += 1
                    print(f"  ✓ {test_file.name} passed")
                else:
                    test_results['failed'] += 1
                    test_results['errors'].append({
                        'file': str(test_file),
                        'error': result.stderr.decode()[:200]
                    })
                    print(f"  ✗ {test_file.name} failed")
            except subprocess.TimeoutExpired:
                test_results['failed'] += 1
                test_results['errors'].append({
                    'file': str(test_file),
                    'error': 'Test timeout'
                })
                print(f"  ✗ {test_file.name} timed out")
            except Exception as e:
                test_results['failed'] += 1
                test_results['errors'].append({
                    'file': str(test_file),
                    'error': str(e)
                })
                print(f"  ✗ {test_file.name} error: {e}")
        
        return test_results
    
    def create_backup(self):
        """Create backup of critical data"""
        print("Creating backup...")
        
        db_file = Path('data/investigation_data.json')
        if db_file.exists():
            backup_file = Path('data/investigation_data.json.backup')
            try:
                import shutil
                shutil.copy2(db_file, backup_file)
                print("  ✓ Backup created")
                return True
            except Exception as e:
                print(f"  ✗ Backup failed: {e}")
                return False
        return False
    
    def run_full_recovery(self):
        """Run complete error detection and recovery cycle"""
        print("="*60)
        print("Autonomous Error Recovery System")
        print("="*60)
        print()
        
        # Create backup first
        self.create_backup()
        
        # Check directory structure
        missing_dirs = self.check_directory_structure()
        if missing_dirs:
            self.fix_directory_structure(missing_dirs)
        
        # Check data integrity
        data_errors = self.check_data_integrity()
        if data_errors:
            print(f"Found {len(data_errors)} data integrity issues")
            self.fix_corrupted_database()
        
        # Check Python syntax
        syntax_errors = self.check_python_syntax()
        if syntax_errors:
            print(f"Found {len(syntax_errors)} syntax errors")
            for error in syntax_errors:
                print(f"  ✗ {error['file']}: Line {error['line']}: {error['error']}")
        
        # Run tests
        test_results = self.run_system_tests()
        
        # Generate report
        print()
        print("="*60)
        print("Recovery Summary")
        print("="*60)
        print(f"Errors Detected: {self.errors_detected}")
        print(f"Errors Fixed: {self.errors_fixed}")
        print(f"Tests Passed: {test_results['passed']}")
        print(f"Tests Failed: {test_results['failed']}")
        print()
        
        # Save recovery log
        log_file = Path('data/recovery_log.json')
        try:
            with open(log_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.utcnow().isoformat(),
                    'errors_detected': self.errors_detected,
                    'errors_fixed': self.errors_fixed,
                    'test_results': test_results,
                    'recovery_log': self.recovery_log
                }, f, indent=2)
            print(f"Recovery log saved to {log_file}")
        except Exception as e:
            print(f"Failed to save recovery log: {e}")
        
        return {
            'errors_detected': self.errors_detected,
            'errors_fixed': self.errors_fixed,
            'test_results': test_results,
            'success': self.errors_fixed >= self.errors_detected
        }


def main():
    """Main entry point"""
    recovery = ErrorRecoverySystem()
    
    try:
        result = recovery.run_full_recovery()
        
        if result['success']:
            print("\n✓ Recovery completed successfully")
            sys.exit(0)
        else:
            print("\n⚠ Recovery completed with warnings")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n✗ Recovery failed: {e}")
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
