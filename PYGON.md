# Pygon宣言

**Python × Go = Pygon** - 明示的で理解しやすいコーディングスタイル  
**必要環境: Python 3.11以上**

## 課題と背景

### 現代開発の3つの課題
1. **生成AI時代**: AIが理解しにくい複雑な継承・暗黙的処理
2. **分散チーム**: 暗黙の了解に依存したコードの説明コスト
3. **マイクロサービス**: 例外処理では不十分なエラーハンドリング

### 従来Pythonの限界
```python
# ❌ Pythonic but unclear
def process(items):
    return [transform(x) for x in items if validate(x)]

def load_config():
    return json.load(open("config.json"))
```
**問題**: エラーケース不明、型情報不足、暗黙的処理

---

## 基本原則

### 1. 明示的エラーハンドリング
例外の代わりに戻り値でエラーを返す。

```python
def divide(a: int, b: int) -> tuple[float | None, str | None]:
    if b == 0:
        return None, "division by zero"
    return a / b, None

result, err = divide(10, 0)
if err:
    print(f"Error: {err}")
```

### 2. 徹底した型注釈
TypeAliasでResult型を統一し、単一/複数エラー戦略を使い分ける。

```python
from src.types.result_types import Result, ValidationResult, MultipleErrorResult

UserResult = Result[User]  # ドメイン固有型エイリアス

def find_user_by_email(users: list[User], email: str) -> UserResult:
    for user in users:
        if user.email == email:
            return user, None
    return None, "user not found"

# 単一エラー（fail fast）
def validate_email_format(email: str) -> ValidationResult:
    if not email:
        return False, "validation_error: email is required"
    if "@" not in email:
        return False, "validation_error: invalid email format"
    return True, None

# 複数エラー（UX重視）
def validate_user_registration(form_data: dict) -> MultipleErrorResult:
    errors = []
    if not form_data.get("name", "").strip():
        errors.append("validation_error: name is required")
    if "@" not in form_data.get("email", ""):
        errors.append("validation_error: invalid email format")
    return len(errors) == 0, errors
```

#### 集約化されたResult型
```python
# src/types/result_types.py
T = TypeVar('T')
Result: TypeAlias = tuple[T | None, str | None]
ValidationResult: TypeAlias = tuple[bool, str | None]  
MultipleErrorResult: TypeAlias = tuple[bool, list[str]]

# 使用例
from src.types.result_types import Result, ValidationResult, MultipleErrorResult
UserResult = Result[User]  # ドメイン固有型エイリアス
```

**エラー戦略の判断基準**
- **単一エラー**: ビジネスロジック、API呼び出し、ファイル操作、パイプライン処理
- **複数エラー**: フォームバリデーション、バッチ処理、設定ファイル検証、データ移行

### 3. シンプルなデータ構造
@dataclass(frozen=True)でデータのみ保持、処理は関数として分離。

```python
@dataclass(frozen=True)
class Task:
    id: int
    title: str
    status: Status
    created_at: str
    # メソッドなし - データのみ

# 処理は関数として分離
def is_task_overdue(task: Task, current_date: str) -> tuple[bool, str | None]:
    try:
        return datetime.fromisoformat(task.created_at) < datetime.fromisoformat(current_date), None
    except ValueError as e:
        return False, f"date_parse_error: {e}"

def with_status(task: Task, new_status: Status) -> Task:
    return Task(task.id, task.title, new_status, task.created_at)
```

### 4. 単一責任の関数
各関数は一つの明確な責任のみ。小さな関数を組み合わせて複雑な処理を実現。

```python
# ❌ 複数責任
def complete_task(task_id: int): # Performs data loading, searching, updating, and saving all in one

# ✅ 単一責任
def find_task_by_id(tasks: list[Task], task_id: int) -> tuple[Task | None, str | None]:
    for task in tasks:
        if task.id == task_id:
            return task, None
    return None, "task_not_found"

def update_task_status(task: Task, new_status: Status) -> Task:
    return Task(task.id, task.title, new_status, task.created_at)

# 組み合わせて実現
def complete_task_workflow(task_id: int) -> tuple[Task | None, str | None]:
    tasks, err = load_all_tasks()
    if err:
        return None, err
    
    task, err = find_task_by_id(tasks, task_id)
    if err:
        return None, err
    
    completed_task = update_task_status(task, Status.COMPLETED)
    # ... 保存処理
    return completed_task, None
```

### 5. 暗黙的動作の排除
「魔法的」な動作を避け、すべてを明示的に記述。

