#!/usr/bin/env python3
"""Test CLI add command."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def test_add_task():
    try:
        from services.task_service import create_task_service
        print("✅ TaskService import successful")
        
        service = create_task_service()
        print("✅ TaskService created")
        
        task, error = service.create_task("Test task from script")
        if error:
            print(f"❌ Error creating task: {error}")
        else:
            print(f"✅ Task created successfully: ID {task.id}, Title: {task.title}")
            
        # List tasks
        tasks, error = service.list_tasks()
        if error:
            print(f"❌ Error listing tasks: {error}")
        else:
            print(f"✅ Found {len(tasks)} tasks")
            for task in tasks:
                print(f"  - {task.id}: {task.title} ({task.status.value})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_add_task()
