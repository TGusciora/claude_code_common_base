# TDD Patterns in Python

Comprehensive guide to Test-Driven Development patterns using pytest.

## Overview

TDD is a discipline: write the test first, watch it fail, write minimal code to pass, then refactor. This guide covers practical patterns for effective TDD in Python.

## The TDD Cycle

```
    ┌─────────────────┐
    │                 │
    ▼                 │
  RED ──► GREEN ──► REFACTOR
    │                 │
    └─────────────────┘
```

### Step 1: RED - Write a Failing Test

```python
def test_user_can_change_password():
    user = User(email="test@example.com", password="old_password")

    user.change_password("new_password")

    assert user.verify_password("new_password")
    assert not user.verify_password("old_password")
```

Run it. Watch it fail. The failure message guides implementation.

### Step 2: GREEN - Minimal Passing Code

```python
class User:
    def __init__(self, email: str, password: str):
        self.email = email
        self._password = password

    def change_password(self, new_password: str) -> None:
        self._password = new_password

    def verify_password(self, password: str) -> bool:
        return self._password == password
```

### Step 3: REFACTOR - Improve the Code

```python
from dataclasses import dataclass, field
from passlib.hash import bcrypt

@dataclass
class User:
    email: str
    _password_hash: str = field(repr=False)

    @classmethod
    def create(cls, email: str, password: str) -> "User":
        return cls(email=email, _password_hash=bcrypt.hash(password))

    def change_password(self, new_password: str) -> None:
        self._password_hash = bcrypt.hash(new_password)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self._password_hash)
```

## Test Structure: Arrange-Act-Assert

Every test follows this pattern:

```python
def test_order_calculates_total_with_tax():
    # Arrange - Set up the test scenario
    order = Order()
    order.add_item(Product("Widget", price=Decimal("10.00")), quantity=2)
    tax_rate = Decimal("0.08")

    # Act - Perform the action being tested
    total = order.calculate_total(tax_rate=tax_rate)

    # Assert - Verify the expected outcome
    assert total == Decimal("21.60")
```

### Keep Each Section Focused

```python
# Bad - Muddled AAA
def test_user_creation():
    user = User("test@example.com")  # Arrange
    assert user.email == "test@example.com"  # Assert
    user.verify_email()  # Act
    assert user.is_verified  # Assert
    user.update_name("Test")  # Act
    assert user.name == "Test"  # Assert

# Good - Clear AAA
def test_user_stores_email():
    user = User("test@example.com")
    assert user.email == "test@example.com"

def test_user_can_verify_email():
    user = User("test@example.com")
    user.verify_email()
    assert user.is_verified

def test_user_can_update_name():
    user = User("test@example.com")
    user.update_name("Test")
    assert user.name == "Test"
```

## Test Naming Convention

```python
def test_<unit>_<scenario>_<expected_result>():
```

### Examples

```python
def test_calculate_discount_with_valid_coupon_returns_reduced_price():
    ...

def test_user_login_with_wrong_password_raises_auth_error():
    ...

def test_order_with_empty_cart_raises_validation_error():
    ...

def test_email_service_send_with_invalid_address_returns_failure():
    ...
```

## Pytest Fixtures

### Basic Fixtures

```python
import pytest

@pytest.fixture
def user():
    """Provide a basic test user."""
    return User(email="test@example.com", name="Test User")

@pytest.fixture
def admin_user():
    """Provide an admin user."""
    user = User(email="admin@example.com", name="Admin")
    user.role = Role.ADMIN
    return user

def test_admin_can_delete_users(admin_user, user):
    admin_user.delete_user(user)
    assert user.is_deleted
```

### Fixture Factories

```python
@pytest.fixture
def user_factory():
    """Factory for creating test users with custom attributes."""
    def _create_user(**kwargs):
        defaults = {
            "email": "test@example.com",
            "name": "Test User",
            "role": Role.USER
        }
        return User(**{**defaults, **kwargs})
    return _create_user

def test_multiple_users_with_different_roles(user_factory):
    admin = user_factory(role=Role.ADMIN)
    moderator = user_factory(email="mod@example.com", role=Role.MODERATOR)

    assert admin.can_manage(moderator)
```

### Scoped Fixtures

```python
@pytest.fixture(scope="session")
def database():
    """Create database once per test session."""
    db = create_test_database()
    yield db
    db.drop()

@pytest.fixture(scope="function")
def db_session(database):
    """Provide clean database session per test."""
    session = database.create_session()
    yield session
    session.rollback()
```

### Fixture Composition

```python
@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()

@pytest.fixture
def user_repository(db_session):
    return UserRepository(db_session)

@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)

def test_user_service_creates_user(user_service):
    user = user_service.create({"email": "new@example.com"})
    assert user.id is not None
```

## Mocking Patterns

### Mock External Dependencies

