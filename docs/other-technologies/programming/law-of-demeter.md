---
title: "Law of Demeter - Don't Talk to Strangers (Python)"
description: "Learn the Law of Demeter from first principles with Python examples: avoid train-wreck call chains and reduce coupling with tell-don't-ask"
tags:
  - python
  - programming
  - design-principles
  - coupling
  - clean-code
difficulty: intermediate
last_updated: "2026-09-17"
---

# Law of Demeter

!!! info "The principle"
    **"Don't talk to strangers."** A method should only talk to its *immediate
    friends*, not to distant objects reached through them. This reduces coupling
    and stops small changes from rippling across the codebase.

## Introduction

A method `m` on object `O` should only call methods on:

- `O` itself,
- objects passed **into** `m` as arguments,
- objects `O` **directly holds** (its own attributes),
- objects `m` **creates**.

It should **not** call methods on objects *returned by other calls* — that is
"talking to a stranger." The classic smell is a **train wreck**:
`a.b.c.d.method()`.

---

## The Problem

```python
class Order:
    def __init__(self, customer):
        self.customer = customer

    def charge(self, amount):
        # reaches through the whole chain: order -> customer -> wallet -> card -> number
        card_number = self.customer.wallet.credit_card.number
        payment_gateway.charge(card_number, amount)
```

`Order` reaches through `customer.wallet.credit_card.number` — three levels of
*someone else's* internal structure.

### Why this is fragile

Suppose the payments team lets a customer have **multiple** cards, so
`wallet.credit_card` becomes `wallet.cards` (a list) with a `default_card()`
method:

```python
# This line now BREAKS — .credit_card no longer exists
card_number = self.customer.wallet.credit_card.number
```

An **order-management** class must be edited because of a change to **how wallets
store cards**. The hidden costs:

- **Fragile coupling** — `Order` is glued to the internals of `Wallet` and
  `CreditCard`, classes it was never directly handed.
- **Ripple effect** — one internal change breaks every distant class that reached
  through the chain.
- **Broken encapsulation** — `Wallet`/`CreditCard` can't change their own internals
  freely because outsiders peek inside them.

---

## The Fix: Tell, Don't Ask

Instead of reaching *through* the customer, `Order` asks its immediate friend to do
the work, and each object handles its **own** internals:

```python
class CreditCard:
    def __init__(self, number):
        self._number = number

    def charge(self, amount):
        payment_gateway.charge(self._number, amount)   # the card charges itself


class Wallet:
    def __init__(self, card):
        self._card = card

    def charge(self, amount):
        self._card.charge(amount)        # wallet delegates to its card


class Customer:
    def __init__(self, wallet):
        self._wallet = wallet

    def charge(self, amount):
        self._wallet.charge(amount)      # customer delegates to its wallet


class Order:
    def __init__(self, customer):
        self.customer = customer

    def charge(self, amount):
        self.customer.charge(amount)     # Order only talks to its friend: customer
```

Now `Order.charge` is a single dot: `self.customer.charge(amount)`. It knows
nothing about wallets, cards, or numbers.

When the payments team changes how wallets store cards, they edit `Wallet` (and
maybe `CreditCard`) — **`Order` and `Customer` never change.** Each object owns its
internals.

---

## How to Spot & Apply It

!!! tip "Two quick tests"
    - **Count the dots.** `self.customer.charge()` → one dot, good.
      `self.customer.wallet.credit_card.number` → train wreck, bad.
    - **Tell, don't ask.** Instead of *asking* an object for its internals and
      doing the work yourself, **tell** it to do the work.

!!! warning "Don't apply it blindly"
    Dot chains on plain **data structures** (`data["user"]["address"]["zip"]`) or
    fluent builders (`query.filter().order().limit()`) are usually fine — those are
    intended usage, not reaching through object internals. The Law of Demeter
    targets **behavioral coupling to objects' internal structure**, not every
    chained call.

---

## How It Connects

- **Single Responsibility (SOLID)** — objects that own their internals have clearer,
  single responsibilities.
- **Encapsulation** — delegating keeps each object's internals private and free to
  change.
- **Composition over Inheritance** — delegation between composed objects is exactly
  how "tell, don't ask" is implemented.

## Summary Checklist

- [ ] Are there train-wreck chains (`a.b.c.d.method()`) reaching through internals?
- [ ] Can I replace a chain by *telling* an immediate friend to do the work?
- [ ] Does each object own and hide its own internal structure?
- [ ] Am I distinguishing behavioral coupling from harmless data/fluent chains?

## Related Topics

- [SOLID Principles (Python)](solid-principles.md)
- [Composition over Inheritance (Python)](composition-over-inheritance.md)
- [DRY, KISS & YAGNI (Python)](dry-kiss-yagni.md)

---

**Tags**: #python #programming #law-of-demeter #coupling #clean-code

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
