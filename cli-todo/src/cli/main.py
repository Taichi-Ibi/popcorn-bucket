import argparse
import sys
from typing import NoReturn
from ..services.task_service import create_task_service
from ..models.task import Task


def print_error(message: str) -> None:
    """Print error message to stderr."""
    print(f"Error: {message}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print success message to stdout."""
    print(message)


def format_task_table(tasks: list[Task]) -> str:
    """Format tasks as a table string.
    
    Args:
        tasks: List of tasks to format
        
    Returns:
        Formatted table string
    """
    if not tasks:
        return "No tasks found."
    
    # Calculate column widths
    id_width = max(len("ID"), max(len(str(task.id)) for task in tasks))
    title_width = max(len("Title"), max(len(task.title) for task in tasks))
    status_width = max(len("Status"), max(len(task.status.value) for task in tasks))
    priority_width = max(len("Priority"), max(len(task.priority.value) for task in tasks))
    due_width = max(len("Due Date"), max(len(task.due_date or "None") for task in tasks))
    
    # Create header
    header = f"{'ID':<{id_width}} | {'Title':<{title_width}} | {'Status':<{status_width}} | {'Priority':<{priority_width}} | {'Due Date':<{due_width}}"
    separator = "-" * len(header)
    
    # Create rows
    rows = []
    for task in tasks:
        due_date_str = task.due_date or "None"
        row = f"{task.id:<{id_width}} | {task.title:<{title_width}} | {task.status.value:<{status_width}} | {task.priority.value:<{priority_width}} | {due_date_str:<{due_width}}"
        rows.append(row)
    
    return "\n".join([header, separator] + rows)


def cmd_add(args: argparse.Namespace) -> None:
    """Handle 'add' command."""
    service = create_task_service()
    
    task, error = service.create_task(
        title=args.title,
        priority=args.priority,
        due_date=args.due_date
    )
    
    if error:
        print_error(error)
        if "validation_error" in error:
            print(f"Usage: todo add \"<title>\" [--priority <high|medium|low>] [--due-date YYYY-MM-DD]", file=sys.stderr)
            print(f"Example: todo add \"Fix bug in login system\" --priority high --due-date 2025-12-31", file=sys.stderr)
        sys.exit(1)
    
    print_success(f"Task created: ID {task.id}")


def cmd_list(args: argparse.Namespace) -> None:
    """Handle 'list' command."""
    service = create_task_service()
    
    if args.overdue:
        tasks, error = service.get_overdue_tasks()
    else:
        tasks, error = service.list_tasks(status_filter=args.status)
    
    if error:
        print_error(error)
        sys.exit(1)
    
    table = format_task_table(tasks)
    print(table)


def cmd_done(args: argparse.Namespace) -> None:
    """Handle 'done' command."""
    service = create_task_service()
    
    task, error = service.complete_task(args.id)
    
    if error:
        print_error(error)
        if "validation_error" in error:
            print(f"Usage: todo done <id>", file=sys.stderr)
            print(f"Example: todo done 1", file=sys.stderr)
        sys.exit(1)
    
    print_success(f"Task {task.id} marked as completed")


def cmd_delete(args: argparse.Namespace) -> None:
    """Handle 'delete' command."""
    service = create_task_service()
    
    # Confirmation unless --force is used
    if not args.force:
        response = input(f"Are you sure you want to delete task {args.id}? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Delete cancelled.")
            return
    
    success, error = service.delete_task(args.id)
    
    if error:
        print_error(error)
        if "validation_error" in error:
            print(f"Usage: todo delete <id> [--force]", file=sys.stderr)
            print(f"Example: todo delete 1", file=sys.stderr)
        sys.exit(1)
    
    print_success(f"Task {args.id} deleted")


def cmd_priority(args: argparse.Namespace) -> None:
    """Handle 'priority' command."""
    service = create_task_service()
    
    task, error = service.set_task_priority(args.id, args.priority)
    
    if error:
        print_error(error)
        if "validation_error" in error:
            print(f"Usage: todo priority <id> <high|medium|low>", file=sys.stderr)
            print(f"Example: todo priority 1 high", file=sys.stderr)
        sys.exit(1)
    
    print_success(f"Task {task.id} priority set to {task.priority.value}")


def cmd_due(args: argparse.Namespace) -> None:
    """Handle 'due' command."""
    service = create_task_service()
    
    task, error = service.set_task_due_date(args.id, args.due_date)
    
    if error:
        print_error(error)
        if "validation_error" in error:
            print(f"Usage: todo due <id> <YYYY-MM-DD>", file=sys.stderr)
            print(f"Example: todo due 1 2025-12-31", file=sys.stderr)
        sys.exit(1)
    
    print_success(f"Task {task.id} due date set to {task.due_date}")


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="CLI TODO Manager - A simple task management tool"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Create a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--priority", choices=["high", "medium", "low"], default="medium", help="Task priority (default: medium)")
    add_parser.add_argument("--due-date", help="Due date in YYYY-MM-DD format")
    add_parser.set_defaults(func=cmd_add)
    
    # List command
    list_parser = subparsers.add_parser("list", help="Show task list")
    list_parser.add_argument("--status", choices=["pending", "completed"], help="Filter by status")
    list_parser.add_argument("--overdue", action="store_true", help="Show only overdue tasks")
    list_parser.set_defaults(func=cmd_list)
    
    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as completed")
    done_parser.add_argument("id", help="Task ID")
    done_parser.set_defaults(func=cmd_done)
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", help="Task ID")
    delete_parser.add_argument("--force", action="store_true", help="Delete without confirmation")
    delete_parser.set_defaults(func=cmd_delete)
    
    # Priority command
    priority_parser = subparsers.add_parser("priority", help="Set task priority")
    priority_parser.add_argument("id", help="Task ID")
    priority_parser.add_argument("priority", choices=["high", "medium", "low"], help="Priority level")
    priority_parser.set_defaults(func=cmd_priority)
    
    # Due command
    due_parser = subparsers.add_parser("due", help="Set task due date")
    due_parser.add_argument("id", help="Task ID")
    due_parser.add_argument("due_date", help="Due date in YYYY-MM-DD format")
    due_parser.set_defaults(func=cmd_due)
    
    return parser


def main() -> NoReturn:
    """Main entry point for CLI application."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print_error(f"unexpected_error: {e}")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
