---
title: "Strategy Pattern (Python)"
description: "Learn the Strategy design pattern from first principles with Python examples: interchangeable algorithms behind a common interface, selectable at runtime"
tags:
  - python
  - programming
  - design-patterns
  - strategy
  - clean-code
difficulty: intermediate
last_updated: "2026-09-17"
---

# Strategy Pattern

!!! info "The pattern"
    Define a family of interchangeable algorithms, put each in its own object
    behind a common interface, and let the client **select or swap** them at
    runtime — without the client's code changing.

## Introduction

**Principles** tell you *what* good design looks like; **patterns** are reusable
recipes that achieve those principles for recurring problems. Strategy is the
concrete recipe for the [Open/Closed Principle](../solid-principles.md).

---

## The Problem

A checkout applies discounts via an `if/elif` chain:

```python
class Checkout:
    def total(self, cart_amount, customer_type):
        if customer_type == "regular":
            return cart_amount
        elif customer_type == "member":
            return cart_amount * 0.9        # 10% off
        elif customer_type == "vip":
            return cart_amount * 0.8        # 20% off
```

Every new discount type (`student`, `black_friday`, `employee`...) forces you to
**edit this tested method** — violating Open/Closed, risking existing branches, and
making each rule hard to test in isolation.

---

## The Fix: Strategy

Pull each discount *algorithm* into its own object behind a common contract; the
client holds one and delegates to it.

```python
from typing import Protocol


# The strategy contract
class DiscountStrategy(Protocol):
    def apply(self, cart_amount: float) -> float: ...


# Each algorithm in its own object
class RegularDiscount:
    def apply(self, cart_amount: float) -> float:
        return cart_amount

class MemberDiscount:
    def apply(self, cart_amount: float) -> float:
        return cart_amount * 0.9        # 10% off

class VipDiscount:
    def apply(self, cart_amount: float) -> float:
        return cart_amount * 0.8        # 20% off


# Checkout holds ONE strategy and delegates — never changes
class Checkout:
    def __init__(self, discount: DiscountStrategy):
        self.discount = discount

    def total(self, cart_amount: float) -> float:
        return self.discount.apply(cart_amount)
```

**Usage** — select the strategy at runtime:

```python
print(Checkout(RegularDiscount()).total(100))   # 100
print(Checkout(MemberDiscount()).total(100))    # 90
print(Checkout(VipDiscount()).total(100))       # 80
```

Adding a `StudentDiscount` means writing a **new class** — `Checkout.total()` is
never touched.

---

## What Strategy Buys You (vs. `if/elif`)

| What Strategy buys you | Why `if/elif` can't |
|------------------------|---------------------|
| **Add without editing** (OCP) | New discount = new class; `if/elif` forces editing the tested method |
| **Test in isolation** | `MemberDiscount().apply(100) == 90` needs no Checkout, no other branches |
| **Swap at runtime** | Strategy chosen from config, user input, or an A/B test; `if/elif` hardcodes all choices |

!!! tip "When to use it (earn the complexity)"
    Use Strategy when you have **multiple ways to do one thing**, those ways
    **genuinely vary**, and you want to **choose/swap** behavior without editing the
    client. If there is only ever one algorithm, a plain function is simpler —
    Strategy would be over-engineering (KISS/YAGNI).

---

## How It Connects

- **Open/Closed** — extend by adding strategies, not editing existing code.
- **Dependency Inversion** — the client depends on the `DiscountStrategy`
  abstraction, not concrete discounts.
- **Composition over Inheritance** — the client *has-a* strategy (composed) rather
  than subclassing per type.

## Summary Checklist

- [ ] Do I have a growing `if/elif` selecting between algorithms?
- [ ] Do the algorithms genuinely vary (real present need)?
- [ ] Do I need to choose or swap behavior at runtime?
- [ ] Does each strategy implement a common interface (`Protocol`/`ABC`)?

## Related Topics

- [SOLID Principles (Python)](../solid-principles.md)
- [Composition over Inheritance (Python)](../composition-over-inheritance.md)

---

**Tags**: #python #programming #design-patterns #strategy #clean-code

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
