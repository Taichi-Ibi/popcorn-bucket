from typing import Protocol
from result_types.result_types import TaskResult, TaskListResult


class TaskStorageProtocol(Protocol):
    """Protocol for task storage implementations.
    
    Defines the interface that any task storage backend must implement.
    This allows for different storage implementations (JSON, database, etc.)
    while maintaining the same interface.
    """
    
    def save_tasks(self, tasks: list) -> tuple[bool, str | None]:
        """Save tasks to storage.
        
        Args:
            tasks: List of tasks to save
            
        Returns:
            Tuple of (success, error_message)
        """
        ...
    
    def load_tasks(self) -> TaskListResult:
        """Load tasks from storage.
        
        Returns:
            Tuple of (tasks_list, error_message)
        """
        ...
    
    def backup_data(self) -> tuple[bool, str | None]:
        """Create a backup of current data.
        
        Returns:
            Tuple of (success, error_message)
        """
        ...
