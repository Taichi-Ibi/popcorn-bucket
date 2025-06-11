# CLI TODOアプリ要件定義書

**Project Name:** CLI TODO Manager  
**Created Date:** 2025/06/11  
**Last Updated:** 2025/06/11  
**Version:** 1.0

---

## 1. Project Overview

### 1.1 Background & Purpose
**Background:**
- 開発者がコマンドラインでタスク管理を効率的に行いたい
- GUIアプリケーションを開かずにターミナル内でタスクを管理したい
- シンプルで高速なタスク操作を求める開発者の需要
- Pygonスタイルを実践する具体的なプロジェクト例が必要

**Purpose:**
- コマンドラインインターフェースでタスクを管理するアプリケーションを提供
- 明示的エラーハンドリングと型安全性を重視したPygonスタイルの実装
- 開発者向けの直感的で高速なタスク管理ツールの実現

### 1.2 Scope
**Included:**
- タスクの作成、表示、更新、削除機能（CRUD操作）
- タスクの完了/未完了ステータス管理
- タスクの優先度設定
- タスクの期限設定
- タスクの一覧表示とフィルタリング
- JSONファイルベースのデータ永続化
- コマンドライン引数によるワンショット操作
- 設定ファイルによるカスタマイズ

**Excluded:**
- Web インターフェース
- データベース連携（第一フェーズでは対象外）
- 複数ユーザー対応
- タスク共有機能
- リアルタイム同期

### 1.3 Success Criteria
- タスク操作（作成・表示・更新・削除）が1秒以内に完了
- コマンドヘルプが分かりやすく、初回利用者が30分以内に基本操作を習得
- エラーメッセージが明確で、問題解決に必要な情報を提供
- Pygonスタイルガイドラインに100%準拠したコード品質

---

## 2. System Architecture

### 2.1 Core Components
| Component | Purpose | Technology | Dependencies |
|-----------|---------|------------|--------------|
| CLI Interface | コマンドライン引数解析・ユーザー操作 | Python argparse | None |
| Task Service | タスクビジネスロジック | Pygon Style Functions | models, validators |
| Task Repository | データ永続化・ファイル操作 | JSON File I/O | utils |
| Validators | 入力データ検証 | Pygon Validation Functions | models |
| Models | データ構造定義 | @dataclass(frozen=True) | None |
| Config | 設定管理 | JSON Configuration | utils |

---

## 3. Functional Requirements

### 3.1 User Stories
**Priority:** High/Medium/Low classification

#### 3.1.1 タスク作成機能
**Priority:** High  
**User Story:** 開発者として、新しいタスクを素早く作成して、後で参照したい。

**Acceptance Criteria:**
- [ ] コマンド `todo add "タスク名"` でタスクを作成できる
- [ ] タスクには自動的にユニークIDが割り当てられる
- [ ] 作成日時が自動的に記録される
- [ ] タスク名が空の場合は明確なエラーメッセージが表示される
- [ ] 作成成功時は「Task created: ID 1」のような確認メッセージが表示される

**Notes:**
- タスク名は最大100文字まで
- 特殊文字も含めて幅広い文字セット対応

#### 3.1.2 タスク一覧表示機能
**Priority:** High  
**User Story:** 開発者として、現在のタスク一覧を確認して、何をすべきか把握したい。

**Acceptance Criteria:**
- [ ] コマンド `todo list` で全タスクを表示できる
- [ ] ID、タスク名、ステータス、優先度、期限が表形式で表示される
- [ ] 完了済みタスクと未完了タスクが区別して表示される
- [ ] タスクが0件の場合は「No tasks found」メッセージが表示される
- [ ] `todo list --status pending` で未完了タスクのみ表示可能

#### 3.1.3 タスク完了機能
**Priority:** High  
**User Story:** 開発者として、完了したタスクをマークして進捗を把握したい。

**Acceptance Criteria:**
- [ ] コマンド `todo done <ID>` でタスクを完了状態にできる
- [ ] 存在しないIDを指定した場合は「Task not found」エラーが表示される
- [ ] 既に完了済みのタスクを指定した場合は「Task already completed」メッセージが表示される
- [ ] 完了時に完了日時が記録される

#### 3.1.4 タスク削除機能
**Priority:** Medium  
**User Story:** 開発者として、不要になったタスクを削除してリストを整理したい。