```python
# ❌ 暗黙的
def process_data(data):
    return transform(data)

# ✅ 明示的
def process_user_data(raw_data: dict[str, str]) -> tuple[User | None, str | None]:
    if "email" not in raw_data:
        return None, "email field is required"
    return User(int(raw_data.get("id", 0)), raw_data.get("name", ""), raw_data["email"]), None
```

## 実践上の重要な注意点

### バリデーション関数の必須化
```python
def validate_task_title(title: str) -> tuple[bool, str | None]:
    if not title:
        return False, "validation_error: title is required"
    if len(title.strip()) > 100:
        return False, "validation_error: title too long"
    return True, None

def create_task(title: str) -> tuple[Task | None, str | None]:
    is_valid, err = validate_task_title(title)
    if err:
        return None, err
    # 処理実行
```

### エラーメッセージの一貫性
```python
# ✅ 推奨: 「エラータイプ: 詳細」
"validation_error: email format is invalid"
"not_found_error: user not found"
"file_io_error: cannot read file"
```

### importの方針統一
**必須要件**: すべてのimport文は絶対importを使用する。相対importは使用しない。

```python
# ✅ 推奨: 絶対import
from src.types.result_types import Result, ValidationResult
from src.services.user_service import create_user
from src.models.user import User
from src.validators.email_validator import validate_email

# ❌ 非推奨: 相対import（ドット付き）
from ..types.result_types import Result, ValidationResult
from .user_service import create_user
from ...models.user import User

# ❌ 非推奨: 相対import（ドットなし）
from types.result_types import Result, ValidationResult
from services.user_service import create_user
from models.user import User
```

**理由**: 
- 生成AIツールでのimportエラー防止
- プロジェクト構造の明確化
- ファイル移動時のimport維持
- チーム開発での一貫性向上
- デバッグ時の依存関係把握の容易さ

### typesモジュール競合回避方針
**重要**: Pygonプロジェクトの`src/types/`モジュールとPython標準ライブラリの`types`モジュールの競合を防ぐ。

#### 基本原則
1. **絶対import必須**: 標準ライブラリの`types`との混同を防ぐため
2. **明示的な命名**: コードレビュー時に意図を明確にする
3. **import aliasの活用**: 必要に応じて別名を使用する

```python
# ✅ 推奨: Pygonの型定義
from src.types.result_types import Result, ValidationResult, PygonError
from src.types.result_types import create_validation_error

# ✅ 推奨: Python標準ライブラリのtypes
import types  # 標準ライブラリ
from types import SimpleNamespace, ModuleType

# ✅ 推奨: 明示的なalias（混同を避ける場合）
import types as python_types
from src.types import result_types as pygon_types

# ❌ 危険: 曖昧なimport
from types import *  # どのtypesか不明
import types  # この後に from src.types import * は混乱の元
```

#### 実装ガイドライン

**1. Pygon型定義の使用**
```python
# Result型を使用する場合
from src.types.result_types import Result, ValidationResult

UserResult = Result[User]  # ドメイン固有型エイリアス

def create_user(name: str, email: str) -> UserResult:
    # バリデーション処理
    pass
```

**2. Python標準types使用時の注意**
```python
# 標準ライブラリのtypesが必要な場合
import types
from types import SimpleNamespace, ModuleType

def create_dynamic_config(data: dict) -> types.SimpleNamespace:
    return types.SimpleNamespace(**data)

# 型チェックでの使用例
def is_module_type(obj: Any) -> bool:
    return isinstance(obj, types.ModuleType)
```

**3. 両方を使用する場合の分離**
```python
# 標準ライブラリのtypes
import types as python_types
from types import ModuleType

# Pygonのtypes
from src.types.result_types import Result, PygonError
from src.types.result_types import create_validation_error

def process_module_config(module: ModuleType, config_data: dict) -> Result[python_types.SimpleNamespace]:
    # バリデーション
    is_valid, error = validate_config_data(config_data)
    if not is_valid:
        return None, error
    
    # 動的設定オブジェクト作成
    config = python_types.SimpleNamespace(**config_data)
    return config, None

def validate_config_data(data: dict) -> tuple[bool, PygonError | None]:
    if not data:
        return False, create_validation_error("config data is required")
    return True, None
```

#### 命名規則とファイル構成

**推奨ディレクトリ構造**
```
src/
├── types/                    # Pygon型定義（必須）
│   ├── __init__.py          # 主要型のexport
│   ├── result_types.py      # Result, ValidationResult等
│   ├── domain_types.py      # ドメイン固有型（オプション）
│   └── protocol_types.py    # Protocol定義（オプション）
├── utils/
│   └── python_types_utils.py # 標準typesのユーティリティ
```

