# SOLID Principles in Python

Detailed guide to applying SOLID principles in Python development.

## Overview

SOLID principles guide object-oriented design toward maintainable, flexible code. In Python, these principles adapt to the language's dynamic nature while preserving their core benefits.

## S - Single Responsibility Principle

**"A class should have only one reason to change."**

### The Problem

```python
# Bad - Multiple responsibilities
class UserManager:
    def create_user(self, data: dict) -> User:
        # Validates data
        if not data.get('email'):
            raise ValueError("Email required")
        if not self._is_valid_email(data['email']):
            raise ValueError("Invalid email")

        # Creates user
        user = User(**data)

        # Saves to database
        self.db.insert('users', user.to_dict())

        # Sends welcome email
        self.email_client.send(
            to=user.email,
            subject="Welcome!",
            body=self._render_welcome_template(user)
        )

        # Logs activity
        self.logger.info(f"Created user: {user.id}")

        return user

    def _is_valid_email(self, email: str) -> bool: ...
    def _render_welcome_template(self, user: User) -> str: ...
```

This class changes for: validation rules, database schema, email templates, logging format.

### The Solution

```python
# Good - Separated responsibilities
class UserValidator:
    """Validates user data."""

    def validate(self, data: dict) -> None:
        if not data.get('email'):
            raise ValidationError("Email required")
        if not self._is_valid_email(data['email']):
            raise ValidationError("Invalid email format")

    def _is_valid_email(self, email: str) -> bool:
        return '@' in email and '.' in email.split('@')[1]


class UserRepository:
    """Persists user data."""

    def __init__(self, db: Database):
        self.db = db

    def save(self, user: User) -> None:
        self.db.insert('users', user.to_dict())

    def find_by_email(self, email: str) -> User | None:
        data = self.db.find_one('users', {'email': email})
        return User(**data) if data else None


class WelcomeEmailSender:
    """Sends welcome emails to new users."""

    def __init__(self, email_client: EmailClient):
        self.email_client = email_client

    def send(self, user: User) -> None:
        self.email_client.send(
            to=user.email,
            subject="Welcome!",
            body=self._render_template(user)
        )

    def _render_template(self, user: User) -> str:
        return f"Welcome, {user.name}!"


class UserService:
    """Orchestrates user creation."""

    def __init__(
        self,
        validator: UserValidator,
        repository: UserRepository,
        welcome_sender: WelcomeEmailSender
    ):
        self.validator = validator
        self.repository = repository
        self.welcome_sender = welcome_sender

    def create_user(self, data: dict) -> User:
        self.validator.validate(data)
        user = User(**data)
        self.repository.save(user)
        self.welcome_sender.send(user)
        return user
```

### When to Split

Ask: "What reasons might this class change?"

- If more than one → split
- If responsibilities are cohesive → keep together

## O - Open/Closed Principle

**"Software entities should be open for extension, closed for modification."**

### The Problem

```python
# Bad - Must modify to extend
class PaymentProcessor:
    def process(self, payment_type: str, amount: Decimal) -> Result:
        if payment_type == "credit_card":
            return self._process_credit_card(amount)
        elif payment_type == "paypal":
            return self._process_paypal(amount)
        elif payment_type == "crypto":
            return self._process_crypto(amount)
        # Adding new payment type requires modifying this class
        else:
            raise ValueError(f"Unknown payment type: {payment_type}")
```

### The Solution

```python
from abc import ABC, abstractmethod

# Good - Extend without modifying
class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: Decimal) -> Result:
        """Process a payment of the given amount."""
        pass


class CreditCardPayment(PaymentMethod):
    def process(self, amount: Decimal) -> Result:
        # Credit card specific logic
        return Result(success=True, transaction_id="cc_123")


class PayPalPayment(PaymentMethod):
    def process(self, amount: Decimal) -> Result:
        # PayPal specific logic
        return Result(success=True, transaction_id="pp_456")


class CryptoPayment(PaymentMethod):
    def process(self, amount: Decimal) -> Result:
        # Crypto specific logic
        return Result(success=True, transaction_id="crypto_789")


class PaymentProcessor:
    def process(self, method: PaymentMethod, amount: Decimal) -> Result:
        return method.process(amount)


# Adding new payment type - no modification needed
class ApplePayPayment(PaymentMethod):
    def process(self, amount: Decimal) -> Result:
        return Result(success=True, transaction_id="apple_101")
```

### Using Protocols (Duck Typing)

```python
from typing import Protocol

class Processor(Protocol):
    def process(self, amount: Decimal) -> Result: ...

def handle_payment(processor: Processor, amount: Decimal) -> Result:
    return processor.process(amount)

# Any object with process() method works
handle_payment(CreditCardPayment(), Decimal('100'))
```

## L - Liskov Substitution Principle

**"Subtypes must be substitutable for their base types."**

### The Problem

```python
# Bad - Violates LSP
class Bird:
    def fly(self) -> None:
        print("Flying!")

class Penguin(Bird):
    def fly(self) -> None:
        raise NotImplementedError("Penguins can't fly!")  # Breaks substitution!
```

Code expecting `Bird` will break with `Penguin`.

### The Solution

```python
# Good - Proper hierarchy
class Bird(ABC):
    @abstractmethod
    def move(self) -> None:
        pass


class FlyingBird(Bird):
    def move(self) -> None:
        self.fly()

    def fly(self) -> None:
        print("Flying!")


class SwimmingBird(Bird):
    def move(self) -> None:
        self.swim()

    def swim(self) -> None:
        print("Swimming!")


class Sparrow(FlyingBird):
    pass


class Penguin(SwimmingBird):
    pass


# Both work correctly
def make_bird_move(bird: Bird) -> None:
    bird.move()  # Works for all birds

make_bird_move(Sparrow())   # Flying!
make_bird_move(Penguin())   # Swimming!
```

