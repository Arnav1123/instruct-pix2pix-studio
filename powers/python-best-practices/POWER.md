---
name: "python-best-practices"
displayName: "Python Best Practices"
description: "Essential Python coding patterns and guidelines for writing clean, maintainable code"
keywords: ["python", "best-practices", "coding-standards", "pep8"]
author: "Your Name"
---

# Python Best Practices

## Overview

A quick reference guide for writing clean, idiomatic Python code. Covers naming conventions, code organization, and common patterns.

## Core Principles

1. **Readability counts** - Code is read more often than written
2. **Explicit is better than implicit** - Be clear about intentions
3. **Simple is better than complex** - Avoid over-engineering

## Common Patterns

### Naming Conventions

```python
# Variables and functions: snake_case
user_name = "Alice"
def calculate_total(items):
    pass

# Classes: PascalCase
class UserAccount:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_CONNECTIONS = 100
```

### List Comprehensions

```python
# Good: Clear and concise
squares = [x**2 for x in range(10)]

# Avoid: Overly complex comprehensions
# If it needs multiple lines, use a regular loop
```

### Context Managers

```python
# Good: Automatic resource cleanup
with open("file.txt", "r") as f:
    content = f.read()

# Avoid: Manual resource management
f = open("file.txt", "r")
content = f.read()
f.close()  # Easy to forget!
```

## Troubleshooting

### Common Mistake: Mutable Default Arguments

**Problem:**
```python
def add_item(item, items=[]):  # Bug!
    items.append(item)
    return items
```

**Solution:**
```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

## Best Practices Checklist

- [ ] Follow PEP 8 style guide
- [ ] Use type hints for function signatures
- [ ] Write docstrings for public functions
- [ ] Keep functions small and focused
- [ ] Use virtual environments for projects