**ファイル命名の明確化**
- `result_types.py`: Pygonスタイルの戻り値型
- `domain_types.py`: ビジネスドメイン固有の型
- `protocol_types.py`: Protocol/インターフェース定義
- `python_types_utils.py`: 標準ライブラリtypesのヘルパー

#### エラー防止のためのチェックポイント

**コードレビュー時の確認項目**
```python
# ✅ 確認: このimportは意図通りか？
from types import SimpleNamespace  # 標準ライブラリ？
from src.types.result_types import Result  # Pygon型？

# ✅ 確認: 混在している場合、区別が明確か？
import types  # 標準ライブラリ
from src.types.result_types import Result  # Pygon型
# → 同じファイル内で両方使用する場合はaliasを検討

# ✅ 確認: 新規開発者が混同しないか？
# コメントやdocstringで意図を明記
def process_data(data: dict) -> Result[types.SimpleNamespace]:
    """Process configuration data.
    
    Uses Pygon Result type for error handling and Python's standard
    types.SimpleNamespace for dynamic configuration objects.
    """
    pass
```

**AIツール協調のための注意点**
- **import文の明示**: AIツールが正しい型を推論できるよう、明示的なimportを使用
- **コメントでの意図説明**: 混同しやすい箇所にはコメントで説明
- **型注釈の完全性**: 戻り値型を明確に指定し、AIツールの推論をサポート

この方針により、Pygonプロジェクトで型システムを安全かつ効率的に活用できる。

### コメントの言語統一
**必須要件**: ソースコード内のすべてのコメントは英語で記述する。

```python
# ✅ 推奨: 英語コメント
def validate_user_data(user_data: dict) -> ValidationResult:
    # Check if email field exists and is valid
    if "email" not in user_data:
        return False, "validation_error: email is required"
    
    # Validate email format using regex pattern
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', user_data["email"]):
        return False, "validation_error: invalid email format"
    
    return True, None

# ❌ 非推奨: 日本語コメント
def validate_user_data(user_data: dict) -> ValidationResult:
    # Check email field existence
    if "email" not in user_data:
        return False, "validation_error: email is required"
    
    return True, None
```

**理由**: 
- 国際的なチーム開発での統一性確保
- 生成AIツールとの協調性向上
- コードレビューの効率化
- 技術文書との整合性維持

### 例外処理の適切な粒度
```python
def load_config_file(path: str) -> tuple[dict | None, str | None]:
    try:
        content = Path(path).read_text(encoding="utf-8")
        return json.loads(content), None
    except FileNotFoundError:
        return None, "file_not_found_error: config file does not exist"
    except PermissionError:
        return None, "permission_error: cannot read config file"
    except json.JSONDecodeError as e:
        return None, f"json_parse_error: {e}"
```

---

## Pygonの拡張性・再利用性

### 組み合わせ重視の設計思想
```python
# ❌ 複雑な継承階層
class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    pass

# ✅ 組み合わせベース
@dataclass
class Animal:
    name: str
    species: str

@dataclass 
class MovementCapability:
    can_walk: bool
    can_fly: bool

@dataclass
class Dog:
    animal: Animal
    movement: MovementCapability

def make_dog_bark(dog: Dog) -> tuple[str, str | None]:
    if dog.animal.species != "dog":
        return "", "not a dog"
    return f"{dog.animal.name} says woof!", None
```

### プロトコル（Protocol）による柔軟性
```python
class Drawable(Protocol):
    def draw(self) -> tuple[str, str | None]:
        ...

def render_object(obj: Drawable) -> tuple[str, str | None]:
    return obj.draw()
```

---

## 高度なエラーハンドリング（リッチエラー対応）

デバッグに役立つ詳細な情報を提供するリッチエラーシステム。

```python
@dataclass(frozen=True)
class PygonError:
    error_type: str
    message: str
    context: dict[str, Any]
    timestamp: str
    source_location: str
    metadata: dict[str, Any]
    cause: Exception | None = None

    def to_string(self) -> str:
        return f"{self.error_type}: {self.message}"

# ヘルパー関数で作成
error = create_validation_error("email is required", 
                                context={"field": "email"},
                                metadata={"rule": "non_empty"})

# 後方互換性
LegacyResult: TypeAlias = tuple[T | None, str | None]       # 文字列ベース
Result: TypeAlias = tuple[T | None, PygonError | None]      # リッチエラーベース

def convert_to_legacy_error(rich_error: PygonError) -> str:
    return rich_error.to_string()
```

**利点**: 詳細なデバッグ情報、タイムスタンプ、例外チェーン、後方互換性、適応的出力

