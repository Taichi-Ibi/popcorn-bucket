from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Task completion status."""
    PENDING = "pending"
    COMPLETED = "completed"


class TaskPriority(Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class Task:
    """Immutable task data structure.
    
    All business logic is implemented as separate functions,
    following Pygon principles of data-logic separation.
    """
    id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    due_date: str | None  # ISO format YYYY-MM-DD or None
    created_at: str  # ISO format datetime string
    completed_at: str | None  # ISO format datetime string or None


# Processing functions separated from data structure
def is_task_overdue(task: Task, current_date: str) -> tuple[bool, str | None]:
    """Check if task is overdue based on current date.
    
    Args:
        task: Task to check
        current_date: Current date in ISO format (YYYY-MM-DD)
        
    Returns:
        Tuple of (is_overdue, error_message)
    """
    if not task.due_date:
        return False, None
    
    if task.status == TaskStatus.COMPLETED:
        return False, None
    
    try:
        from datetime import datetime
        due = datetime.fromisoformat(task.due_date)
        current = datetime.fromisoformat(current_date)
        return due.date() < current.date(), None
    except ValueError as e:
        return False, f"date_parse_error: {e}"


def mark_task_completed(task: Task, completion_time: str) -> Task:
    """Create a new task instance marked as completed.
    
    Args:
        task: Original task
        completion_time: Completion time in ISO format
        
    Returns:
        New task instance with completed status
    """
    return Task(
        id=task.id,
        title=task.title,
        status=TaskStatus.COMPLETED,
        priority=task.priority,
        due_date=task.due_date,
        created_at=task.created_at,
        completed_at=completion_time
    )


def update_task_priority(task: Task, new_priority: TaskPriority) -> Task:
    """Create a new task instance with updated priority.
    
    Args:
        task: Original task
        new_priority: New priority level
        
    Returns:
        New task instance with updated priority
    """
    return Task(
        id=task.id,
        title=task.title,
        status=task.status,
        priority=new_priority,
        due_date=task.due_date,
        created_at=task.created_at,
        completed_at=task.completed_at
    )


def update_task_due_date(task: Task, new_due_date: str | None) -> Task:
    """Create a new task instance with updated due date.
    
    Args:
        task: Original task
        new_due_date: New due date in ISO format or None
        
    Returns:
        New task instance with updated due date
    """
    return Task(
        id=task.id,
        title=task.title,
        status=task.status,
        priority=task.priority,
        due_date=new_due_date,
        created_at=task.created_at,
        completed_at=task.completed_at
    )
