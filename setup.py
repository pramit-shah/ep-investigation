#!/usr/bin/env python3
"""
Setup script for Epstein Investigation System
Initializes the database and creates necessary directories
"""

import os
import sys
from investigation_system import InvestigationDatabase, Entity, Evidence
from data_collector import create_initial_data_structure


def setup_investigation_system():
    """Initialize the investigation system"""
    print("="*60)
    print("Epstein Investigation System - Setup")
    print("="*60)
    print()
    
    # Create directory structure
    print("Step 1: Creating directory structure...")
    create_initial_data_structure()
    print("✓ Directories created")
    print()
    
    # Initialize database
    print("Step 2: Initializing investigation database...")
    db = InvestigationDatabase()
    
    # Add core entity
    epstein = Entity("Jeffrey Epstein", "person", {
        "role": "Primary Subject",
        "status": "Deceased",
        "date_of_death": "2019-08-10"
    })
    epstein.add_tag("primary_subject")
    epstein.add_tag("deceased")
    db.add_entity(epstein)
    
    # Save initial database
    db.save_to_file()
    print("✓ Database initialized with core entity")
    print()
    
    # Show next steps
    print("="*60)
    print("Setup Complete!")
    print("="*60)
    print()
    print("Next Steps:")
    print("1. Run 'python3 cli.py' to start the interactive interface")
    print("2. Run 'python3 cli.py --summary' to view investigation summary")
    print("3. Add entities and evidence using the CLI or Python API")
    print("4. Review the README.md for detailed documentation")
    print()
    print("Quick Start:")
    print("  python3 cli.py              # Interactive mode")
    print("  python3 cli.py --summary    # Quick summary")
    print()
    print("Templates available in the 'templates/' directory")
    print()
    return True


def verify_python_version():
    """Verify Python version is sufficient"""
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True


def main():
    """Main setup function"""
    if not verify_python_version():
        sys.exit(1)
    
    try:
        setup_investigation_system()
        print("✓ Setup completed successfully")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
