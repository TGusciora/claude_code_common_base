# Python Anti-Patterns

Common mistakes in Python development and how to avoid them.

## Code Organization Anti-Patterns

### God Class

**Problem:** A class that knows too much or does too much.

```python
# Bad - God class
class ApplicationManager:
    def __init__(self):
        self.users = []
        self.orders = []
        self.products = []
        self.db = Database()
        self.email = EmailClient()
        self.cache = Cache()

    def create_user(self, data): ...
    def authenticate_user(self, email, password): ...
    def reset_password(self, email): ...
    def create_order(self, user_id, items): ...
    def process_payment(self, order_id): ...
    def ship_order(self, order_id): ...
    def add_product(self, data): ...
    def update_inventory(self, product_id, quantity): ...
    def generate_report(self, type): ...
    def send_notification(self, user_id, message): ...
    # ... 50 more methods
```

**Solution:** Split by responsibility.

```python
# Good - Focused classes
class UserService:
    def create(self, data): ...
    def authenticate(self, email, password): ...

class OrderService:
    def create(self, user_id, items): ...
    def process_payment(self, order_id): ...

class InventoryService:
    def update(self, product_id, quantity): ...
```

---

### Spaghetti Code

**Problem:** Code with no clear structure, deeply nested, hard to follow.

```python
# Bad - Spaghetti
def process_data(data):
    result = []
    for item in data:
        if item.get('type') == 'A':
            if item.get('status') == 'active':
                if item.get('value') > 0:
                    for sub in item.get('subs', []):
                        if sub.get('enabled'):
                            if sub.get('count') > 10:
                                result.append({
                                    'id': item['id'],
                                    'sub_id': sub['id'],
                                    'value': item['value'] * sub['count']
                                })
    return result
```

**Solution:** Extract functions, use early returns.

```python
# Good - Clear structure
def process_data(data: list[dict]) -> list[dict]:
    return [
        result
        for item in data
        if is_processable(item)
        for result in process_item(item)
    ]

def is_processable(item: dict) -> bool:
    return (
        item.get('type') == 'A'
        and item.get('status') == 'active'
        and item.get('value', 0) > 0
    )

def process_item(item: dict) -> list[dict]:
    return [
        create_result(item, sub)
        for sub in item.get('subs', [])
        if is_enabled_with_sufficient_count(sub)
    ]

def is_enabled_with_sufficient_count(sub: dict) -> bool:
    return sub.get('enabled') and sub.get('count', 0) > 10

def create_result(item: dict, sub: dict) -> dict:
    return {
        'id': item['id'],
        'sub_id': sub['id'],
        'value': item['value'] * sub['count']
    }
```

---

### Primitive Obsession

**Problem:** Overusing primitives instead of domain objects.

```python
# Bad - Primitives everywhere
def create_user(email: str, phone: str, birth_date: str, address: str):
    if '@' not in email:
        raise ValueError("Invalid email")
    if not phone.startswith('+'):
        raise ValueError("Invalid phone")
    # Parse birth_date string every time...
    # Parse address string every time...
```

**Solution:** Create value objects.

```python
# Good - Domain types
@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if '@' not in self.value:
            raise ValueError(f"Invalid email: {self.value}")

@dataclass(frozen=True)
class PhoneNumber:
    value: str

    def __post_init__(self):
        if not self.value.startswith('+'):
            raise ValueError(f"Invalid phone: {self.value}")

@dataclass
class User:
    email: Email
    phone: PhoneNumber
    birth_date: date
    address: Address

# Validation happens at construction
user = User(
    email=Email("user@example.com"),
    phone=PhoneNumber("+1234567890"),
    birth_date=date(1990, 1, 1),
    address=Address(street="123 Main St", city="NYC")
)
```

---

## Testing Anti-Patterns

### Test After Development

**Problem:** Writing tests after code is complete.

**Issues:**
- Tests become documentation, not design drivers
- Hard-to-test code gets skipped
- Bias toward implementation details

