from result_types.result_types import ValidationResult, MultipleErrorResult
from models.task import TaskPriority


def validate_task_title(title: str) -> ValidationResult:
    """Validate task title according to business rules.
    
    Args:
        title: Task title to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title:
        return False, "validation_error: task title is required"
    
    if not title.strip():
        return False, "validation_error: task title cannot be empty or whitespace only"
    
    if len(title.strip()) > 100:
        return False, "validation_error: task title too long (max 100 characters)"
    
    return True, None


def validate_due_date_format(due_date: str) -> ValidationResult:
    """Validate due date format (YYYY-MM-DD).
    
    Args:
        due_date: Due date string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not due_date:
        return False, "validation_error: due date is required"
    
    try:
        from datetime import datetime
        datetime.strptime(due_date, "%Y-%m-%d")
        return True, None
    except ValueError:
        return False, "validation_error: invalid due date format (use YYYY-MM-DD)"


def validate_priority_value(priority: str) -> ValidationResult:
    """Validate priority value against allowed values.
    
    Args:
        priority: Priority string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not priority:
        return False, "validation_error: priority is required"
    
    valid_priorities = [p.value for p in TaskPriority]
    if priority.lower() not in valid_priorities:
        valid_list = ", ".join(valid_priorities)
        return False, f"validation_error: invalid priority '{priority}' (valid: {valid_list})"
    
    return True, None


def validate_task_creation_data(task_data: dict) -> MultipleErrorResult:
    """Validate all data required for task creation.
    
    Args:
        task_data: Dictionary containing task creation data
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Validate title
    title = task_data.get("title", "")
    is_valid, error = validate_task_title(title)
    if error:
        errors.append(error)
    
    # Validate due date if provided
    due_date = task_data.get("due_date")
    if due_date:
        is_valid, error = validate_due_date_format(due_date)
        if error:
            errors.append(error)
    
    # Validate priority if provided
    priority = task_data.get("priority")
    if priority:
        is_valid, error = validate_priority_value(priority)
        if error:
            errors.append(error)
    
    return len(errors) == 0, errors


def validate_task_id(task_id: str) -> ValidationResult:
    """Validate task ID format (must be positive integer).
    
    Args:
        task_id: Task ID string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not task_id:
        return False, "validation_error: task ID is required"
    
    try:
        id_int = int(task_id)
        if id_int <= 0:
            return False, "validation_error: task ID must be a positive integer"
        return True, None
    except ValueError:
        return False, "validation_error: task ID must be a valid integer"
