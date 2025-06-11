# CLI TODO Manager

A command-line task management tool built with **Pygon** style - explicit, maintainable, and AI-collaborative Python code.

## 🐍 Pygon Style

This project follows **Pygon** coding principles for clear, explicit, and maintainable code:

- Explicit error handling via return values
- Comprehensive type annotations
- Immutable dataclasses with no methods
- Single-responsibility functions
- English comments only

> 📋 See [../PYGON.md](../PYGON.md) for complete style guidelines.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+

### Installation
```bash
cd cli-todo
pip install -r requirements.txt
```

### Basic Usage
```bash
# Create a new task
python -m src.cli.main add "Fix bug in login system"

# List all tasks
python -m src.cli.main list

# Mark task as completed
python -m src.cli.main done 1

# Set task priority
python -m src.cli.main priority 1 high

# Set due date
python -m src.cli.main due 1 2025-12-31

# Delete a task
python -m src.cli.main delete 1
```

## 📁 Project Structure

```
cli-todo/
├── src/
│   ├── types/           # Result type definitions
│   ├── models/          # Data structures (@dataclass, Enum)
│   ├── validators/      # Validation functions
│   ├── services/        # Business logic functions
│   ├── repositories/    # Data access functions
│   ├── protocols/       # Interface definitions
│   ├── config/          # Configuration & constants
│   ├── utils/           # Utility functions
│   └── cli/             # CLI interface
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── fixtures/       # Test data
├── data/               # Task data storage
├── README.md           # This file
└── requirements.txt    # Dependencies
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test category
python -m pytest tests/unit/
python -m pytest tests/integration/
```

## 📝 Features

- ✅ Create, list, complete, and delete tasks
- ✅ Set task priorities (high, medium, low)
- ✅ Set due dates with overdue detection
- ✅ Filter tasks by status
- ✅ JSON-based data persistence
- ✅ Comprehensive error handling
- ✅ Type-safe implementation

## 🤖 AI Collaboration

This project is designed for **human-AI collaborative development**:

- Clear function signatures for effective AI assistance
- Explicit error patterns for consistency
- Single-responsibility functions for safe AI modifications
- Comprehensive type annotations for AI understanding

---

**Built with ❤️ using Pygon style**
