#!/usr/bin/env python3
"""Complete CLI functionality demonstration."""

import sys
import subprocess
from pathlib import Path

def run_command(cmd_args, description):
    """Run a CLI command and capture output."""
    print(f"\n=== {description} ===")
    print(f"Command: python todo.py {' '.join(cmd_args)}")
    
    cmd = [sys.executable, "todo.py"] + cmd_args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/workspaces/popcorn-bucket/cli-todo")
    
    if result.stdout:
        print("Output:")
        print(result.stdout)
    if result.stderr:
        print("Error:")
        print(result.stderr)
    if result.returncode != 0:
        print(f"Exit code: {result.returncode}")
    
    return result.returncode == 0

def demo_cli():
    """Demonstrate all CLI functionality."""
    print("CLI TODO Manager - Complete Functionality Demo")
    print("=" * 50)
    
    # Clear existing data
    data_file = Path("/workspaces/popcorn-bucket/cli-todo/data/tasks.json")
    if data_file.exists():
        data_file.unlink()
    
    # Test help
    run_command(["--help"], "Help Command")
    
    # Add tasks
    run_command(["add", "Implement user authentication", "--priority", "high", "--due-date", "2025-07-01"], 
                "Add Task with Priority and Due Date")
    
    run_command(["add", "Write unit tests", "--priority", "medium"], 
                "Add Task with Priority Only")
    
    run_command(["add", "Update documentation"], 
                "Add Simple Task")
    
    # List all tasks
    run_command(["list"], "List All Tasks")
    
    # Complete a task
    run_command(["done", "2"], "Mark Task 2 as Completed")
    
    # List pending tasks only
    run_command(["list", "--status", "pending"], "List Pending Tasks")
    
    # List completed tasks only
    run_command(["list", "--status", "completed"], "List Completed Tasks")
    
    # Set priority
    run_command(["priority", "3", "high"], "Set Task 3 Priority to High")
    
    # Set due date
    run_command(["due", "3", "2025-06-30"], "Set Task 3 Due Date")
    
    # List all tasks to see changes
    run_command(["list"], "Final Task List")
    
    # Test error handling
    run_command(["done", "999"], "Error: Non-existent Task ID")
    
    run_command(["priority", "1", "urgent"], "Error: Invalid Priority")
    
    run_command(["due", "1", "invalid-date"], "Error: Invalid Date Format")
    
    # Test overdue tasks (if any exist)
    run_command(["list", "--overdue"], "List Overdue Tasks")
    
    print("\n" + "=" * 50)
    print("Demo completed! Check the outputs above to verify all functionality works correctly.")

if __name__ == "__main__":
    demo_cli()
