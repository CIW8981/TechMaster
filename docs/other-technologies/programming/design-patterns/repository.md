---
title: "Repository Pattern (Python)"
description: "Learn the Repository design pattern from first principles with Python examples: hide storage behind a collection-like interface for swappable, testable data access"
tags:
  - python
  - programming
  - design-patterns
  - repository
  - clean-code
difficulty: intermediate
last_updated: "2026-09-18"
---

# Repository Pattern

!!! info "The pattern"
    Mediate between business logic and data storage by providing a
    **collection-like interface** (`save`, `find`, `delete`...) for accessing
    domain objects — hiding the underlying storage mechanism entirely.

## Introduction

The Repository pattern is [Dependency Inversion](../solid-principles.md) plus
[Separation of Concerns](../separation-of-concerns.md) turned into a concrete,
reusable recipe for the data layer. Think of it as an **in-memory collection
illusion**: business logic acts as if working with a simple collection of objects,
while the repository quietly handles the real database behind that illusion.

---

## The Problem

Business logic talks to the database directly, littered with SQL and driver
details:

```python
class UserService:
    def register(self, email, password):
        # ...validation...
        conn = sqlite3.connect("users.db")
        conn.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                     (email, password))
        conn.commit()

    def find_by_email(self, email):
        conn = sqlite3.connect("users.db")
        return conn.execute("SELECT * FROM users WHERE email = ?",
                            (email,)).fetchone()
```

Problems:

- **Migration is painful** — switching to PostgreSQL/Mongo/REST means rewriting
  every method containing SQL, with heavy re-testing. `UserService` now has *two*
  reasons to change (business rules **and** database tech) — a Single
  Responsibility / Separation of Concerns violation.
- **Hard to test** — testing the validation runs real SQL against a real database
  file.

---

## The Fix: A Repository

Put all storage details behind a domain-focused interface, and inject it.

```python
from typing import Protocol


# The abstraction — business logic depends on THIS, not on any database
class UserRepository(Protocol):
    def save(self, email: str, password: str) -> None: ...
    def find_by_email(self, email: str): ...


# Concrete implementation — all SQL/sqlite lives HERE, nowhere else
class SqliteUserRepository:
    def __init__(self, connection):
        self._conn = connection

    def save(self, email, password):
        self._conn.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        self._conn.commit()

    def find_by_email(self, email):
        return self._conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)).fetchone()


# Business logic — ZERO SQL, depends only on the UserRepository abstraction
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, email, password):
        if "@" not in email:
            raise ValueError("invalid email")     # pure business rule
        self.repo.save(email, password)

    def find_by_email(self, email):
        return self.repo.find_by_email(email)
```

### Migration — write a new repository, `UserService` never changes

```python
class PostgresUserRepository:                    # new class, same interface
    def save(self, email, password): ...         # Postgres SQL here
    def find_by_email(self, email): ...

service = UserService(PostgresUserRepository(pg_conn))   # inject a different one
```

### Testing — inject a fake, no database at all

```python
class FakeUserRepository:
    def __init__(self):
        self.users = {}
    def save(self, email, password):
        self.users[email] = password
    def find_by_email(self, email):
        return self.users.get(email)


def test_register_rejects_bad_email():
    service = UserService(FakeUserRepository())   # no DB, no SQL, no file
    try:
        service.register("no-at-sign", "pw")
        assert False
    except ValueError as e:
        assert str(e) == "invalid email"          # fast, pure logic test
```

---

## What a Repository Abstracts

> The Repository abstracts **where and how data is stored and retrieved** — SQL,
> connections, table names, the specific database technology — behind a simple,
> domain-focused interface.

Why hiding it behind an interface matters:

- **Storage-agnostic business logic** — `UserService` thinks "save a user," not
  "run this INSERT on SQLite." Backed by SQLite, Postgres, REST, or a dict — it
  can't tell.
- **The database becomes a swappable detail** (Dependency Inversion).
- **All persistence knowledge lives in one place** (Separation of Concerns + DRY).

---

## When to Use It

- Business logic needs to persist/retrieve domain objects, **and**
- You want storage details out of business logic (testability, swappability), **and**
- You might change storage tech, or need to test without a real database.

For a tiny throwaway script hitting one DB forever, it can be overkill
(KISS/YAGNI) — but for any app you'll test or maintain, it pays off quickly.

## How It Connects

- **Separation of Concerns** — it *is* the data layer, cleanly separated.
- **Dependency Inversion** — the service depends on the abstraction, not a concrete DB.
- **Single Responsibility** — the repository changes when *storage* changes; the
  service changes when *business rules* change.
- **Strategy / Factory** — a repository is a swappable persistence strategy; a
  factory can choose which repository to inject based on config.

## Summary Checklist

- [ ] Is SQL / driver code mixed into business logic?
- [ ] Can I swap the database by writing a new repository class only?
- [ ] Can I test business logic with a fake repository (no real DB)?
- [ ] Does the repository expose a domain-focused interface (`save`, `find`...)?

## Related Topics

- [Separation of Concerns (Python)](../separation-of-concerns.md)
- [SOLID Principles (Python)](../solid-principles.md)
- [Factory Pattern (Python)](factory.md)

---

**Tags**: #python #programming #design-patterns #repository #clean-code

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
