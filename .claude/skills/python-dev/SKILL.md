---
name: python-dev
description: Python development guide emphasizing KISS, YAGNI, SOLID principles with TDD-driven testing. Covers clean code patterns, pytest testing, type hints, and avoiding common anti-patterns.
---

# Python Development Guide

## Purpose

Guide Python development following first principles (KISS, YAGNI) and SOLID design, with test-driven development (TDD) as the primary workflow. This skill helps write clean, maintainable, well-tested Python code.

> **Core Principles:** See [CLAUDE.md](/CLAUDE.md) for KISS, YAGNI, SOLID definitions.
> This skill applies those principles specifically to Python development.

## When to Use This Skill

- Writing new Python functions, classes, or modules
- Refactoring existing Python code
- Writing or improving tests with pytest
- Reviewing Python code for quality
- Designing class hierarchies or module structure
- Debugging test failures

## Quick Reference

### First Principles

| Principle | Python Application |
|-----------|-------------------|
| KISS | One function = one task, avoid clever code |
| YAGNI | No speculative features, delete unused code |
| DRY | Extract common patterns, but not prematurely |

### TDD Cycle

```
RED → GREEN → REFACTOR
 ↑___________|
```

1. **RED**: Write failing test first
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Clean up, maintaining green

### Test Naming

```python
def test_<function>_<scenario>_<expected>():
    # test_calculate_total_with_discount_returns_reduced_price
```

### Type Hints

```python
def process_users(users: list[dict[str, Any]]) -> list[User]:
    """Always use type hints on function signatures."""
```

## KISS in Python

### Keep Functions Focused

**Bad - Does too much:**
```python
def process_order(order_data):
    # Validates
    if not order_data.get('items'):
        raise ValueError("No items")
    # Calculates
    total = sum(item['price'] * item['qty'] for item in order_data['items'])
    # Applies discount
    if order_data.get('coupon'):
        total *= 0.9
    # Saves to database
    db.orders.insert({'total': total, **order_data})
    # Sends email
    send_email(order_data['email'], f"Order confirmed: ${total}")
    return total
```

**Good - Single responsibility:**
```python
def validate_order(order_data: dict) -> None:
    """Validate order has required fields."""
    if not order_data.get('items'):
        raise ValueError("Order must have items")

def calculate_total(items: list[dict], coupon: str | None = None) -> Decimal:
    """Calculate order total with optional discount."""
    subtotal = sum(Decimal(item['price']) * item['qty'] for item in items)
    if coupon:
        return subtotal * Decimal('0.9')
    return subtotal

def process_order(order_data: dict) -> Order:
    """Orchestrate order processing."""
    validate_order(order_data)
    total = calculate_total(order_data['items'], order_data.get('coupon'))
    order = save_order(order_data, total)
    notify_customer(order)
    return order
```

### Avoid Clever Code

```python
# Bad - clever but unclear
result = [x for x in (y.strip() for y in data.split(',')) if x and x[0].isalpha()]

# Good - clear intent
def parse_csv_values(data: str) -> list[str]:
    """Extract valid alphabetic values from CSV string."""
    values = []
    for item in data.split(','):
        cleaned = item.strip()
        if cleaned and cleaned[0].isalpha():
            values.append(cleaned)
    return values
```

## YAGNI in Python

### Don't Add "Just In Case" Features

```python
# Bad - speculative flexibility
class DataProcessor:
    def __init__(self, format='json', compression=None, encryption=None,
                 retry_count=3, timeout=30, cache_enabled=True):
        # Most of these will never be used
        ...

# Good - only what's needed now
class DataProcessor:
    def __init__(self, format: str = 'json'):
        self.format = format
```

### Delete Unused Code

```python
# Bad - commented "just in case"
# def old_calculate_tax(amount):
#     return amount * 0.08

# Good - delete it, git has history
def calculate_tax(amount: Decimal) -> Decimal:
    return amount * Decimal('0.0825')
```

## SOLID Principles

### Quick Summary

| Principle | Meaning | Python Example |
|-----------|---------|----------------|
| S - Single Responsibility | One reason to change | One class per concern |
| O - Open/Closed | Extend, don't modify | Use inheritance/composition |
| L - Liskov Substitution | Subtypes are substitutable | Honor parent contracts |
| I - Interface Segregation | Small, focused interfaces | Use Protocol classes |
| D - Dependency Inversion | Depend on abstractions | Inject dependencies |

> For detailed patterns and examples, see [SOLID_PRINCIPLES.md](resources/SOLID_PRINCIPLES.md)

### Dependency Injection Example

```python
# Bad - hard dependency
class OrderService:
    def __init__(self):
        self.db = PostgresDatabase()  # Tight coupling
        self.emailer = SMTPEmailer()  # Hard to test

# Good - injected dependencies
class OrderService:
    def __init__(self, db: Database, emailer: Emailer):
        self.db = db
        self.emailer = emailer

# In production
service = OrderService(PostgresDatabase(), SMTPEmailer())

# In tests
service = OrderService(MockDatabase(), MockEmailer())
```

## TDD Workflow

