import subprocess
import sys
import tempfile
import json
from pathlib import Path


class TestCLIIntegration:
    """Integration tests for CLI commands."""
    
    def setup_method(self):
        """Set up test environment for each test."""
        # Create temporary data directory
        self.temp_dir = tempfile.mkdtemp()
        self.data_file = Path(self.temp_dir) / "tasks.json"
        
        # Set environment to use temporary data file
        self.original_cwd = Path.cwd()
        
    def teardown_method(self):
        """Clean up after each test."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def run_cli_command(self, args: list[str]) -> tuple[int, str, str]:
        """Run CLI command and return exit code, stdout, stderr."""
        # Run the CLI module
        cmd = [sys.executable, "-m", "src.cli.main"] + args
        
        result = subprocess.run(
            cmd,
            cwd=self.original_cwd / "cli-todo",
            capture_output=True,
            text=True,
            env={"PYTHONPATH": str(self.original_cwd / "cli-todo")}
        )
        
        return result.returncode, result.stdout, result.stderr
    
    def test_add_task_command(self):
        """Test adding a task via CLI."""
        exit_code, stdout, stderr = self.run_cli_command([
            "add", "Test task from CLI"
        ])
        
        assert exit_code == 0
        assert "Task created: ID 1" in stdout
        assert stderr == ""
    
    def test_add_task_with_priority_and_due_date(self):
        """Test adding task with priority and due date."""
        exit_code, stdout, stderr = self.run_cli_command([
            "add", "Important task",
            "--priority", "high",
            "--due-date", "2025-12-31"
        ])
        
        assert exit_code == 0
        assert "Task created: ID 1" in stdout
    
    def test_list_empty_tasks(self):
        """Test listing when no tasks exist."""
        exit_code, stdout, stderr = self.run_cli_command(["list"])
        
        assert exit_code == 0
        assert "No tasks found" in stdout
    
    def test_add_and_list_tasks(self):
        """Test adding tasks and then listing them."""
        # Add first task
        self.run_cli_command(["add", "First task"])
        
        # Add second task with priority
        self.run_cli_command([
            "add", "Second task",
            "--priority", "high"
        ])
        
        # List all tasks
        exit_code, stdout, stderr = self.run_cli_command(["list"])
        
        assert exit_code == 0
        assert "First task" in stdout
        assert "Second task" in stdout
        assert "pending" in stdout
        assert "high" in stdout
    
    def test_complete_task(self):
        """Test completing a task."""
        # Add a task first
        self.run_cli_command(["add", "Task to complete"])
        
        # Complete the task
        exit_code, stdout, stderr = self.run_cli_command(["done", "1"])
        
        assert exit_code == 0
        assert "Task 1 marked as completed" in stdout
        
        # Verify task is completed
        exit_code, stdout, stderr = self.run_cli_command(["list"])
        assert "completed" in stdout
    
    def test_delete_task(self):
        """Test deleting a task with force flag."""
        # Add a task first
        self.run_cli_command(["add", "Task to delete"])
        
        # Delete the task with force flag
        exit_code, stdout, stderr = self.run_cli_command([
            "delete", "1", "--force"
        ])
        
        assert exit_code == 0
        assert "Task 1 deleted" in stdout
        
        # Verify task is deleted
        exit_code, stdout, stderr = self.run_cli_command(["list"])
        assert "No tasks found" in stdout
    
    def test_set_task_priority(self):
        """Test setting task priority."""
        # Add a task first
        self.run_cli_command(["add", "Task for priority test"])
        
        # Set priority
        exit_code, stdout, stderr = self.run_cli_command([
            "priority", "1", "high"
        ])
        
        assert exit_code == 0
        assert "Task 1 priority set to high" in stdout
    
    def test_set_task_due_date(self):
        """Test setting task due date."""
        # Add a task first
        self.run_cli_command(["add", "Task for due date test"])
        
        # Set due date
        exit_code, stdout, stderr = self.run_cli_command([
            "due", "1", "2025-12-31"
        ])
        
        assert exit_code == 0
        assert "Task 1 due date set to 2025-12-31" in stdout
    
    def test_invalid_task_id_error(self):
        """Test error handling for invalid task ID."""
        exit_code, stdout, stderr = self.run_cli_command([
            "done", "999"
        ])
        
        assert exit_code == 1
        assert "Error: not_found_error: task with ID 999 not found" in stderr
    
    def test_invalid_priority_error(self):
        """Test error handling for invalid priority."""
        # Add a task first
        self.run_cli_command(["add", "Test task"])
        
        exit_code, stdout, stderr = self.run_cli_command([
            "priority", "1", "urgent"
        ])
        
        assert exit_code == 1
        assert "Error: validation_error: invalid priority 'urgent'" in stderr
    
    def test_invalid_date_format_error(self):
        """Test error handling for invalid date format."""
        # Add a task first
        self.run_cli_command(["add", "Test task"])
        
        exit_code, stdout, stderr = self.run_cli_command([
            "due", "1", "31-12-2025"
        ])
        
        assert exit_code == 1
        assert "Error: validation_error: invalid due date format" in stderr
    
    def test_help_command(self):
        """Test help command output."""
        exit_code, stdout, stderr = self.run_cli_command(["--help"])
        
        assert exit_code == 0
        assert "CLI TODO Manager" in stdout
        assert "add" in stdout
        assert "list" in stdout
        assert "done" in stdout
    
    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status."""
        # Add and complete some tasks
        self.run_cli_command(["add", "Pending task"])
        self.run_cli_command(["add", "Task to complete"])
        self.run_cli_command(["done", "2"])
        
        # List only pending tasks
        exit_code, stdout, stderr = self.run_cli_command([
            "list", "--status", "pending"
        ])
        
        assert exit_code == 0
        assert "Pending task" in stdout
        assert "Task to complete" not in stdout
        
        # List only completed tasks
        exit_code, stdout, stderr = self.run_cli_command([
            "list", "--status", "completed"
        ])
        
        assert exit_code == 0
        assert "Task to complete" in stdout
        assert "Pending task" not in stdout