---

## 既存コードとの統合

### デコレータによるPygonスタイル変換
```python
def to_pygon(error_mapping: dict[type, str] | None = None):
    def decorator(func):
        def wrapper(*args, **kwargs) -> tuple[Any, str | None]:
            try:
                return func(*args, **kwargs), None
            except Exception as e:
                error_type = type(e).__name__.lower().replace('error', '_error')
                return None, f"{error_type}: {e}"
        return wrapper
    return decorator

# 使用例
@to_pygon({ValueError: "validation_error", FileNotFoundError: "file_not_found"})
def load_config_file(path: str) -> dict:
    return json.load(open(path))

config, err = load_config_file("settings.json")
```

---

## PygonにおけるOOP使い分け

### 判断基準
```
データ構造を定義？
├─ Yes → @dataclass ✅ (メソッドなし、データのみ)
└─ No
    └─ 設定や状態を保持？
        ├─ Yes → class ✅ (FileStorage等)
        └─ No → function ✅
```

```python
# ✅ データ構造
@dataclass
class User:
    id: int
    name: str
    email: str  # メソッドなし

# ✅ 状態保持
class FileStorage:
    def __init__(self, directory: str):
        self.directory = directory
    
    def save_data(self, data: dict) -> tuple[bool, str | None]:
        pass

# ✅ Protocol
class Storage(Protocol):
    def save(self, data: dict) -> tuple[bool, str | None]:
        ...

# ❌ 状態なしロジック → 関数を使用
def validate_email(email: str) -> tuple[bool, str | None]:
    if "@" in email:
        return True, None
    return False, "invalid email"
```

---

## Pygonプロジェクト構成

### 推奨ディレクトリ構造
```
project/
├── src/
│   ├── types/           # Result型の集約
│   ├── models/          # @dataclass, Enum
│   ├── validators/      # バリデーション関数
│   ├── services/        # ビジネスロジック関数
│   ├── repositories/    # データアクセス関数
│   ├── protocols/       # インターフェース定義
│   ├── config/          # 設定・定数
│   └── utils/           # ユーティリティ関数
├── tests/               # srcと同構造
│   ├── unit/            # 単体テスト
│   ├── integration/     # 結合テスト
│   └── fixtures/        # テストデータ
├── PYGON.md            # スタイルガイド（必須）
└── README.md           # プロジェクト概要
```

### プロジェクト文書の役割
- **PYGON.md**: チーム・AI共通の統一指針（必須）
- **README.md**: プロジェクト概要、Pygonスタイル言及
- **requirements-specification-template.md**: Pygonスタイル準拠の要件定義テンプレート

### TDD（テスト駆動開発）とPygon
**Pygon TDDサイクル**: テスト作成 → 最小実装 → リファクタリング（関数分割・責任分離）

```python
# 基本的なテストパターン
class TestEmailValidation:
    def test_valid_email_returns_success(self):
        result, error = validate_email_format("user@example.com")
        assert error is None
        assert result is True
    
    def test_invalid_email_returns_error(self):
        result, error = validate_email_format("invalid-email")
        assert result is False
        assert "validation_error" in error

# 推奨: 成功・失敗ケースをペアで作成、エラーメッセージ検証、モック活用
```

### 設計原則
- **関数中心分割**: services/(ビジネスロジック), validators/(バリデーション)
- **データと処理分離**: models/(データのみ), services/(処理関数)

---

## Pygonが目指すもの

### 核となる価値観
- **明示性 > 簡潔性**: わかりやすいコードを優先
- **予測可能性 > 柔軟性**: 期待通りの動作を優先  
- **チーム理解 > 個人効率**: みんなが読みやすいコードを優先
- **長期保守性 > 短期生産性**: 安全に変更できるコードを優先
- **人間-AI協調**: AIツールとの効果的な協力を重視

### 適用場面
**推奨**: チーム開発（3名以上）、本番環境、生成AIペアプログラミング、長期保守プロジェクト  
**従来Python**: 個人スクリプト、一回限り分析、小規模プロジェクト（100行未満）

### 段階的導入
1. プロジェクト構成（PYGON.md等） → 2. エラーハンドリング → 3. 型注釈 → 4. データ構造 → 5. 関数設計 → 6. AI協調最適化

---

**"明示的であることは、暗黙的であることよりも良い"** - The Zen of Python

Pygonは、AI時代の現代的開発環境でこの精神を実現する実践的アプローチ。**誰が読んでもわかる、誰が修正しても安全なコード**を目指す。

**Pygon Community**: GitHub `#pygon-style` | Python開発者のための明示的プログラミング