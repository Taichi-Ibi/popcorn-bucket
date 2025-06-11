#!/usr/bin/env python3
"""Test CLI functionality and write results to file."""

import sys
from pathlib import Path
import traceback

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def run_tests():
    results = []
    
    try:
        # Test 1: Import validation
        from validators.task_validator import validate_task_title
        results.append("✅ Validator import successful")
        
        # Test 2: Validation function
        is_valid, error = validate_task_title("Test task")
        if is_valid and not error:
            results.append("✅ Task validation successful")
        else:
            results.append(f"❌ Task validation failed: {error}")
        
        # Test 3: Model import
        from models.task import Task, TaskStatus, TaskPriority
        results.append("✅ Model import successful")
        
        # Test 4: Create task instance
        task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            due_date=None,
            created_at="2025-06-11T10:00:00",
            completed_at=None
        )
        results.append(f"✅ Task created: {task.title}")
        
        # Test 5: Repository import
        from repositories.task_repository import JsonTaskRepository
        results.append("✅ Repository import successful")
        
        # Test 6: Service import
        from services.task_service import create_task_service
        results.append("✅ Service import successful")
        
        # Test 7: Create service
        service = create_task_service()
        results.append("✅ Service created")
        
        # Test 8: CLI import
        from cli.main import create_parser
        results.append("✅ CLI import successful")
        
        results.append("🎉 All imports and basic functionality working!")
        
    except Exception as e:
        results.append(f"❌ Error: {e}")
        results.append(f"Traceback: {traceback.format_exc()}")
    
    # Write results to file
    with open("test_results.txt", "w") as f:
        for result in results:
            f.write(result + "\n")
    
    return results

if __name__ == "__main__":
    run_tests()