**Acceptance Criteria:**
- [ ] コマンド `todo delete <ID>` でタスクを削除できる
- [ ] 削除前に確認メッセージが表示される
- [ ] `--force` オプションで確認なしで削除可能
- [ ] 存在しないIDを指定した場合は明確なエラーメッセージが表示される

#### 3.1.5 タスク優先度設定機能
**Priority:** Medium  
**User Story:** 開発者として、タスクに優先度を設定して重要度を管理したい。

**Acceptance Criteria:**
- [ ] コマンド `todo priority <ID> <high|medium|low>` で優先度を設定できる
- [ ] 無効な優先度を指定した場合はエラーメッセージが表示される
- [ ] 優先度別でタスクをソート表示できる

#### 3.1.6 タスク期限設定機能
**Priority:** Medium  
**User Story:** 開発者として、タスクに期限を設定してデッドラインを管理したい。

**Acceptance Criteria:**
- [ ] コマンド `todo due <ID> <YYYY-MM-DD>` で期限を設定できる
- [ ] 無効な日付形式の場合はエラーメッセージが表示される
- [ ] 過去の日付を指定した場合は警告メッセージが表示される
- [ ] 期限切れタスクを `todo list --overdue` で表示可能

### 3.2 Screen & UI Requirements
#### 3.2.1 コマンドライン出力仕様
| 出力タイプ | 概要 | 優先度 | 備考 |
|-------------|----------|----------|-------|
| タスク一覧 | テーブル形式の表示 | High | 列幅自動調整 |
| エラーメッセージ | 明確で解決可能な情報 | High | Pygonエラー形式準拠 |
| 成功メッセージ | 操作完了の確認 | Medium | 簡潔で明確 |
| ヘルプ表示 | コマンド使用方法 | Medium | 例付きで分かりやすく |

#### 3.2.2 ユーザビリティ要件
- コマンド名は直感的で短い（`todo`）
- エラーメッセージには解決方法のヒントを含める
- 成功時と失敗時の出力を明確に区別する
- カラー出力対応（オプション）

### 3.3 External System Integration
#### 3.3.1 ファイルシステム統合
| 連携先 | 連携方法 | データ形式 | 頻度 |
|-------------|-------------------|-------------|-----------|
| JSONファイル | 直接ファイルI/O | JSON | リアルタイム |
| 設定ファイル | 起動時読み込み | JSON | 起動時 |

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
**Response Time:**
- コマンド実行: 1秒以内
- ファイル読み込み: 500ms以内
- タスク表示: 100ms以内（100件まで）

**Throughput:**
- 同時実行: 対応不要（単一ユーザー前提）
- 最大タスク数: 1000件まで対応

### 4.2 Availability Requirements
**データ整合性:**
- ファイル破損時の自動復旧機能
- バックアップファイルの自動作成

### 4.3 Security Requirements
**Data Protection:**
- ローカルファイルのみ使用（ネットワーク通信なし）
- ファイル権限の適切な設定（600）

### 4.4 Operations & Maintenance Requirements
**Monitoring:**
- エラーログの記録
- 操作履歴の記録（オプション）

**Backup:**
- データファイルの自動バックアップ
- 設定ファイルの復元機能

---

## 5. Technical Requirements (Pygon Style Compliant)

### 5.1 Development Environment
**Programming Language:**
- Python 3.11+ (Pygon style compliant)

**Frameworks & Libraries:**
- argparse (CLI argument parsing)
- json (data serialization)
- pathlib (file operations)
- datetime (date/time handling)
- typing (type annotations)

**Development Tools:**
- mypy (type checking)
- ruff (linting)
- pytest (testing)
- pre-commit (pre-commit checks)

### 5.2 Architecture Requirements
**Design Principles (Pygon Style Compliant):**
- Explicit error handling (return errors via return values)
- Comprehensive type annotations (leveraging TypeAlias)
- Simple data structures (@dataclass(frozen=True))
- Single responsibility functions
- Elimination of implicit behavior

**Directory Structure:**
```
cli-todo/
├── src/
│   ├── types/           # Result type aggregation
│   │   └── result_types.py
│   ├── models/          # @dataclass, Enum
│   │   └── task.py
│   ├── validators/      # Validation functions
│   │   └── task_validator.py
│   ├── services/        # Business logic functions
│   │   └── task_service.py
│   ├── repositories/    # Data access functions
│   │   └── task_repository.py
│   ├── protocols/       # Interface definitions
│   │   └── storage_protocol.py
│   ├── config/          # Configuration & constants
│   │   └── settings.py
│   ├── utils/           # Utility functions
│   │   └── file_utils.py
│   └── cli/             # CLI interface
│       └── main.py
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── fixtures/       # Test data
├── PYGON.md           # Style guide
├── README.md          # Project overview
└── TODO.md            # Tasks & AI collaboration records
```

