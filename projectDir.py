import os
import sys
from pathlib import Path
import constants
import shutil # for copying files

"""
This module provides functions to initialize and check the project directory.
It ensures that necessary files like objects.yaml, csound.csd, and config.yaml exist.
If any of these files are missing, it copies them from a source directory.
"""

def init_project_dir(directory):
    """
    Initialize the project directory
    """
    # Make directory
    directory = Path(directory)
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created project directory: {directory.resolve()}")
    else:
        print(f"Project directory already exists: {directory.resolve()}")

def check_project_dir(directory):
    """
    Check if the given directory is a valid project directory.
    """
    was_incomplete = False
    directory = Path(directory)
    
    if not directory.is_dir():
        print(f"The path '{directory}' is not a valid directory.")
        init_project_dir(directory)
        was_incomplete = True
    
    # Check if objects.yaml exists
    object_yaml_path = directory / constants.YAML_PATH
    
    if not object_yaml_path.exists():
        print(f"Object model file '{constants.YAML_PATH}' does not exist in the directory. Creating one now...")
        src_path = Path("src/objects.yaml")  # Assuming the source file is in a src directory
        was_incomplete = True
        if src_path.exists():
            shutil.copy(src_path, object_yaml_path)
            print(f"Copied '{constants.YAML_PATH}' to {object_yaml_path.resolve()}")
        else:
            raise FileNotFoundError(f"Source object model file not found at {src_path.resolve()}. Please ensure it exists.")
    
    # Check if csound.csd exists
    csound_csd_path = directory / 'csound.csd'
    if not csound_csd_path.exists():
        print(f"Csound file 'csound.csd' does not exist in the directory. Creating csound file.")
        src_path = Path("src/csound.csd")  # Assuming the source file is in a src directory
        was_incomplete = True
        if src_path.exists():
            shutil.copy(src_path, csound_csd_path)
            print(f"Copied 'csound.csd' to {csound_csd_path.resolve()}")
        else:
            raise FileNotFoundError(f"Source csound file not found at {src_path.resolve()}. Please ensure it exists.")
        
    # Check if config.yaml exists
    constants_path = directory / 'config.yaml'
    if not constants_path.exists():
        print(f"Constants file 'config.yaml' does not exist in the directory. Creating one now...")
        src_constants_path = Path("src/config.yaml")  # Assuming the source file is in a src directory
        was_incomplete = True
        if src_constants_path.exists():
            shutil.copy(src_constants_path, constants_path)
            print(f"Copied 'config.yaml' to {constants_path.resolve()}")
        else:
            raise FileNotFoundError(f"Source constants file not found at {src_constants_path.resolve()}. Please ensure it exists.")
    
    # If project directory was incomplete, then dont run the rest of the program
    return was_incomplete