```python
from unittest.mock import Mock, patch

def test_order_service_sends_confirmation_email():
    # Arrange
    email_service = Mock()
    order_service = OrderService(email_service=email_service)
    order = Order(customer_email="test@example.com")

    # Act
    order_service.complete(order)

    # Assert
    email_service.send.assert_called_once_with(
        to="test@example.com",
        subject="Order Confirmation",
        body=ANY  # Match any body content
    )
```

### Mock Return Values

```python
def test_user_service_handles_database_error():
    db = Mock()
    db.save.side_effect = DatabaseError("Connection failed")
    service = UserService(db=db)

    with pytest.raises(ServiceError) as exc:
        service.create_user({"email": "test@example.com"})

    assert "Failed to create user" in str(exc.value)
```

### Patch Decorators

```python
@patch('myapp.services.email_client')
def test_sends_welcome_email(mock_email):
    service = UserService()
    service.create_user({"email": "test@example.com"})

    mock_email.send.assert_called_once()
```

### When to Mock

| Mock | Don't Mock |
|------|------------|
| External APIs | Your own business logic |
| Database (unit tests) | Simple data objects |
| File system | Pure functions |
| Time/randomness | In-memory collections |
| Email/SMS services | Value objects |

## Testing Exceptions

```python
def test_withdraw_with_insufficient_funds_raises_error():
    account = Account(balance=Decimal("100"))

    with pytest.raises(InsufficientFundsError) as exc:
        account.withdraw(Decimal("150"))

    assert exc.value.balance == Decimal("100")
    assert exc.value.requested == Decimal("150")


def test_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError, match="Invalid email format"):
        User(email="not-an-email")
```

## Parametrized Tests

```python
@pytest.mark.parametrize("amount,discount,expected", [
    (Decimal("100"), 10, Decimal("90")),
    (Decimal("100"), 0, Decimal("100")),
    (Decimal("100"), 100, Decimal("0")),
    (Decimal("50"), 25, Decimal("37.50")),
])
def test_calculate_discount(amount, discount, expected):
    result = calculate_discount(amount, percent=discount)
    assert result == expected


@pytest.mark.parametrize("input_email,is_valid", [
    ("user@example.com", True),
    ("user@sub.example.com", True),
    ("user+tag@example.com", True),
    ("invalid", False),
    ("@example.com", False),
    ("user@", False),
    ("", False),
])
def test_email_validation(input_email, is_valid):
    if is_valid:
        assert validate_email(input_email)
    else:
        with pytest.raises(ValidationError):
            validate_email(input_email)
```

## Test Organization

### File Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Fast, isolated tests
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/             # Tests with real dependencies
│   ├── test_database.py
│   └── test_api.py
└── e2e/                     # End-to-end tests
    └── test_user_journey.py
```

### conftest.py

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def app():
    """Create application instance."""
    return create_app(testing=True)

@pytest.fixture
def client(app):
    """Test client for the application."""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Headers with authentication token."""
    response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "password"
    })
    token = response.json["token"]
    return {"Authorization": f"Bearer {token}"}
```

## Test Doubles Summary

| Double | Purpose | Example |
|--------|---------|---------|
| **Dummy** | Fill parameter, never used | `None` or empty object |
| **Stub** | Return canned answers | `mock.return_value = X` |
| **Spy** | Record calls for verification | `mock.assert_called_with()` |
| **Mock** | Verify interactions | Full Mock object |
| **Fake** | Working implementation (simplified) | In-memory database |

## Common TDD Mistakes

### Mistake: Testing Implementation

```python
# Bad - Tests implementation details
def test_user_stores_password_in_hash_field():
    user = User(password="secret")
    assert user._password_hash.startswith("$2b$")

# Good - Tests behavior
def test_user_verifies_correct_password():
    user = User(password="secret")
    assert user.verify_password("secret")
```

### Mistake: Overly Complex Tests

```python
# Bad - Too much in one test
def test_user_journey():
    user = create_user()
    user.login()
    user.update_profile()
    user.create_order()
    user.cancel_order()
    user.logout()
    # What are we actually testing?

# Good - Focused tests
def test_user_can_login():
    ...

def test_user_can_update_profile():
    ...
```

### Mistake: Mock Everything

```python
# Bad - Mocking too much
def test_addition():
    calculator = Mock()
    calculator.add.return_value = 5
    assert calculator.add(2, 3) == 5  # Tests nothing!

# Good - Test real logic
def test_addition():
    calculator = Calculator()
    assert calculator.add(2, 3) == 5
```

## Test Coverage

```bash
# Run with coverage
pytest --cov=src --cov-report=html

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80
```

### Coverage Guidelines

- Aim for 80%+ coverage
- 100% coverage doesn't mean bug-free
- Cover edge cases, not just happy paths
- Don't write tests just to increase coverage

## See Also

- [Main Skill](../SKILL.md)
- [SOLID Principles](SOLID_PRINCIPLES.md)
- [Anti-Patterns](ANTI_PATTERNS.md)