**Solution:** Practice TDD.

```python
# TDD Flow
# 1. Write failing test
def test_order_total_includes_tax():
    order = Order()
    order.add_item(Product(price=Decimal("100")))

    total = order.calculate_total(tax_rate=Decimal("0.08"))

    assert total == Decimal("108")

# 2. Run test - RED
# 3. Write minimal code - GREEN
# 4. Refactor - still GREEN
```

---

### Mock Everything

**Problem:** Mocking so much that tests don't test anything real.

```python
# Bad - Mocks testing mocks
def test_user_service():
    mock_repo = Mock()
    mock_hasher = Mock()
    mock_validator = Mock()
    mock_notifier = Mock()

    mock_validator.validate.return_value = True
    mock_hasher.hash.return_value = "hashed"
    mock_repo.save.return_value = User(id=1)

    service = UserService(mock_repo, mock_hasher, mock_validator, mock_notifier)
    result = service.create({"email": "test@example.com"})

    # This tests nothing meaningful!
    assert result.id == 1
```

**Solution:** Mock at boundaries only.

```python
# Good - Mock external systems, test real logic
def test_user_service_creates_user_with_hashed_password():
    # Real hasher - it's our code, test it
    hasher = BcryptHasher()
    # Fake repo - in-memory, fast, real behavior
    repo = InMemoryUserRepository()
    # Mock only external system
    notifier = Mock()

    service = UserService(repo, hasher, notifier)
    user = service.create({"email": "test@example.com", "password": "secret"})

    # Test real behavior
    assert user.id is not None
    assert user.verify_password("secret")
    notifier.send_welcome.assert_called_once()
```

---

### Brittle Tests

**Problem:** Tests that break with any implementation change.

```python
# Bad - Tests implementation details
def test_user_creation():
    service = UserService()
    service.create({"email": "test@example.com"})

    # Testing internal state
    assert len(service._user_cache) == 1
    assert service._last_created_id == 1
    assert service._creation_log[-1]['action'] == 'create'
```

**Solution:** Test behavior, not implementation.

```python
# Good - Tests observable behavior
def test_created_user_can_be_retrieved():
    service = UserService()

    user = service.create({"email": "test@example.com"})
    retrieved = service.get_by_email("test@example.com")

    assert retrieved.id == user.id
```

---

### Slow Tests

**Problem:** Tests that take too long to run.

```python
# Bad - Real database per test
def test_user_creation():
    db = PostgresDatabase("localhost:5432/test")
    db.execute("DELETE FROM users")  # Slow!

    service = UserService(db)
    user = service.create(...)

    assert db.execute("SELECT * FROM users").count() == 1  # Slow!
```

**Solution:** Use in-memory fakes for unit tests.

```python
# Good - Fast in-memory fake
class InMemoryUserRepository:
    def __init__(self):
        self.users = {}
        self._id_counter = 0

    def save(self, user: User) -> User:
        self._id_counter += 1
        user.id = self._id_counter
        self.users[user.id] = user
        return user

def test_user_creation():
    repo = InMemoryUserRepository()  # Fast!
    service = UserService(repo)

    user = service.create(...)

    assert len(repo.users) == 1
```

---

## Design Anti-Patterns

### Tight Coupling

**Problem:** Classes directly depend on concrete implementations.

```python
# Bad - Tight coupling
class OrderProcessor:
    def __init__(self):
        self.db = PostgresDatabase()
        self.email = SMTPEmailer()
        self.payment = StripeGateway()

    def process(self, order):
        self.db.save(order)
        self.payment.charge(order.total)
        self.email.send(order.customer_email, "Order confirmed")
```

**Solution:** Dependency injection.

```python
# Good - Loose coupling
class OrderProcessor:
    def __init__(
        self,
        repository: OrderRepository,
        payment: PaymentGateway,
        notifier: Notifier
    ):
        self.repository = repository
        self.payment = payment
        self.notifier = notifier

    def process(self, order: Order) -> None:
        self.repository.save(order)
        self.payment.charge(order.total)
        self.notifier.notify(order.customer_email, "Order confirmed")
```

