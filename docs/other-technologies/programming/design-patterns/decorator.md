---
title: "Decorator Pattern (Python)"
description: "Learn the Decorator design pattern from first principles: add behavior by wrapping, covering both Python's @ function decorators and the class-based GoF form"
tags:
  - python
  - programming
  - design-patterns
  - decorator
  - clean-code
difficulty: intermediate
last_updated: "2026-09-18"
---

# Decorator Pattern

!!! info "The pattern"
    Dynamically add behavior to an object or function by **wrapping** it in
    another with the **same interface** — so the wrapper is usable wherever the
    original was, and wrappers can be **stacked**.

## Introduction

Where the [Adapter](adapter.md) wraps an object to *change its interface*, the
Decorator wraps to *add behavior while keeping the same interface*. Python's `@`
syntax (`@staticmethod`, `@classmethod`) is this pattern built into the language.

---

## The Problem

Cross-cutting concerns (logging, caching, auth) get crammed into a function whose
real job is just fetching a user:

```python
def get_user(user_id):
    log(f"calling get_user({user_id})")           # logging
    if user_id in cache:                          # caching
        return cache[user_id]
    if not current_user_is_authorized():          # auth
        raise PermissionError()
    result = {"id": user_id, "name": "Alice"}     # the actual job, buried
    cache[user_id] = result
    return result
```

This violates **Single Responsibility** (four jobs in one function), **DRY** (every
other function needs the same logging/caching/auth), and **Open/Closed** (a new
concern means editing every function).

---

## Form 1: Python `@` Function Decorators

A decorator is a function that takes a function and returns a new one that wraps it.

```python
import functools

def with_logging(func):
    @functools.wraps(func)                    # preserves name/docstring
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__} with {args}")   # behavior BEFORE
        result = func(*args, **kwargs)                   # call the ORIGINAL
        print(f"{func.__name__} returned {result}")      # behavior AFTER
        return result
    return wrapper
```

Apply it — the `@` syntax is literally `get_user = with_logging(get_user)`:

```python
@with_logging
def get_user(user_id):
    return {"id": user_id, "name": "Alice"}
```

`get_user` itself is never modified — the logging lives in the wrapper.

### Stacking decorators

```python
@with_logging          # outermost
@with_cache            # middle
@with_auth             # innermost — runs closest to the real function
def get_user(user_id):
    return {"id": user_id, "name": "Alice"}
```

Equivalent to `with_logging(with_cache(with_auth(get_user)))`. A call flows through
each layer like an onion: logging → cache → auth → **real function** → back out.
Each wrapper has **one job** (SRP), is reused across many functions (DRY), and is
added without editing the original (Open/Closed).

---

## Form 2: Class-Based Decorator (the GoF form)

The original Gang of Four pattern wraps **objects**, not functions. The wrapper
implements the **same interface** and delegates to the wrapped object.

```python
from typing import Protocol


class DataSource(Protocol):
    def get(self, key: str) -> str: ...


class DatabaseSource:                         # the real thing (slow)
    def get(self, key: str) -> str:
        print(f"  querying database for {key}")
        return f"value_for_{key}"


class CachingDataSource:                      # SAME interface: has get()
    def __init__(self, wrapped: DataSource):  # wraps another DataSource
        self._wrapped = wrapped
        self._cache: dict[str, str] = {}

    def get(self, key: str) -> str:
        if key in self._cache:                # added behavior
            print(f"  cache hit for {key}")
            return self._cache[key]
        value = self._wrapped.get(key)        # delegate to wrapped object
        self._cache[key] = value
        return value
```

**Usage** — the wrapper is interchangeable with what it wraps:

```python
source: DataSource = DatabaseSource()
source = CachingDataSource(source)            # wrap to add caching

source.get("user:1")   # querying database for user:1  (miss)
source.get("user:1")   # cache hit for user:1           (hit)
```

Class decorators stack too:

```python
source = LoggingDataSource(CachingDataSource(DatabaseSource()))
```

---

## Decorator vs. Adapter

| | Adapter | Decorator |
|---|---------|-----------|
| Wraps an object/function? | Yes | Yes |
| Changes the interface? | **Yes** (makes incompatible things fit) | **No** (keeps the same interface) |
| Purpose | Translate | Add behavior |

Both wrap; Adapter *translates*, Decorator *enhances*.

## When to Use It

- Add **cross-cutting concerns** (logging, caching, auth, retry, timing,
  validation) **without modifying** the original, **and**
- Make those concerns **reusable and composable** across many targets.

Use **function form** (`@`) for standalone functions; use **class form** for objects
with state or multiple methods (a `DataSource`, `Repository`, `HttpClient`).

## How It Connects

- **Single Responsibility** — each decorator does one thing; the target stays focused.
- **Open/Closed** — add behavior by adding a decorator, not editing the original.
- **DRY** — one decorator reused across many targets.
- **Composition over Inheritance** — stacking composes behavior at runtime instead
  of subclassing for every combination (avoids class explosion).

## Summary Checklist

- [ ] Am I mixing cross-cutting concerns into a function's core logic?
- [ ] Can I move each concern into its own wrapper (same interface)?
- [ ] Can I stack/compose the wrappers as needed per target?
- [ ] Is the original code left unmodified?

## Related Topics

- [Adapter Pattern (Python)](adapter.md)
- [Composition over Inheritance (Python)](../composition-over-inheritance.md)
- [SOLID Principles (Python)](../solid-principles.md)

---

**Tags**: #python #programming #design-patterns #decorator #clean-code

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