### LSP Checklist

Subclasses must:
- [ ] Accept same or broader input types
- [ ] Return same or narrower output types
- [ ] Not strengthen preconditions
- [ ] Not weaken postconditions
- [ ] Preserve invariants of the base class

## I - Interface Segregation Principle

**"Clients should not depend on interfaces they don't use."**

### The Problem

```python
# Bad - Fat interface
class Worker(ABC):
    @abstractmethod
    def work(self) -> None: ...

    @abstractmethod
    def eat(self) -> None: ...

    @abstractmethod
    def sleep(self) -> None: ...

    @abstractmethod
    def take_break(self) -> None: ...


class Robot(Worker):
    def work(self) -> None:
        print("Working...")

    def eat(self) -> None:
        raise NotImplementedError()  # Robots don't eat!

    def sleep(self) -> None:
        raise NotImplementedError()  # Robots don't sleep!

    def take_break(self) -> None:
        raise NotImplementedError()
```

### The Solution

```python
# Good - Segregated interfaces
class Workable(Protocol):
    def work(self) -> None: ...


class Eatable(Protocol):
    def eat(self) -> None: ...


class Sleepable(Protocol):
    def sleep(self) -> None: ...


class Human:
    def work(self) -> None:
        print("Working...")

    def eat(self) -> None:
        print("Eating...")

    def sleep(self) -> None:
        print("Sleeping...")


class Robot:
    def work(self) -> None:
        print("Working...")


def assign_work(worker: Workable) -> None:
    worker.work()

def schedule_lunch(eater: Eatable) -> None:
    eater.eat()


# Both work where appropriate
assign_work(Human())  # OK
assign_work(Robot())  # OK

schedule_lunch(Human())  # OK
# schedule_lunch(Robot())  # Type error - Robot isn't Eatable
```

### Python Protocols

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    def to_json(self) -> str: ...

class User:
    def to_json(self) -> str:
        return json.dumps({"id": self.id})

# Runtime check
if isinstance(user, Serializable):
    print(user.to_json())
```

## D - Dependency Inversion Principle

**"Depend on abstractions, not concretions."**

### The Problem

```python
# Bad - Depends on concrete implementation
class OrderService:
    def __init__(self):
        self.db = PostgresDatabase()  # Concrete dependency
        self.emailer = SMTPEmailer()  # Concrete dependency

    def create_order(self, data: dict) -> Order:
        order = Order(**data)
        self.db.save(order)           # Tightly coupled
        self.emailer.send_confirmation(order)
        return order
```

Can't test without real database and email server.

### The Solution

```python
# Good - Depends on abstractions
class Database(Protocol):
    def save(self, entity: Any) -> None: ...
    def find(self, id: int) -> Any | None: ...


class Emailer(Protocol):
    def send(self, to: str, subject: str, body: str) -> None: ...


class OrderService:
    def __init__(self, db: Database, emailer: Emailer):
        self.db = db
        self.emailer = emailer

    def create_order(self, data: dict) -> Order:
        order = Order(**data)
        self.db.save(order)
        self.emailer.send(
            to=order.customer_email,
            subject="Order Confirmation",
            body=f"Order {order.id} confirmed"
        )
        return order


# Production
service = OrderService(
    db=PostgresDatabase(connection_string),
    emailer=SMTPEmailer(smtp_config)
)

# Testing
class MockDatabase:
    def __init__(self):
        self.saved = []

    def save(self, entity: Any) -> None:
        self.saved.append(entity)

    def find(self, id: int) -> Any | None:
        return next((e for e in self.saved if e.id == id), None)


class MockEmailer:
    def __init__(self):
        self.sent = []

    def send(self, to: str, subject: str, body: str) -> None:
        self.sent.append({"to": to, "subject": subject, "body": body})


def test_create_order_saves_and_emails():
    db = MockDatabase()
    emailer = MockEmailer()
    service = OrderService(db, emailer)

    order = service.create_order({"customer_email": "test@example.com"})

    assert len(db.saved) == 1
    assert len(emailer.sent) == 1
    assert emailer.sent[0]["to"] == "test@example.com"
```

### Dependency Injection Container

```python
from dataclasses import dataclass

@dataclass
class Container:
    """Simple dependency injection container."""
    db: Database
    emailer: Emailer
    user_repo: UserRepository
    order_service: OrderService

    @classmethod
    def create_production(cls) -> "Container":
        db = PostgresDatabase(os.environ["DATABASE_URL"])
        emailer = SMTPEmailer(os.environ["SMTP_URL"])
        user_repo = PostgresUserRepository(db)
        order_service = OrderService(db, emailer)
        return cls(db, emailer, user_repo, order_service)

    @classmethod
    def create_test(cls) -> "Container":
        db = MockDatabase()
        emailer = MockEmailer()
        user_repo = MockUserRepository()
        order_service = OrderService(db, emailer)
        return cls(db, emailer, user_repo, order_service)
```

## Summary

| Principle | Key Question | Indicator |
|-----------|--------------|-----------|
| SRP | How many reasons to change? | >1 = split |
| OCP | Can I extend without modifying? | No = refactor |
| LSP | Can subtype replace parent? | No = fix hierarchy |
| ISP | Does client use all methods? | No = segregate |
| DIP | Am I depending on concrete? | Yes = abstract |

## See Also

- [Main Skill](../SKILL.md)
- [TDD Patterns](TDD_PATTERNS.md)
- [Anti-Patterns](ANTI_PATTERNS.md)