### The Red-Green-Refactor Cycle

**Step 1: RED - Write a failing test**
```python
def test_calculate_discount_applies_percentage():
    result = calculate_discount(Decimal('100'), percent=10)
    assert result == Decimal('90')
```

**Step 2: GREEN - Write minimal passing code**
```python
def calculate_discount(amount: Decimal, percent: int) -> Decimal:
    return amount * (100 - percent) / 100
```

**Step 3: REFACTOR - Improve while staying green**
```python
def calculate_discount(amount: Decimal, percent: int) -> Decimal:
    """Apply percentage discount to amount."""
    discount_multiplier = Decimal(100 - percent) / Decimal(100)
    return amount * discount_multiplier
```

### Test Structure: Arrange-Act-Assert

```python
def test_user_service_creates_user_with_hashed_password():
    # Arrange
    service = UserService(hasher=MockHasher())
    user_data = {"email": "test@example.com", "password": "secret"}

    # Act
    user = service.create_user(user_data)

    # Assert
    assert user.email == "test@example.com"
    assert user.password_hash == "hashed:secret"
```

### Pytest Fixtures

```python
@pytest.fixture
def db_session():
    """Provide clean database session for each test."""
    session = create_test_session()
    yield session
    session.rollback()

@pytest.fixture
def user_factory(db_session):
    """Factory for creating test users."""
    def _create_user(**kwargs):
        defaults = {"email": "test@example.com", "name": "Test User"}
        return User(**{**defaults, **kwargs})
    return _create_user

def test_user_can_update_profile(db_session, user_factory):
    user = user_factory(name="Original")
    user.update_name("Updated")
    assert user.name == "Updated"
```

> For more TDD patterns, see [TDD_PATTERNS.md](resources/TDD_PATTERNS.md)

## Type Hints

### Always Type Function Signatures

```python
from typing import Any
from decimal import Decimal

def process_payment(
    amount: Decimal,
    currency: str,
    metadata: dict[str, Any] | None = None
) -> PaymentResult:
    """Process a payment transaction."""
    ...
```

### Use Modern Syntax (Python 3.10+)

```python
# Modern (3.10+)
def get_user(id: int) -> User | None:
    ...

def process(items: list[str]) -> dict[str, int]:
    ...

# Legacy (pre-3.10)
from typing import Optional, List, Dict

def get_user(id: int) -> Optional[User]:
    ...
```

### Protocol Classes for Duck Typing

```python
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict: ...

def save_record(record: Serializable) -> None:
    data = record.to_dict()
    db.insert(data)

# Any class with to_dict() method works
class User:
    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

save_record(User())  # Type checks!
```

## Common Patterns

### Factory Pattern

```python
class NotificationFactory:
    @staticmethod
    def create(type: str, **kwargs) -> Notification:
        match type:
            case "email":
                return EmailNotification(**kwargs)
            case "sms":
                return SMSNotification(**kwargs)
            case "push":
                return PushNotification(**kwargs)
            case _:
                raise ValueError(f"Unknown notification type: {type}")
```

### Context Manager

```python
from contextlib import contextmanager

@contextmanager
def transaction(db):
    """Database transaction context manager."""
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise

# Usage
with transaction(db) as conn:
    conn.execute("INSERT INTO users ...")
```

### Repository Pattern

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> User | None: ...

    @abstractmethod
    def save(self, user: User) -> None: ...

class PostgresUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    def get(self, id: int) -> User | None:
        return self.session.query(User).get(id)

    def save(self, user: User) -> None:
        self.session.add(user)
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| God Class | Does everything | Split by responsibility |
| Spaghetti Code | No structure | Extract functions/classes |
| Primitive Obsession | Overuse of str/int/dict | Create domain types |
| Test After | Writing tests after code | Practice TDD |
| Mock Everything | Brittle tests | Mock boundaries only |

> For detailed anti-patterns, see [ANTI_PATTERNS.md](resources/ANTI_PATTERNS.md)

## Project Structure

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── domain/          # Business logic
│       │   ├── models.py
│       │   └── services.py
│       ├── adapters/        # External interfaces
│       │   ├── database.py
│       │   └── api.py
│       └── utils/           # Shared utilities
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── unit/                # Fast, isolated tests
│   └── integration/         # Tests with real dependencies
├── pyproject.toml
└── README.md
```

## Resource Files

| File | Content | When to Use |
|------|---------|-------------|
| [SOLID_PRINCIPLES.md](resources/SOLID_PRINCIPLES.md) | Detailed SOLID patterns | Designing classes |
| [TDD_PATTERNS.md](resources/TDD_PATTERNS.md) | Testing patterns and fixtures | Writing tests |
| [ANTI_PATTERNS.md](resources/ANTI_PATTERNS.md) | Common mistakes | Code review |

## Quick Commands

| Command | Purpose |
|---------|---------|
| `/python-dev` | Invoke this skill manually |
| `pytest` | Run all tests |
| `pytest --cov` | Run with coverage |
| `ruff check` | Lint code |
| `ruff format` | Format code |
| `mypy src` | Type check |
