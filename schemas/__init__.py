# create_init_files.py
import os
from pathlib import Path


def create_init_files():
    """Create __init__.py files for proper package structure"""

    directories = [
        'schemas',
        'loaders',
        'classification',
        'extraction'
    ]

    base_path = Path('.')

    for directory in directories:
        dir_path = base_path / directory
        init_file = dir_path / '__init__.py'

        # Create directory if it doesn't exist
        dir_path.mkdir(exist_ok=True)

        # Create __init__.py file
        if not init_file.exists():
            init_file.touch()
            print(f"Created: {init_file}")
        else:
            print(f"Exists: {init_file}")

    print("All __init__.py files created successfully!")


if __name__ == "__main__":
    create_init_files()