### 5.3 Error Handling Strategy
**Basic Patterns:**
```python
# Single error (fail fast)
def validate_task_title(title: str) -> tuple[bool, str | None]:
    if not title.strip():
        return False, "validation_error: task title is required"
    if len(title) > 100:
        return False, "validation_error: task title too long (max 100 characters)"
    return True, None

# Multiple errors (UX-focused)
def validate_task_creation(task_data: dict) -> tuple[bool, list[str]]:
    errors = []
    if not task_data.get("title", "").strip():
        errors.append("validation_error: task title is required")
    if task_data.get("due_date") and not is_valid_date_format(task_data["due_date"]):
        errors.append("validation_error: invalid due date format (use YYYY-MM-DD)")
    return len(errors) == 0, errors
```

**Result Type Definitions:**
```python
from typing import TypeVar, TypeAlias

T = TypeVar('T')
Result: TypeAlias = tuple[T | None, str | None]
ValidationResult: TypeAlias = tuple[bool, str | None]
MultipleErrorResult: TypeAlias = tuple[bool, list[str]]
TaskResult: TypeAlias = Result[Task]
TaskListResult: TypeAlias = Result[list[Task]]
```

### 5.4 Database Requirements
**File Storage:**
- JSON format for data persistence
- Atomic write operations for data integrity
- Backup file creation before modification

---

## 6. Data Models

### 6.1 Entity List
| Entity Name | Overview | Key Attributes |
|-------------|----------|----------------|
| Task | タスク情報 | id, title, status, priority, due_date, created_at, completed_at |
| Priority | 優先度 | HIGH, MEDIUM, LOW |
| Status | ステータス | PENDING, COMPLETED |

### 6.2 Data Structure Examples (Pygon Style)
```python
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskPriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass(frozen=True)
class Task:
    id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    due_date: str | None
    created_at: str
    completed_at: str | None
    # No methods - data only

# Processing separated as functions
def is_task_overdue(task: Task, current_date: str) -> tuple[bool, str | None]:
    if not task.due_date:
        return False, None
    try:
        from datetime import datetime
        due = datetime.fromisoformat(task.due_date)
        current = datetime.fromisoformat(current_date)
        return due < current and task.status == TaskStatus.PENDING, None
    except ValueError as e:
        return False, f"date_parse_error: {e}"

def mark_task_completed(task: Task, completion_time: str) -> Task:
    return Task(
        id=task.id,
        title=task.title,
        status=TaskStatus.COMPLETED,
        priority=task.priority,
        due_date=task.due_date,
        created_at=task.created_at,
        completed_at=completion_time
    )
```

---

## 7. API Specifications

### 7.1 CLI Command List
| Command | Arguments | Overview | Input | Output |
|---------|-----------|----------|-------|--------|
| `todo add` | `<title>` | Create new task | Task title | Success/Error message |
| `todo list` | `[--status pending/completed]` | Show task list | Filter options | Task table |
| `todo done` | `<id>` | Mark task as completed | Task ID | Success/Error message |
| `todo delete` | `<id> [--force]` | Delete task | Task ID | Success/Error message |
| `todo priority` | `<id> <high/medium/low>` | Set task priority | Task ID, Priority | Success/Error message |
| `todo due` | `<id> <YYYY-MM-DD>` | Set due date | Task ID, Date | Success/Error message |

### 7.2 Error Response Specification
**Standard Error Format:**
```
Error: validation_error: task title is required
Usage: todo add "<title>"
Example: todo add "Fix bug in login system"
```

---

## 8. Test Requirements

### 8.1 Test Strategy
**Test Levels:**
- Unit Test: Individual function testing
- Integration Test: CLI command testing
- System Test: End-to-end workflow testing

