from datetime import datetime
from ..result_types.result_types import TaskResult, TaskListResult, ValidationResult
from ..models.task import Task, TaskStatus, TaskPriority, mark_task_completed, update_task_priority, update_task_due_date
from ..validators.task_validator import validate_task_title, validate_due_date_format, validate_priority_value, validate_task_id
from ..repositories.task_repository import JsonTaskRepository


class TaskService:
    """Service layer for task business logic.
    
    Handles all task-related operations with comprehensive error handling
    and validation following Pygon principles.
    """
    
    def __init__(self, repository: JsonTaskRepository):
        """Initialize service with repository dependency.
        
        Args:
            repository: Task repository for data persistence
        """
        self.repository = repository
    
    def create_task(self, title: str, priority: str = "medium", due_date: str | None = None) -> TaskResult:
        """Create a new task with validation.
        
        Args:
            title: Task title
            priority: Task priority (high, medium, low)
            due_date: Optional due date in YYYY-MM-DD format
            
        Returns:
            Tuple of (created_task, error_message)
        """
        # Validate inputs
        is_valid, error = validate_task_title(title)
        if error:
            return None, error
        
        is_valid, error = validate_priority_value(priority)
        if error:
            return None, error
        
        if due_date:
            is_valid, error = validate_due_date_format(due_date)
            if error:
                return None, error
        
        # Load existing tasks to generate new ID
        tasks, error = self.repository.load_tasks()
        if error:
            return None, error
        
        # Generate new task ID
        new_id = max([task.id for task in tasks], default=0) + 1
        
        # Create new task
        current_time = datetime.now().isoformat()
        new_task = Task(
            id=new_id,
            title=title.strip(),
            status=TaskStatus.PENDING,
            priority=TaskPriority(priority.lower()),
            due_date=due_date,
            created_at=current_time,
            completed_at=None
        )
        
        # Add to tasks list and save
        tasks.append(new_task)
        save_success, error = self.repository.save_tasks(tasks)
        if error:
            return None, error
        
        return new_task, None
    
    def list_tasks(self, status_filter: str | None = None) -> TaskListResult:
        """List all tasks with optional status filtering.
        
        Args:
            status_filter: Optional status filter (pending, completed)
            
        Returns:
            Tuple of (tasks_list, error_message)
        """
        tasks, error = self.repository.load_tasks()
        if error:
            return None, error
        
        # Apply status filter if provided
        if status_filter:
            try:
                filter_status = TaskStatus(status_filter.lower())
                filtered_tasks = [task for task in tasks if task.status == filter_status]
                return filtered_tasks, None
            except ValueError:
                return None, f"validation_error: invalid status filter '{status_filter}' (valid: pending, completed)"
        
        return tasks, None
    
    def complete_task(self, task_id: str) -> TaskResult:
        """Mark a task as completed.
        
        Args:
            task_id: ID of task to complete
            
        Returns:
            Tuple of (completed_task, error_message)
        """
        # Validate task ID
        is_valid, error = validate_task_id(task_id)
        if error:
            return None, error
        
        # Load tasks and find target task
        tasks, error = self.repository.load_tasks()
        if error:
            return None, error
        
        task_id_int = int(task_id)
        target_task = None
        task_index = None
        
        for i, task in enumerate(tasks):
            if task.id == task_id_int:
                target_task = task
                task_index = i
                break
        
        if not target_task:
            return None, f"not_found_error: task with ID {task_id} not found"
        
        if target_task.status == TaskStatus.COMPLETED:
            return None, f"validation_error: task {task_id} is already completed"
        
        # Mark as completed
        completion_time = datetime.now().isoformat()
        completed_task = mark_task_completed(target_task, completion_time)
        
        # Update tasks list and save
        tasks[task_index] = completed_task
        save_success, error = self.repository.save_tasks(tasks)
        if error:
            return None, error
        
        return completed_task, None
    
    def delete_task(self, task_id: str) -> tuple[bool, str | None]:
        """Delete a task by ID.
        
        Args:
            task_id: ID of task to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        # Validate task ID
        is_valid, error = validate_task_id(task_id)
        if error:
            return False, error
        
        # Load tasks and find target task
        tasks, error = self.repository.load_tasks()
        if error:
            return False, error
        
        task_id_int = int(task_id)
        task_found = False
        
        # Remove task from list
        updated_tasks = []
        for task in tasks:
            if task.id == task_id_int:
                task_found = True
            else:
                updated_tasks.append(task)
        
        if not task_found:
            return False, f"not_found_error: task with ID {task_id} not found"
        
        # Save updated tasks list
        save_success, error = self.repository.save_tasks(updated_tasks)
        if error:
            return False, error
        
        return True, None
    
    def set_task_priority(self, task_id: str, priority: str) -> TaskResult:
        """Set task priority.
        
        Args:
            task_id: ID of task to update
            priority: New priority level (high, medium, low)
            
        Returns:
            Tuple of (updated_task, error_message)
        """
        # Validate inputs
        is_valid, error = validate_task_id(task_id)
        if error:
            return None, error
        
        is_valid, error = validate_priority_value(priority)
        if error:
            return None, error
        
        # Load tasks and find target task
        tasks, error = self.repository.load_tasks()
        if error:
            return None, error
        
        task_id_int = int(task_id)
        target_task = None
        task_index = None
        
        for i, task in enumerate(tasks):
            if task.id == task_id_int:
                target_task = task
                task_index = i
                break
        
        if not target_task:
            return None, f"not_found_error: task with ID {task_id} not found"
        
        # Update priority
        new_priority = TaskPriority(priority.lower())
        updated_task = update_task_priority(target_task, new_priority)
        
        # Update tasks list and save
        tasks[task_index] = updated_task
        save_success, error = self.repository.save_tasks(tasks)
        if error:
            return None, error
        
        return updated_task, None
    
    def set_task_due_date(self, task_id: str, due_date: str) -> TaskResult:
        """Set task due date.
        
        Args:
            task_id: ID of task to update
            due_date: Due date in YYYY-MM-DD format
            
        Returns:
            Tuple of (updated_task, error_message)
        """
        # Validate inputs
        is_valid, error = validate_task_id(task_id)
        if error:
            return None, error
        
        is_valid, error = validate_due_date_format(due_date)
        if error:
            return None, error
        
        # Load tasks and find target task
        tasks, error = self.repository.load_tasks()
        if error:
            return None, error
        
        task_id_int = int(task_id)
        target_task = None
        task_index = None
        
        for i, task in enumerate(tasks):
            if task.id == task_id_int:
                target_task = task
                task_index = i
                break
        
        if not target_task:
            return None, f"not_found_error: task with ID {task_id} not found"
        
        # Update due date
        updated_task = update_task_due_date(target_task, due_date)
        
        # Update tasks list and save
        tasks[task_index] = updated_task
        save_success, error = self.repository.save_tasks(tasks)
        if error:
            return None, error
        
        return updated_task, None
    
    def get_overdue_tasks(self) -> TaskListResult:
        """Get all overdue tasks.
        
        Returns:
            Tuple of (overdue_tasks_list, error_message)
        """
        tasks, error = self.repository.load_tasks()
        if error:
            return None, error
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        overdue_tasks = []
        
        for task in tasks:
            if task.status == TaskStatus.PENDING and task.due_date:
                try:
                    from ..models.task import is_task_overdue
                    is_overdue, check_error = is_task_overdue(task, current_date)
                    if check_error:
                        return None, check_error
                    if is_overdue:
                        overdue_tasks.append(task)
                except Exception as e:
                    return None, f"date_check_error: {e}"
        
        return overdue_tasks, None


def create_task_service(repository: JsonTaskRepository | None = None) -> TaskService:
    """Factory function to create a task service instance.
    
    Args:
        repository: Optional custom repository instance
        
    Returns:
        TaskService instance
    """
    if repository:
        return TaskService(repository)
    
    from ..repositories.task_repository import create_task_repository
    default_repository = create_task_repository()
    return TaskService(default_repository)
