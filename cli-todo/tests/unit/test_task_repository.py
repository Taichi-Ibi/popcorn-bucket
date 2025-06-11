import pytest
import tempfile
import json
import sys
from pathlib import Path

# Add src to path for testing
src_path = Path(__file__).parent.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from repositories.task_repository import JsonTaskRepository
from models.task import Task, TaskStatus, TaskPriority


class TestJsonTaskRepository:
    """Test cases for JSON task repository."""
    
    @pytest.fixture
    def temp_data_file(self):
        """Create temporary data file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)
        Path(f"{temp_path}.backup").unlink(missing_ok=True)
    
    @pytest.fixture
    def repository(self, temp_data_file):
        """Create repository instance with temporary file."""
        return JsonTaskRepository(temp_data_file)
    
    @pytest.fixture
    def sample_tasks(self):
        """Create sample tasks for testing."""
        return [
            Task(
                id=1,
                title="First task",
                status=TaskStatus.PENDING,
                priority=TaskPriority.HIGH,
                due_date="2025-12-31",
                created_at="2025-06-11T10:00:00",
                completed_at=None
            ),
            Task(
                id=2,
                title="Second task",
                status=TaskStatus.COMPLETED,
                priority=TaskPriority.MEDIUM,
                due_date=None,
                created_at="2025-06-10T09:00:00",
                completed_at="2025-06-11T14:00:00"
            )
        ]
    
    def test_save_and_load_tasks(self, repository, sample_tasks):
        """Test saving and loading tasks."""
        # Save tasks
        success, error = repository.save_tasks(sample_tasks)
        assert error is None
        assert success is True
        
        # Load tasks
        loaded_tasks, error = repository.load_tasks()
        assert error is None
        assert len(loaded_tasks) == 2
        
        # Verify first task
        assert loaded_tasks[0].id == 1
        assert loaded_tasks[0].title == "First task"
        assert loaded_tasks[0].status == TaskStatus.PENDING
        assert loaded_tasks[0].priority == TaskPriority.HIGH
        assert loaded_tasks[0].due_date == "2025-12-31"
        
        # Verify second task
        assert loaded_tasks[1].id == 2
        assert loaded_tasks[1].title == "Second task"
        assert loaded_tasks[1].status == TaskStatus.COMPLETED
        assert loaded_tasks[1].priority == TaskPriority.MEDIUM
        assert loaded_tasks[1].due_date is None
    
    def test_load_nonexistent_file_returns_empty_list(self, repository):
        """Test loading from nonexistent file returns empty list."""
        tasks, error = repository.load_tasks()
        assert error is None
        assert tasks == []
    
    def test_save_empty_task_list(self, repository):
        """Test saving empty task list."""
        success, error = repository.save_tasks([])
        assert error is None
        assert success is True
        
        tasks, error = repository.load_tasks()
        assert error is None
        assert tasks == []
    
    def test_backup_creation(self, repository, sample_tasks, temp_data_file):
        """Test that backup is created when saving."""
        # Save initial data
        success, error = repository.save_tasks(sample_tasks)
        assert error is None
        
        # Modify and save again (should create backup)
        modified_tasks = sample_tasks + [
            Task(
                id=3,
                title="Third task",
                status=TaskStatus.PENDING,
                priority=TaskPriority.LOW,
                due_date=None,
                created_at="2025-06-11T11:00:00",
                completed_at=None
            )
        ]
        
        success, error = repository.save_tasks(modified_tasks)
        assert error is None
        
        # Check backup file exists
        backup_file = Path(f"{temp_data_file}.backup")
        assert backup_file.exists()
        
        # Verify backup contains original data
        with backup_file.open('r') as f:
            backup_data = json.load(f)
        assert len(backup_data) == 2
    
    def test_atomic_write_operation(self, repository, sample_tasks, temp_data_file):
        """Test that write operation is atomic."""
        # Save initial data
        success, error = repository.save_tasks(sample_tasks)
        assert error is None
        
        # Verify no temporary file remains
        temp_file = Path(temp_data_file).with_suffix('.tmp')
        assert not temp_file.exists()
        
        # Verify main file exists and is valid
        main_file = Path(temp_data_file)
        assert main_file.exists()
        
        with main_file.open('r') as f:
            data = json.load(f)
        assert len(data) == 2
    
    def test_invalid_json_data_handling(self, temp_data_file):
        """Test handling of invalid JSON data."""
        # Write invalid JSON to file
        with open(temp_data_file, 'w') as f:
            f.write("invalid json content")
        
        repository = JsonTaskRepository(temp_data_file)
        tasks, error = repository.load_tasks()
        
        assert tasks is None
        assert "json_parse_error" in error
    
    def test_corrupted_task_data_handling(self, temp_data_file):
        """Test handling of corrupted task data."""
        # Write valid JSON but invalid task structure
        corrupted_data = [
            {
                "id": 1,
                "title": "Task without status",
                # Missing required fields
            }
        ]
        
        with open(temp_data_file, 'w') as f:
            json.dump(corrupted_data, f)
        
        repository = JsonTaskRepository(temp_data_file)
        tasks, error = repository.load_tasks()
        
        assert tasks is None
        assert "data_format_error" in error
