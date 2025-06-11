from typing import TypeVar, TypeAlias

# Core Result types for explicit error handling
T = TypeVar('T')
Result: TypeAlias = tuple[T | None, str | None]
ValidationResult: TypeAlias = tuple[bool, str | None]
MultipleErrorResult: TypeAlias = tuple[bool, list[str]]

# Domain-specific type aliases for better clarity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.task import Task

TaskResult: TypeAlias = Result['Task']
TaskListResult: TypeAlias = Result[list['Task']]
