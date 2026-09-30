---
title: "SOLID Principles in Python - First Principles Guide"
description: "Learn the five SOLID object-oriented design principles from first principles, with practical Python examples using ABC, Protocol, and dependency injection"
tags:
  - python
  - programming
  - design-principles
  - solid
  - clean-code
difficulty: intermediate
last_updated: "2026-09-17"
---

# SOLID Principles in Python

!!! info "What is SOLID?"
    SOLID is a set of five object-oriented design principles that make software
    easier to change, test, and maintain. This guide derives each principle from
    **first principles** — starting from the root problem it solves — using
    practical Python examples.

## Introduction

Every SOLID principle answers one root problem: **software changes over time, and
change is expensive when code is rigidly coupled.** The principles are strategies
to make change cheap. Because that root problem exists in every language, SOLID
applies fully to Python — with Python's dynamic nature (duck typing, `Protocol`,
mixins) changing *how* some principles are applied.

| Letter | Principle | One-line memory hook |
|--------|-----------|----------------------|
| **S** | Single Responsibility | One class, one reason to change |
| **O** | Open/Closed | Open to extension, closed to modification |
| **L** | Liskov Substitution | A child must be usable as its parent |
| **I** | Interface Segregation | Keep interfaces small and focused |
| **D** | Dependency Inversion | Depend on abstractions, not concretes |

---

## S — Single Responsibility Principle

!!! abstract "Definition"
    A class should have only **one reason to change** — where a "reason" is tied
    to a single stakeholder/actor whose needs drive that change.

### The Problem

```python
class Invoice:
    def __init__(self, items):
        self.items = items  # list of (name, price, qty)

    def total(self):
        return sum(price * qty for _, price, qty in self.items)

    def save_to_db(self):
        connection = connect_to_postgres()
        connection.execute("INSERT INTO invoices ...")

    def send_email(self, customer):
        smtp = connect_smtp("smtp.company.com")
        smtp.send(customer.email, f"Your total is {self.total()}")
```

Three unrelated business events each force you to open the **same** class:

1. Finance changes tax rules → edit `total()`
2. Ops migrates the database → edit `save_to_db()`
3. Marketing changes notifications → edit `send_email()`

**The danger:** editing the email logic means touching a file that also contains
billing and persistence code. A small change now has a large blast radius — a
mistake or merge conflict can break unrelated features.

### The Fix

Split by reason-to-change: one responsibility per class.

```python
class Invoice:
    def __init__(self, items):
        self.items = items

    def total(self):                       # changes only when finance changes rules
        return sum(price * qty for _, price, qty in self.items)


class InvoiceRepository:
    def save(self, invoice):               # changes only when storage changes
        connection = connect_to_postgres()
        connection.execute("INSERT INTO invoices ...")


class InvoiceNotifier:
    def send(self, invoice, customer):     # changes only when notifications change
        smtp = connect_smtp("smtp.company.com")
        smtp.send(customer.email, f"Your total is {invoice.total()}")
```

Now an email change never touches billing or persistence.

---

## O — Open/Closed Principle

!!! abstract "Definition"
    Software should be **open to extension but closed to modification**. Add new
    behavior by writing new code, not by editing existing, tested code.

### The Problem

```python
class ShippingCalculator:
    def cost(self, package):
        if package.kind == "standard":
            return package.weight * 1.0
        elif package.kind == "express":
            return package.weight * 2.5
        elif package.kind == "overnight":
            return package.weight * 5.0
```

Every new shipping type means adding another `elif` to a method that already
works. Editing tested code risks breaking `standard` while adding `drone`, and
forces you to re-verify everything that was already correct.

### The Fix

Let each package type carry its own cost rule; the calculator delegates.

```python
from typing import Protocol


class ShippingStrategy(Protocol):
    def cost(self, weight: float) -> float: ...


class Standard:
    def cost(self, weight: float) -> float:
        return weight * 1.0

class Express:
    def cost(self, weight: float) -> float:
        return weight * 2.5

class Overnight:
    def cost(self, weight: float) -> float:
        return weight * 5.0


class Package:
    def __init__(self, weight: float, strategy: ShippingStrategy):
        self.weight = weight
        self.strategy = strategy


class ShippingCalculator:
    def cost(self, package: Package) -> float:
        return package.strategy.cost(package.weight)   # never changes again
```

**Usage** — adding `Drone` requires zero edits to `ShippingCalculator`:

```python
calc = ShippingCalculator()
print(calc.cost(Package(10, Standard())))   # 10.0
print(calc.cost(Package(10, Express())))    # 25.0

# OPEN/CLOSED IN ACTION: just ADD a new class, don't touch anything above.
class Drone:
    def cost(self, weight: float) -> float:
        return weight * 8.0

print(calc.cost(Package(10, Drone())))       # 80.0
```

