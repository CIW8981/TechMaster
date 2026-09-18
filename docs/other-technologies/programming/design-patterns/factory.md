---
title: "Factory Pattern (Python)"
description: "Learn the Factory design pattern from first principles with Python examples, plus when to use @staticmethod vs @classmethod for factory methods"
tags:
  - python
  - programming
  - design-patterns
  - factory
  - clean-code
difficulty: intermediate
last_updated: "2026-09-17"
---

# Factory Pattern

!!! info "The pattern"
    Centralize object creation in a dedicated component, so client code requests
    objects by a simple identifier (a string, enum, etc.) **without knowing or
    depending on the concrete classes** being instantiated.

## Introduction

The [Strategy pattern](strategy.md) makes behavior swappable — but *something*
still has to decide **which** strategy to create from input like a `customer_type`
string. The Factory pattern answers *where that decision lives*.

---

## The Problem

Creation logic leaks into the caller and gets duplicated:

```python
def checkout_for_customer(customer_type, cart_amount):
    if customer_type == "regular":
        discount = RegularDiscount()
    elif customer_type == "member":
        discount = MemberDiscount()
    elif customer_type == "vip":
        discount = VipDiscount()
    return Checkout(discount).total(cart_amount)
```

If several places need "turn a `customer_type` into a discount," this `if/elif` is
**copy-pasted** everywhere (a DRY violation), and every caller is coupled to the
concrete discount classes. Adding `StudentDiscount` means editing every copy.

---

## The Fix: A Factory

Put the "identifier → object" logic in **one** dedicated place.

```python
from typing import Protocol


class DiscountStrategy(Protocol):
    def apply(self, cart_amount: float) -> float: ...


class DiscountFactory:
    _discounts = {                          # the mapping lives in ONE place
        "regular": RegularDiscount,
        "member": MemberDiscount,
        "vip": VipDiscount,
    }

    @staticmethod
    def create(customer_type: str) -> DiscountStrategy:
        try:
            discount_class = DiscountFactory._discounts[customer_type]
        except KeyError:
            raise ValueError(f"Unknown customer type: {customer_type}")
        return discount_class()
```

Callers become trivial and know nothing about concrete classes:

```python
def checkout_for_customer(customer_type, cart_amount):
    discount = DiscountFactory.create(customer_type)   # just ask the factory
    return Checkout(discount).total(cart_amount)
```

Adding `StudentDiscount`? Add **one line** to the factory's map.

---

## What a Factory Accomplishes

The branching can't be *eliminated* (a string must map to a class somewhere) — the
Factory **quarantines** it:

1. **Centralizes the decision** — the mapping lives in exactly one place (DRY).
2. **Hides concrete classes** — callers depend only on the abstraction + factory,
   not on `RegularDiscount`/`MemberDiscount`/etc. (decoupling).
3. **Separates concerns** — *usage* (Checkout), *algorithm* (discounts), and
   *selection/creation* (factory) are isolated.

> **Strategy** answers "how do I make behavior swappable?"; **Factory** answers
> "where does deciding-and-creating live?" — in one isolated place.

---

## `@staticmethod` vs `@classmethod` for Factory Methods

A factory method uses neither instance data, so it should not require an instance.

=== "@staticmethod"

    ```python
    class DiscountFactory:
        _discounts = {"member": MemberDiscount}

        @staticmethod
        def create(customer_type):
            return DiscountFactory._discounts[customer_type]()   # hardcoded name

    DiscountFactory.create("member")     # no instance needed
    ```

    Simplest choice. Call directly on the class. Drawback: it hardcodes the class
    name, so subclasses that override `_discounts` are **not** respected.

=== "@classmethod (subclass-friendly)"

    ```python
    class DiscountFactory:
        _discounts = {"member": MemberDiscount}

        @classmethod
        def create(cls, customer_type):
            return cls._discounts[customer_type]()   # uses cls -> respects subclasses
    ```

    `cls` is **the class the method was called on** (the subclass if called via one),
    so subclass overrides work automatically. This is the idiomatic choice for
    factories and alternative constructors.

!!! warning "Without either decorator"
    A plain method requires `self`, forcing a pointless instance:
    `DiscountFactory().create("member")` — and Python would misread the first
    argument as `self`. Use `@staticmethod`/`@classmethod` to call on the class
    directly.

### Alternative constructors (the most common `@classmethod` use)

```python
class User:
    def __init__(self, name, age):
        self.name, self.age = name, age

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["age"])   # cls() builds the correct type


class AdminUser(User):
    pass

admin = AdminUser.from_dict({"name": "Bob", "age": 40})
print(type(admin))   # AdminUser — because from_dict used cls(), not User()
```

### Quick decision guide

| Method needs... | Use |
|-----------------|-----|
| this object's instance data (`self.x`) | normal method |
| the class, e.g. to support subclasses (`cls`) | `@classmethod` |
| neither — pure helper grouped in the class | `@staticmethod` |

---

## When to Use the Factory Pattern

- You create objects based on some **input/condition** (type string, config, choice), **and**
- The creation logic would otherwise be **duplicated** or **couple callers** to concrete classes, **and**
- You have (or will have) **multiple types** to choose from.

If you only ever create one fixed class, skip the factory (KISS/YAGNI).

## How It Connects

- **DRY** — creation knowledge lives in one place.
- **Open/Closed** — add a type by editing only the factory (or registering into its map).
- **Dependency Inversion** — callers depend on the abstraction + factory, not concretes.
- **Pairs with Strategy** — Strategy defines swappable behaviors; Factory decides which to instantiate.

## Summary Checklist

- [ ] Is object-creation `if/elif` duplicated across callers?
- [ ] Are callers coupled to concrete classes they shouldn't know about?
- [ ] Did I centralize creation in one factory?
- [ ] Did I choose `@staticmethod` vs `@classmethod` deliberately (subclassing?)?

## Related Topics

- [Strategy Pattern (Python)](strategy.md)
- [SOLID Principles (Python)](../solid-principles.md)

---

**Tags**: #python #programming #design-patterns #factory #clean-code

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
