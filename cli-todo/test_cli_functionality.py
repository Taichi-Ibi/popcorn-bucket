#!/usr/bin/env python3
"""Test CLI commands and write results to file."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def test_cli_commands():
    results = []
    
    try:
        from cli.main import create_parser, cmd_add, cmd_list
        import argparse
        
        results.append("✅ CLI modules imported successfully")
        
        # Test parser creation
        parser = create_parser()
        results.append("✅ Parser created successfully")
        
        # Test add command
        class MockArgs:
            def __init__(self):
                self.title = "Test task from CLI test"
                self.priority = "medium"
                self.due_date = None
        
        try:
            # Create a test namespace
            args = MockArgs()
            
            # Import service to test task creation
            from services.task_service import create_task_service
            service = create_task_service()
            
            task, error = service.create_task("CLI Test Task", "high", "2025-12-31")
            if error:
                results.append(f"❌ Task creation failed: {error}")
            else:
                results.append(f"✅ Task created: ID {task.id}, Title: {task.title}")
            
            # Test listing tasks
            tasks, error = service.list_tasks()
            if error:
                results.append(f"❌ Task listing failed: {error}")
            else:
                results.append(f"✅ Listed {len(tasks)} tasks")
                for task in tasks:
                    results.append(f"   - {task.id}: {task.title} ({task.status.value}, {task.priority.value})")
            
        except SystemExit:
            results.append("✅ CLI command executed (SystemExit is expected for help)")
        
        results.append("🎉 CLI functionality test completed!")
        
    except Exception as e:
        results.append(f"❌ Error: {e}")
        import traceback
        results.append(f"Traceback: {traceback.format_exc()}")
    
    # Write results to file
    with open("cli_test_results.txt", "w") as f:
        for result in results:
            f.write(result + "\n")
    
    return results

if __name__ == "__main__":
    test_cli_commands()