!!! tip "Duck typing"
    Notice `Standard`, `Express`, and `Drone` do **not** inherit from
    `ShippingStrategy`. Python only cares that they *have* a `cost(weight)`
    method — "if it quacks like a duck, it's a duck." The `Protocol` documents
    the contract and lets `mypy` verify it, without requiring inheritance.

---

## L — Liskov Substitution Principle

!!! abstract "Definition"
    Named after **Barbara Liskov** (Turing Award, 2008). A subclass must be
    **substitutable** for its parent without breaking the behavioral expectations
    the parent established. *If code works with the parent, it must still work with
    any child.*

### The Problem

Mathematically a square is a rectangle — but that "is-a" is a trap in code:

```python
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def set_width(self, width):
        self._width = width

    def set_height(self, height):
        self._height = height

    def area(self):
        return self._width * self._height


class Square(Rectangle):
    def set_width(self, width):
        self._width = width
        self._height = width          # keep it square

    def set_height(self, height):
        self._width = height          # keep it square
        self._height = height
```

Code written against `Rectangle` breaks when given a `Square`:

```python
def resize_and_check(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20          # Square gives 16 -> AssertionError!
```

The failure is **not** a type error — `Square` *is* a `Rectangle`. It's a broken
**behavioral promise**: `Rectangle` promises width and height are independent;
`Square` secretly couples them.

### The Fix

A mutable `Square` is simply not a behavioral subtype of a mutable `Rectangle`.
Either drop the inheritance (use a shared abstraction)...

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...


class Rectangle(Shape):
    def __init__(self, width, height):
        self._width, self._height = width, height
    def set_width(self, w): self._width = w
    def set_height(self, h): self._height = h
    def area(self): return self._width * self._height


class Square(Shape):
    def __init__(self, side):
        self._side = side
    def set_side(self, s): self._side = s
    def area(self): return self._side * self._side


def total_area(shapes: list[Shape]) -> float:
    return sum(s.area() for s in shapes)   # safe for any Shape

print(total_area([Rectangle(5, 4), Square(3)]))   # 29 — always correct
```

...or make the objects immutable so no operation can break the promise:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Rectangle:
    width: float
    height: float

    @property
    def area(self) -> float:
        return self.width * self.height


@dataclass(frozen=True)
class Square(Rectangle):
    def __init__(self, side: float):
        super().__init__(width=side, height=side)
```

!!! success "The test to remember"
    Before writing `class Child(Parent)`, ask: *"Can I hand a `Child` to every
    piece of code that expects a `Parent`, and have all of it still work?"* If
    not — don't inherit.

---

## I — Interface Segregation Principle

!!! abstract "Definition"
    Don't force a class to depend on methods it doesn't use. Split fat interfaces
    into small, focused ones. (Think of it as *"SRP for interfaces"*.)

### The Problem

```python
from abc import ABC, abstractmethod


class Machine(ABC):
    @abstractmethod
    def print(self, doc): ...
    @abstractmethod
    def scan(self, doc): ...
    @abstractmethod
    def fax(self, doc): ...


class CheapPrinter(Machine):
    def print(self, doc): print(f"Printing {doc}")
    def scan(self, doc): ...   # can't scan — forced to fake it
    def fax(self, doc): ...    # can't fax — forced to fake it
```

A print-only device is forced to implement `scan()` and `fax()`. Every way of
filling them in is bad: `pass` lies silently, `raise NotImplementedError`
crashes, a print statement returns garbage. The fat interface put the class in an
impossible spot — and breaks Liskov (a `CheapPrinter` can't stand in for a
`Machine`).

### The Fix

Split the fat interface into small, focused ones.

```python
from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print(self, doc): ...

class Scanner(ABC):
    @abstractmethod
    def scan(self, doc): ...

class Fax(ABC):
    @abstractmethod
    def fax(self, doc): ...


class CheapPrinter(Printer):                    # only what it can do
    def print(self, doc): print(f"Printing {doc}")


class AllInOnePrinter(Printer, Scanner, Fax):   # composes real capabilities
    def print(self, doc): print(f"Printing {doc}")
    def scan(self, doc):  print(f"Scanning {doc}")
    def fax(self, doc):   print(f"Faxing {doc}")
```

**Usage** — each function asks for only the capability it needs:

```python
def do_print_job(device: Printer, doc): device.print(doc)
def do_scan_job(device: Scanner, doc):  device.scan(doc)
def do_fax_job(device: Fax, doc):       device.fax(doc)

all_in_one = AllInOnePrinter()
cheap = CheapPrinter()

do_print_job(all_in_one, "report.pdf")    # OK
do_scan_job(all_in_one, "contract.pdf")   # OK
do_print_job(cheap, "memo.pdf")           # OK
# do_scan_job(cheap, "memo.pdf")          # rejected: CheapPrinter is not a Scanner
```

The impossible "fake `scan()`" situation can no longer even be expressed.

---

## D — Dependency Inversion Principle

