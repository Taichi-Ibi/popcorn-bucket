import json
from pathlib import Path
from typing import Any
from ..result_types.result_types import TaskResult, TaskListResult
from ..models.task import Task, TaskStatus, TaskPriority
from ..protocols.storage_protocol import TaskStorageProtocol


class JsonTaskRepository(TaskStorageProtocol):
    """JSON file-based task repository implementation.
    
    Handles persistence of tasks to/from JSON files with atomic writes
    and backup functionality.
    """
    
    def __init__(self, data_file: str = "data/tasks.json"):
        """Initialize repository with data file path.
        
        Args:
            data_file: Path to JSON data file
        """
        self.data_file = Path(data_file)
        self.backup_file = Path(f"{data_file}.backup")
        
        # Ensure data directory exists
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
    
    def save_tasks(self, tasks: list[Task]) -> tuple[bool, str | None]:
        """Save tasks to JSON file with atomic write operation.
        
        Args:
            tasks: List of tasks to save
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Create backup before saving
            if self.data_file.exists():
                backup_success, backup_error = self.backup_data()
                if backup_error:
                    return False, f"backup_error: {backup_error}"
            
            # Convert tasks to dictionary format
            tasks_data = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status.value,
                    "priority": task.priority.value,
                    "due_date": task.due_date,
                    "created_at": task.created_at,
                    "completed_at": task.completed_at
                }
                tasks_data.append(task_dict)
            
            # Write to temporary file first (atomic operation)
            temp_file = self.data_file.with_suffix('.tmp')
            with temp_file.open('w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
            
            # Move temporary file to final location
            temp_file.replace(self.data_file)
            
            return True, None
            
        except PermissionError:
            return False, "file_io_error: permission denied to write data file"
        except OSError as e:
            return False, f"file_io_error: {e}"
        except Exception as e:
            return False, f"unexpected_error: {e}"
    
    def load_tasks(self) -> TaskListResult:
        """Load tasks from JSON file.
        
        Returns:
            Tuple of (tasks_list, error_message)
        """
        try:
            if not self.data_file.exists():
                # Return empty list if file doesn't exist (first run)
                return [], None
            
            # Check if file is empty
            if self.data_file.stat().st_size == 0:
                return [], None
            
            with self.data_file.open('r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return [], None
                tasks_data = json.loads(content)
            
            # Convert dictionary data to Task objects
            tasks = []
            for task_dict in tasks_data:
                try:
                    task = Task(
                        id=task_dict["id"],
                        title=task_dict["title"],
                        status=TaskStatus(task_dict["status"]),
                        priority=TaskPriority(task_dict["priority"]),
                        due_date=task_dict.get("due_date"),
                        created_at=task_dict["created_at"],
                        completed_at=task_dict.get("completed_at")
                    )
                    tasks.append(task)
                except (KeyError, ValueError) as e:
                    return None, f"data_format_error: invalid task data - {e}"
            
            return tasks, None
            
        except FileNotFoundError:
            return [], None  # File doesn't exist, return empty list
        except PermissionError:
            return None, "file_io_error: permission denied to read data file"
        except json.JSONDecodeError as e:
            return None, f"json_parse_error: {e}"
        except Exception as e:
            return None, f"unexpected_error: {e}"
    
    def backup_data(self) -> tuple[bool, str | None]:
        """Create a backup of the current data file.
        
        Returns:
            Tuple of (success, error_message)
        """
        try:
            if not self.data_file.exists():
                return True, None  # Nothing to backup
            
            import shutil
            shutil.copy2(self.data_file, self.backup_file)
            return True, None
            
        except PermissionError:
            return False, "file_io_error: permission denied to create backup"
        except OSError as e:
            return False, f"file_io_error: {e}"
        except Exception as e:
            return False, f"unexpected_error: {e}"


def create_task_repository(data_file: str | None = None) -> JsonTaskRepository:
    """Factory function to create a task repository instance.
    
    Args:
        data_file: Optional custom data file path
        
    Returns:
        JsonTaskRepository instance
    """
    if data_file:
        return JsonTaskRepository(data_file)
    return JsonTaskRepository()
