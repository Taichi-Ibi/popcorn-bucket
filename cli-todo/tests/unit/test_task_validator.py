import pytest
import sys
from pathlib import Path

# Add src to path for testing
src_path = Path(__file__).parent.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from validators.task_validator import (
    validate_task_title,
    validate_due_date_format,
    validate_priority_value,
    validate_task_creation_data,
    validate_task_id
)


class TestTaskTitleValidation:
    """Test cases for task title validation."""
    
    def test_valid_title_returns_success(self):
        """Test that valid title passes validation."""
        result, error = validate_task_title("Valid task title")
        assert error is None
        assert result is True
    
    def test_empty_title_returns_error(self):
        """Test that empty title returns validation error."""
        result, error = validate_task_title("")
        assert result is False
        assert "validation_error: task title is required" == error
    
    def test_whitespace_only_title_returns_error(self):
        """Test that whitespace-only title returns validation error."""
        result, error = validate_task_title("   ")
        assert result is False
        assert "validation_error: task title cannot be empty or whitespace only" == error
    
    def test_long_title_returns_specific_error(self):
        """Test that overly long title returns specific error."""
        long_title = "a" * 101
        result, error = validate_task_title(long_title)
        assert result is False
        assert "validation_error: task title too long (max 100 characters)" == error
    
    def test_max_length_title_passes(self):
        """Test that exactly 100 character title passes."""
        max_title = "a" * 100
        result, error = validate_task_title(max_title)
        assert error is None
        assert result is True


class TestDueDateValidation:
    """Test cases for due date validation."""
    
    def test_valid_date_format_returns_success(self):
        """Test that valid date format passes validation."""
        result, error = validate_due_date_format("2025-12-31")
        assert error is None
        assert result is True
    
    def test_invalid_date_format_returns_error(self):
        """Test that invalid date format returns error."""
        result, error = validate_due_date_format("31-12-2025")
        assert result is False
        assert "validation_error: invalid due date format (use YYYY-MM-DD)" == error
    
    def test_empty_date_returns_error(self):
        """Test that empty date returns error."""
        result, error = validate_due_date_format("")
        assert result is False
        assert "validation_error: due date is required" == error
    
    def test_invalid_date_values_return_error(self):
        """Test that invalid date values return error."""
        result, error = validate_due_date_format("2025-13-45")
        assert result is False
        assert "validation_error: invalid due date format (use YYYY-MM-DD)" == error


class TestPriorityValidation:
    """Test cases for priority validation."""
    
    def test_valid_priorities_return_success(self):
        """Test that all valid priorities pass validation."""
        valid_priorities = ["high", "medium", "low"]
        for priority in valid_priorities:
            result, error = validate_priority_value(priority)
            assert error is None, f"Priority {priority} should be valid"
            assert result is True
    
    def test_case_insensitive_priority_validation(self):
        """Test that priority validation is case insensitive."""
        # Test uppercase
        result, error = validate_priority_value("HIGH")
        assert result is True
        assert error is None
        
        # Test lowercase
        result, error = validate_priority_value("high")
        assert result is True
        assert error is None
        
        # Test mixed case
        result, error = validate_priority_value("High")
        assert result is True
        assert error is None
    
    def test_invalid_priority_returns_error(self):
        """Test that invalid priority returns error."""
        result, error = validate_priority_value("urgent")
        assert result is False
        assert "validation_error: invalid priority 'urgent'" in error
    
    def test_empty_priority_returns_error(self):
        """Test that empty priority returns error."""
        result, error = validate_priority_value("")
        assert result is False
        assert "validation_error: priority is required" == error


class TestTaskIdValidation:
    """Test cases for task ID validation."""
    
    def test_valid_positive_id_returns_success(self):
        """Test that valid positive integer ID passes validation."""
        result, error = validate_task_id("1")
        assert error is None
        assert result is True
    
    def test_zero_id_returns_error(self):
        """Test that zero ID returns error."""
        result, error = validate_task_id("0")
        assert result is False
        assert "validation_error: task ID must be a positive integer" == error
    
    def test_negative_id_returns_error(self):
        """Test that negative ID returns error."""
        result, error = validate_task_id("-1")
        assert result is False
        assert "validation_error: task ID must be a positive integer" == error
    
    def test_non_numeric_id_returns_error(self):
        """Test that non-numeric ID returns error."""
        result, error = validate_task_id("abc")
        assert result is False
        assert "validation_error: task ID must be a valid integer" == error
    
    def test_empty_id_returns_error(self):
        """Test that empty ID returns error."""
        result, error = validate_task_id("")
        assert result is False
        assert "validation_error: task ID is required" == error


class TestTaskCreationDataValidation:
    """Test cases for complete task creation data validation."""
    
    def test_valid_data_returns_success(self):
        """Test that valid task creation data passes validation."""
        task_data = {
            "title": "Valid task",
            "priority": "high",
            "due_date": "2025-12-31"
        }
        result, errors = validate_task_creation_data(task_data)
        assert len(errors) == 0
        assert result is True
    
    def test_missing_title_returns_error(self):
        """Test that missing title returns error."""
        task_data = {"priority": "high"}
        result, errors = validate_task_creation_data(task_data)
        assert result is False
        assert "validation_error: task title is required" in errors
    
    def test_multiple_errors_collected(self):
        """Test that multiple validation errors are collected."""
        task_data = {
            "title": "",
            "priority": "urgent",
            "due_date": "invalid-date"
        }
        result, errors = validate_task_creation_data(task_data)
        assert result is False
        assert len(errors) == 3
        assert any("task title is required" in error for error in errors)
        assert any("invalid priority" in error for error in errors)
        assert any("invalid due date format" in error for error in errors)