!!! abstract "Definition"
    High-level modules should not depend on low-level details. Both should depend
    on **abstractions**. Instead of a class creating its own dependencies, they
    are **injected** from outside.

### The Problem

```python
class MySQLDatabase:
    def save(self, data):
        print(f"Saving to MySQL: {data}")


class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()      # creates its own database

    def place_order(self, order):
        # business logic...
        self.db.save(order)
```

Two problems:

- **Testing:** `OrderService()` always hits a real MySQL — you can't unit test the
  business logic without a live database.
- **Change:** switching to PostgreSQL means editing `OrderService` (business
  logic) just to change a storage detail.

The root cause: high-level business logic is **welded to** a low-level detail.

### The Fix

Depend on an abstraction and **inject** the concrete implementation.

```python
from abc import ABC, abstractmethod


class Database(ABC):                     # the abstraction
    @abstractmethod
    def save(self, data): ...


class MySQLDatabase(Database):
    def save(self, data): print(f"Saving to MySQL: {data}")


class PostgresDatabase(Database):
    def save(self, data): print(f"Saving to Postgres: {data}")


class OrderService:
    def __init__(self, db: Database):    # receives the db from outside
        self.db = db

    def place_order(self, order):
        # business logic...
        self.db.save(order)
```

**Usage** — create the dependency at the top and pass it in:

```python
service = OrderService(MySQLDatabase())
service.place_order("Book x2")

# Switch databases without editing OrderService:
service = OrderService(PostgresDatabase())
```

**Testing** becomes trivial — inject a fake:

```python
class FakeDatabase(Database):
    def __init__(self):
        self.saved = []
    def save(self, data):
        self.saved.append(data)          # records instead of hitting a real DB


def test_place_order_saves():
    fake = FakeDatabase()
    service = OrderService(fake)         # inject the fake
    service.place_order("Book x2")
    assert fake.saved == ["Book x2"]     # no real database needed
```

The direction of dependency is **inverted**: `OrderService` no longer depends on a
specific database — the database depends on the abstraction that `OrderService`
owns.

---

## Choosing Your Abstraction: `ABC` vs `Protocol`

Python offers two ways to define contracts. There is no `interface` keyword.

| | `ABC` + `@abstractmethod` | `Protocol` |
|---|---|---|
| Typing style | **Nominal** — "I AM a X" (must inherit) | **Structural** — "I LOOK LIKE a X" (duck typing) |
| Inheritance required | Yes | No |
| Share concrete code | Yes (mixed abstract + real methods) | No (shape only) |
| Enforcement | Runtime (can't instantiate if incomplete) | Static (via `mypy`/`pyright`) |
| Works with 3rd-party classes | No | Yes |

!!! tip "Rule of thumb"
    - Default to **`ABC`** when you control the classes, want explicit hierarchies,
      want to share code, or want runtime enforcement.
    - Reach for **`Protocol`** when you need loose coupling or must accept objects
      you don't own. Pair it with a type checker (`mypy`) since it's static-only.

### Bonus: `@override` (Python 3.12+)

Marks a method as intentionally overriding a parent's — catching typos that cause
silent Liskov violations.

```python
from typing import override


class Animal:
    def speak(self) -> str:
        return "..."


class Dog(Animal):
    @override
    def speak(self) -> str:      # verified to really override Animal.speak
        return "Woof"

# A typo like `def speek(...)` under @override is flagged by mypy/pyright.
```

---

## Data Validation is a Separate Concern

Libraries like **Pydantic** validate *data* ("is this weight positive?"), which is
a different job from behavioral contracts (`ABC`/`Protocol`). Keep them separate —
often you use both: `Protocol`/`ABC` for behavior, Pydantic for data.

```python
from pydantic import BaseModel, field_validator


class Package(BaseModel):
    weight: float
    strategy: object

    model_config = {"arbitrary_types_allowed": True}

    @field_validator("weight")
    @classmethod
    def weight_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("weight must be positive")
        return v
```

---

## How the Principles Reinforce Each Other

- **S and I** are cousins: SRP keeps *classes* focused; ISP keeps *interfaces*
  focused.
- **I and L**: fat interfaces force fake implementations, and fake implementations
  break substitutability. Slim interfaces prevent both.
- **O and D**: both rely on depending on abstractions so you can extend or swap
  behavior without editing tested code.

## Summary Checklist

- [ ] **S**: Does each class have only one reason to change?
- [ ] **O**: Can I add features by writing new code, not editing old code?
- [ ] **L**: Can any subclass replace its parent without breaking callers?
- [ ] **I**: Do classes implement only methods they actually use?
- [ ] **D**: Does high-level code depend on abstractions, not concrete details?

## Related Topics

- [Docker](../docker/index.md)
- [Kubernetes](../kubernetes/index.md)
- [Terraform](../terraform/index.md)

---

**Tags**: #python #programming #solid #design-principles #clean-code

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