---

### Feature Envy

**Problem:** Method uses more features of another class than its own.

```python
# Bad - Feature envy
class InvoiceGenerator:
    def calculate_total(self, order):
        subtotal = sum(item.price * item.quantity for item in order.items)
        discount = order.discount_percent / 100
        tax = order.tax_rate
        shipping = order.shipping_cost

        return (subtotal * (1 - discount) + shipping) * (1 + tax)
```

**Solution:** Move behavior to the right class.

```python
# Good - Behavior belongs to Order
class Order:
    def calculate_total(self) -> Decimal:
        subtotal = sum(item.total for item in self.items)
        discounted = subtotal * (1 - self.discount_percent / 100)
        with_shipping = discounted + self.shipping_cost
        return with_shipping * (1 + self.tax_rate)

class InvoiceGenerator:
    def generate(self, order: Order) -> Invoice:
        return Invoice(total=order.calculate_total())
```

---

### Callback Hell

**Problem:** Deeply nested callbacks.

```python
# Bad - Callback hell
def process_order(order_id, callback):
    get_order(order_id, lambda order:
        validate_order(order, lambda validated:
            check_inventory(validated, lambda available:
                process_payment(available, lambda paid:
                    ship_order(paid, lambda shipped:
                        notify_customer(shipped, callback)
                    )
                )
            )
        )
    )
```

**Solution:** Use async/await or compose functions.

```python
# Good - Async/await
async def process_order(order_id: int) -> Order:
    order = await get_order(order_id)
    validated = await validate_order(order)
    available = await check_inventory(validated)
    paid = await process_payment(available)
    shipped = await ship_order(paid)
    await notify_customer(shipped)
    return shipped
```

---

## Python-Specific Anti-Patterns

### Mutable Default Arguments

**Problem:** Default mutable arguments are shared across calls.

```python
# Bad - Mutable default
def add_item(item, items=[]):
    items.append(item)
    return items

add_item("a")  # ["a"]
add_item("b")  # ["a", "b"] - Oops!
```

**Solution:** Use `None` as default.

```python
# Good - None default
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

---

### Bare Except Clauses

**Problem:** Catching all exceptions hides bugs.

```python
# Bad - Catches everything
try:
    process_data(data)
except:
    log.error("Something went wrong")
    # Catches KeyboardInterrupt, SystemExit, bugs...
```

**Solution:** Catch specific exceptions.

```python
# Good - Specific exceptions
try:
    process_data(data)
except ValidationError as e:
    log.warning(f"Invalid data: {e}")
    raise
except DatabaseError as e:
    log.error(f"Database error: {e}")
    raise ServiceError("Failed to process") from e
```

---

### Using `type()` for Type Checking

**Problem:** Doesn't work with inheritance.

```python
# Bad - Doesn't catch subclasses
if type(animal) == Dog:
    animal.bark()
```

**Solution:** Use `isinstance()`.

```python
# Good - Works with inheritance
if isinstance(animal, Dog):
    animal.bark()
```

---

## Anti-Pattern Quick Reference

| Anti-Pattern | Symptom | Solution |
|--------------|---------|----------|
| God Class | Too many methods | Split by responsibility |
| Spaghetti Code | Deep nesting | Extract functions |
| Primitive Obsession | str/int/dict everywhere | Create value objects |
| Test After | Tests feel like chores | Practice TDD |
| Mock Everything | Tests don't catch bugs | Mock boundaries only |
| Tight Coupling | Can't test in isolation | Dependency injection |
| Feature Envy | Reaching into other objects | Move method to data |
| Mutable Default | Shared state bugs | Use `None` default |
| Bare Except | Hidden errors | Catch specific exceptions |

## See Also

- [Main Skill](../SKILL.md)
- [SOLID Principles](SOLID_PRINCIPLES.md)
- [TDD Patterns](TDD_PATTERNS.md)