### 8.2 Pygon Style Test Patterns
```python
class TestTaskValidation:
    def test_valid_title_returns_success(self):
        result, error = validate_task_title("Valid task title")
        assert error is None
        assert result is True
    
    def test_empty_title_returns_error(self):
        result, error = validate_task_title("")
        assert result is False
        assert "validation_error" in error

    def test_long_title_returns_specific_error(self):
        long_title = "a" * 101
        result, error = validate_task_title(long_title)
        assert result is False
        assert error == "validation_error: task title too long (max 100 characters)"

class TestTaskService:
    def test_create_task_with_valid_data_succeeds(self):
        task, error = create_task("New task", TaskPriority.HIGH)
        assert error is None
        assert task is not None
        assert task.title == "New task"
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.PENDING
```

### 8.3 Test Coverage
**Target Coverage:**
- Unit tests: 90% or higher
- Integration tests: 80% or higher

**Required Test Cases:**
- Happy path (success cases)
- Error path (error cases)
- Boundary value testing
- CLI argument parsing
- File I/O error handling

---

## 9. Development & Operations Environment

### 9.1 Environment Configuration
| Environment | Purpose | Notes |
|-------------|---------|-------|
| Development | Development & debugging | Local development with sample data |
| Test | Quality assurance | Automated testing environment |
| Production | User environment | End-user's local machine |

### 9.2 CI/CD Requirements
**Continuous Integration:**
- Automated test execution on commit
- Type checking (mypy)
- Linting (ruff)
- Test coverage measurement

**Distribution:**
- pip installable package
- Standalone executable (PyInstaller)
- Cross-platform compatibility (Windows, macOS, Linux)

---

## 10. Project Management

### 10.1 Development Process
**Development Methodology:**
- TDD (Test-Driven Development)
- AI-collaborative development
- Incremental delivery

**Pygon TDD Cycle:**
1. Create tests
2. Minimal implementation
3. Refactoring (function separation & responsibility isolation)

### 10.2 Quality Management
**Automated Quality Checks:**
- Pull request validation
- Automated testing
- Pygon style guide compliance checks

**Quality Standards:**
- [ ] Explicit return types for all functions
- [ ] Appropriate error handling
- [ ] Immutable dataclasses (frozen=True)
- [ ] Single responsibility principle adherence
- [ ] English comments only
- [ ] Test coverage targets achieved

---

## 11. Schedule

### 11.1 Milestones
| Phase | Start Date | End Date | Deliverable | Status |
|-------|------------|----------|-------------|--------|
| Requirements Definition | 2025/06/11 | 2025/06/11 | This document | Completed |
| Core Models & Types | 2025/06/12 | 2025/06/13 | Data structures, Result types | Planned |
| Basic CRUD Operations | 2025/06/14 | 2025/06/17 | Task creation, listing, completion | Planned |
| CLI Interface | 2025/06/18 | 2025/06/20 | Command parsing, help system | Planned |
| Advanced Features | 2025/06/21 | 2025/06/24 | Priority, due dates, filtering | Planned |
| Testing & Documentation | 2025/06/25 | 2025/06/27 | Test completion, user docs | Planned |

### 11.2 Risks and Mitigation
| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|-------------------|
| File corruption | High | Low | Implement atomic writes and backup |
| Performance issues with large datasets | Medium | Medium | Implement pagination and indexing |
| Cross-platform compatibility | Medium | Low | Thorough testing on all target platforms |

---

## 12. Documentation

### 12.1 Version History
| Version | Change Date | Changes |
|---------|-------------|---------|
| 1.0 | 2025/06/11 | Initial requirements specification |

---

## Appendix

### A. Reference Documents
- [PYGON.md](./PYGON.md) - Pygon style guide
- [requirements-specification-template.md](./requirements-specification-template.md) - Template used for this document

### B. Glossary
| Term | Definition |
|------|------------|
| Pygon | Python × Go fusion style. Explicit and understandable coding methodology |
| Result Type | `tuple[T | None, str | None]` pattern for explicit error handling |
| Frozen Dataclass | Immutable data class. Defined with `@dataclass(frozen=True)` |
| CLI | Command Line Interface |
| CRUD | Create, Read, Update, Delete operations |

### C. AI-Collaborative Development Guidelines
**AI Usage Scenarios:**
- Function signature generation for service layer
- Test case generation for validation functions
- Error message consistency checking
- Code review for Pygon style compliance

**AI Collaboration Points:**
- Leverage clear function signatures for effective AI assistance
- Utilize type information to enhance AI understanding
- Enable safe AI modifications through single responsibility functions

---

**About This Requirements Specification:**
This document defines the requirements for a CLI TODO application built using Pygon style principles. The application emphasizes explicit error handling, type safety, and maintainable architecture suitable for team development and AI collaboration.
