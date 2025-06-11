import pytest
import sys
from pathlib import Path

# Add src to path for testing
src_path = Path(__file__).parent.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from models.task import (
    Task, TaskStatus, TaskPriority,
    is_task_overdue, mark_task_completed,
    update_task_priority, update_task_due_date
)


class TestTaskModel:
    """Test cases for Task data model."""
    
    def test_task_creation_with_all_fields(self):
        """Test creating task with all fields."""
        task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH,
            due_date="2025-12-31",
            created_at="2025-06-11T10:00:00",
            completed_at=None
        )
        assert task.id == 1
        assert task.title == "Test task"
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == "2025-12-31"
        assert task.created_at == "2025-06-11T10:00:00"
        assert task.completed_at is None
    
    def test_task_is_immutable(self):
        """Test that Task is immutable (frozen dataclass)."""
        task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            due_date=None,
            created_at="2025-06-11T10:00:00",
            completed_at=None
        )
        
        # Should raise FrozenInstanceError when trying to modify
        with pytest.raises(Exception):  # FrozenInstanceError
            task.title = "Modified title"


class TestTaskStatusEnum:
    """Test cases for TaskStatus enum."""
    
    def test_task_status_values(self):
        """Test TaskStatus enum values."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.COMPLETED.value == "completed"


class TestTaskPriorityEnum:
    """Test cases for TaskPriority enum."""
    
    def test_task_priority_values(self):
        """Test TaskPriority enum values."""
        assert TaskPriority.HIGH.value == "high"
        assert TaskPriority.MEDIUM.value == "medium"
        assert TaskPriority.LOW.value == "low"


class TestTaskOverdueCheck:
    """Test cases for task overdue checking."""
    
    def test_task_without_due_date_not_overdue(self):
        """Test that task without due date is not overdue."""
        task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            due_date=None,
            created_at="2025-06-11T10:00:00",
            completed_at=None
        )
        
        is_overdue, error = is_task_overdue(task, "2025-06-12")
        assert error is None
        assert is_overdue is False
    
    def test_completed_task_not_overdue(self):
        """Test that completed task is not considered overdue."""
        task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.MEDIUM,
            due_date="2025-06-10",  # Past date
            created_at="2025-06-11T10:00:00",
            completed_at="2025-06-11T15:00:00"
        )
        
        is_overdue, error = is_task_overdue(task, "2025-06-12")
        assert error is None
        assert is_overdue is False
    
    def test_pending_task_past_due_date_is_overdue(self):
        """Test that pending task past due date is overdue."""
        task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            due_date="2025-06-10",
            created_at="2025-06-09T10:00:00",
            completed_at=None
        )
        
        is_overdue, error = is_task_overdue(task, "2025-06-12")
        assert error is None
        assert is_overdue is True
    
    def test_pending_task_before_due_date_not_overdue(self):
        """Test that pending task before due date is not overdue."""
        task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            due_date="2025-06-15",
            created_at="2025-06-11T10:00:00",
            completed_at=None
        )
        
        is_overdue, error = is_task_overdue(task, "2025-06-12")
        assert error is None
        assert is_overdue is False
    
    def test_invalid_date_format_returns_error(self):
        """Test that invalid date format returns error."""
        task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            due_date="invalid-date",
            created_at="2025-06-11T10:00:00",
            completed_at=None
        )
        
        is_overdue, error = is_task_overdue(task, "2025-06-12")
        assert is_overdue is False
        assert "date_parse_error" in error


class TestTaskOperations:
    """Test cases for task manipulation functions."""
    
    def test_mark_task_completed(self):
        """Test marking task as completed."""
        original_task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH,
            due_date="2025-12-31",
            created_at="2025-06-11T10:00:00",
            completed_at=None
        )
        
        completion_time = "2025-06-11T15:30:00"
        completed_task = mark_task_completed(original_task, completion_time)
        
        # Original task unchanged
        assert original_task.status == TaskStatus.PENDING
        assert original_task.completed_at is None
        
        # New task has updated fields
        assert completed_task.status == TaskStatus.COMPLETED
        assert completed_task.completed_at == completion_time
        assert completed_task.id == original_task.id
        assert completed_task.title == original_task.title
    
    def test_update_task_priority(self):
        """Test updating task priority."""
        original_task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            due_date=None,
            created_at="2025-06-11T10:00:00",
            completed_at=None
        )
        
        updated_task = update_task_priority(original_task, TaskPriority.HIGH)
        
        # Original task unchanged
        assert original_task.priority == TaskPriority.MEDIUM
        
        # New task has updated priority
        assert updated_task.priority == TaskPriority.HIGH
        assert updated_task.id == original_task.id
        assert updated_task.title == original_task.title
        assert updated_task.status == original_task.status
    
    def test_update_task_due_date(self):
        """Test updating task due date."""
        original_task = Task(
            id=1,
            title="Test task",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            due_date=None,
            created_at="2025-06-11T10:00:00",
            completed_at=None
        )
        
        new_due_date = "2025-12-31"
        updated_task = update_task_due_date(original_task, new_due_date)
        
        # Original task unchanged
        assert original_task.due_date is None
        
        # New task has updated due date
        assert updated_task.due_date == new_due_date
        assert updated_task.id == original_task.id
        assert updated_task.title == original_task.title
        assert updated_task.status == original_task.status
