"""
Perfect. Before looking at the code, let's understand what the assignment is trying to teach.

This assignment is actually testing **two concepts**:

1. **Singleton Pattern**

   * Only one `ConnectionPoolImpl` object should exist.

2. **Connection Pool**

   * Maintain a collection of reusable connections.
   * Give connections when requested.
   * Take them back when released.

---

# Complete Implementation

```python
"""
from typing import Optional

from .connection_pool import ConnectionPool
from .database_connection import DatabaseConnection


class ConnectionPoolImpl(ConnectionPool):

    _instance = None

    def __init__(self, max_connections: int):
        self.max_connections = max_connections
        self.available_connections = []
        self.used_connections = []

        self.initialize_pool()

    @staticmethod
    def get_instance(max_connections: int) -> ConnectionPool:
        if ConnectionPoolImpl._instance is None:
            ConnectionPoolImpl._instance = ConnectionPoolImpl(
                max_connections
            )

        return ConnectionPoolImpl._instance

    @staticmethod
    def reset_instance() -> None:
        ConnectionPoolImpl._instance = None

    def initialize_pool(self) -> None:
        self.available_connections = []
        self.used_connections = []

        for _ in range(self.max_connections):
            connection = DatabaseConnection()
            self.available_connections.append(connection)

    def get_connection(self) -> Optional[DatabaseConnection]:
        if len(self.available_connections) == 0:
            return None

        connection = self.available_connections.pop(0)
        self.used_connections.append(connection)

        return connection

    def release_connection(
        self,
        connection: DatabaseConnection
    ) -> None:
        if connection in self.used_connections:
            self.used_connections.remove(connection)
            self.available_connections.append(connection)

    def get_available_connections_count(self) -> int:
        return len(self.available_connections)

    def get_total_connections_count(self) -> int:
        return (
            len(self.available_connections)
            + len(self.used_connections)
        )

"""
```

---

# Line By Line Explanation

---

## Class Variable

```python
_instance = None
```

### Why?

Singleton needs a place to store the single object.

Initially:

```python
ConnectionPoolImpl._instance = None
```

Meaning:

```text
No pool exists yet.
```

---

## Constructor

```python
def __init__(self, max_connections: int):
```

### Why?

Whenever a pool object is created, we need:

```text
Pool Size
Available Connections
Used Connections
```

---

### Store Maximum Size

```python
self.max_connections = max_connections
```

Example:

```python
ConnectionPoolImpl.get_instance(10)
```

Now:

```python
self.max_connections = 10
```

Meaning:

```text
Pool should contain 10 connections.
```

---

### Available Connections

```python
self.available_connections = []
```

### Why?

Store connections ready to use.

Initially:

```text
[]
```

After initialization:

```text
[conn1, conn2, conn3 ...]
```

---

### Used Connections

```python
self.used_connections = []
```

### Why?

Track borrowed connections.

Example:

```python
conn = pool.get_connection()
```

After:

```text
available = [conn2, conn3]
used = [conn1]
```

---

### Initialize Pool Immediately

```python
self.initialize_pool()
```

### Why?

The hidden tests expect the pool to already contain connections.

Without this:

```python
available_connections = []
```

Count becomes:

```python
0
```

Tests fail.

---

# get_instance()

```python
@staticmethod
def get_instance(max_connections: int) -> ConnectionPool:
```

### Why Static?

We need to get the object before any object exists.

Calling:

```python
ConnectionPoolImpl.get_instance(10)
```

does not require creating an object first.

---

### First Time

```python
if ConnectionPoolImpl._instance is None:
```

Check whether a pool already exists.

---

### Create Singleton

```python
ConnectionPoolImpl._instance = ConnectionPoolImpl(
    max_connections
)
```

Only the first call creates the object.

---

### Return Same Object

```python
return ConnectionPoolImpl._instance
```

Every call returns the same object.

Example:

```python
pool1 = ConnectionPoolImpl.get_instance(10)
pool2 = ConnectionPoolImpl.get_instance(20)
```

Result:

```python
pool1 is pool2
```

returns:

```python
True
```

---

# reset_instance()

```python
ConnectionPoolImpl._instance = None
```

### Why?

Used by tests.

Example:

```python
ConnectionPoolImpl.reset_instance()
```

Now Singleton is removed.

Next call:

```python
get_instance()
```

creates a new object.

---

# initialize_pool()

```python
def initialize_pool(self):
```

### Responsibility

Create all connections.

---

### Reset Existing State

```python
self.available_connections = []
self.used_connections = []
```

### Why?

Ensure clean initialization.

---

### Create Connections

```python
for _ in range(self.max_connections):
```

Example:

```python
max_connections = 10
```

Loop runs:

```text
10 times
```

---

### Create Connection

```python
connection = DatabaseConnection()
```

Creates:

```text
conn1
conn2
conn3
...
```

Each is a different object.

---

### Store As Available

```python
self.available_connections.append(connection)
```

Initially every connection is free.

---

# get_connection()

```python
def get_connection(self):
```

### Responsibility

Give one available connection.

---

### No Connection Left

```python
if len(self.available_connections) == 0:
    return None
```

### Why?

Method signature:

```python
Optional[DatabaseConnection]
```

means:

```python
DatabaseConnection
or
None
```

---

### Take Connection

```python
connection = self.available_connections.pop(0)
```

Example:

Before:

```text
[conn1, conn2, conn3]
```

After:

```text
[conn2, conn3]
```

---

### Mark As Used

```python
self.used_connections.append(connection)
```

Now:

```text
used = [conn1]
```

---

### Return Connection

```python
return connection
```

Caller receives:

```python
conn1
```

---

# release_connection()

```python
def release_connection(self, connection):
```

### Responsibility

Return borrowed connection.

---

### Verify It Was Borrowed

```python
if connection in self.used_connections:
```

### Why?

Only borrowed connections should be released.

---

### Remove From Used

```python
self.used_connections.remove(connection)
```

Before:

```text
used = [conn1]
```

After:

```text
used = []
```

---

### Add Back To Available

```python
self.available_connections.append(connection)
```

Before:

```text
available = [conn2, conn3]
```

After:

```text
available = [conn2, conn3, conn1]
```

Connection becomes reusable.

---

# get_available_connections_count()

```python
return len(self.available_connections)
```

### Why?

Available connections are exactly what is inside:

```python
self.available_connections
```

Example:

```text
[conn1, conn2, conn3]
```

Result:

```python
3
```

---

# get_total_connections_count()

```python
return (
    len(self.available_connections)
    + len(self.used_connections)
)
```

### Why?

Every connection is always in exactly one of two states:

```text
Available
or
Used
```

Therefore:

```text
Total
=
Available + Used
```

Example:

```text
available = 7
used = 3
```

Result:

```python
10
```

---

# Most Important Learning From This Assignment

The real goal was not connection pooling.

The real goal was understanding:

```text
State Management
```

The pool continuously moves objects between:

```text
available_connections
        ↓
used_connections
        ↓
available_connections
```

while Singleton ensures:

```text
Only one pool exists.
```

That combination is exactly what the assignment was testing.
"""