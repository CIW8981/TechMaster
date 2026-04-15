---
title: "DynamoDB - AWS NoSQL Database"
description: "Comprehensive guide to AWS DynamoDB including features, use cases, and best practices"
tags:
  - aws
  - databases
  - dynamodb
  - nosql
certification:
  - solutions-architect
  - developer
  - sysops
difficulty: intermediate
last_updated: "2026-02-20"
---

# DynamoDB

> **Service Overview**  
> Amazon DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability.

## Overview

DynamoDB is a key-value and document database that delivers single-digit millisecond performance at any scale. It's a fully managed, multi-region, multi-active, durable database with built-in security, backup and restore, and in-memory caching for internet-scale applications.

## Key Features

- **Fully Managed**: No servers to provision, patch, or manage
- **Performance at Scale**: Single-digit millisecond latency at any scale
- **Flexible Schema**: Store structured, semi-structured, or unstructured data
- **Built-in Security**: Encryption at rest and in transit, fine-grained access control
- **Global Tables**: Multi-region, fully replicated tables for global applications
- **Point-in-Time Recovery**: Continuous backups for the last 35 days
- **DynamoDB Streams**: Capture item-level changes in real-time

## Use Cases

### Use Case 1: Web and Mobile Applications

High-traffic web and mobile applications requiring consistent, low-latency data access at any scale.

### Use Case 2: Gaming Leaderboards

Real-time gaming applications with leaderboards, player data, and session information.

### Use Case 3: IoT Data Storage

Storing and querying time-series data from IoT devices with high write throughput.

---

# AWS DynamoDB - Questions

## Level 1: Fundamental Concepts (What is it?)

### 1. What problem does DynamoDB solve that traditional databases cannot?

DynamoDb solve performance at any scale, that traditional database struggle with

**Traditional Databases (SQL) Problem:**

- Performance degrades as data grows (millions → billions of rows)
- Vertical scaling has limits (bigger servers get exponentially expensive)
- Horizontal scaling (sharding) requires manual intervention and complex application logic

**DynamoDB's Solution:**

- Automatic horizontal scaling
- No Server management

**Real-world scenario:**

- Traditional DB: Black Friday traffic spike → database crashes or slows to 5+ seconds per query
- DynamoDB: Same spike → still responds in 5-10 milliseconds per request

### 2. Why does DynamoDB exist? What fundamental need does it address?

It's built for the reality that availability and speed are more valuable than perfect data consistency for most internet-scale applications.

**The Fundamental Shift:**

- **Traditional databases ask**: "How do we make one powerful database handle everything?"
- **DynamoDB asks**: "How do we make hundreds of simple databases work together seamlessly?"

**Bottom Line:**

DynamoDB exists because businesses can't afford downtime. It addresses the need for databases that are:

- Always available (99.99%+ uptime)
- Automatically scalable (no manual intervention)
- Predictably fast (regardless of load)
- Self-healing (automatic failure recovery)

### 3. What is the most basic unit of data in DynamoDB?

The most basic unit of data in DynamoDB is an Item.

**Think of it like:**

- DynamoDB → Item
- SQL database → Row

A collection of attributes (key-value pairs) that represents a single entity.

**Example:**

```json
{
  "UserID": "12345",
  "Name": "John Doe",
  "Email": "john@example.com",
  "Age": 30
}
```

**Key Characteristics:**

- **Must have a primary key** (partition key, or partition key + sort key)
- **Schema-less** - Each item can have different attributes
- **Max size: 400KB** per item
- **Attributes** are the name-value pairs within an item

**Why "Item" and not "Row"?**

Because unlike SQL rows (which must follow a fixed schema), DynamoDB items are flexible - each item in the same table can have completely different attributes (except for the required primary key).

### 4. How does DynamoDB physically store data? (distributed vs centralized)
 DynamoDB stores data in a distributed manner, not centralized.

Physical Storage Model:

Your Table
    ↓
Partitions (distributed across multiple servers)
    ↓
Each Partition = Physical storage node holding a subset of your data
    ↓
Replicated 3x across different Availability Zones


How It Works:

1. Partitioning (Horizontal Distribution)
   • Data is split across multiple physical storage nodes called "partitions"
   • Each partition holds a range of partition key values
   • Partitions are distributed across many servers

2. Hash-Based Distribution


   Your Item's Partition Key → Hash Function → Determines which partition stores it

   Example:
   UserID: "12345" → Hash → Partition 7
   UserID: "67890" → Hash → Partition 23



3. Replication (3 copies)
   • Each partition is automatically replicated to 3 different Availability Zones
   • If one data center fails, your data is still available in 2 others

Visual:
Availability Zone 1    Availability Zone 2    Availability Zone 3
    Partition A            Partition A            Partition A
    Partition B            Partition B            Partition B
    Partition C            Partition C            Partition C


Why Distributed?
• **Scalability** - Add more partitions as data grows
• **Performance** - Parallel processing across multiple servers
• **Availability** - No single point of failure
• **Fault tolerance** - Server failures don't cause data loss

### 5. What makes DynamoDB "NoSQL"? What does it NOT do that SQL databases do?
 DynamoDB is "NoSQL" because it doesn't use SQL query language and sacrifices relational features for performance and scale.

What DynamoDB Does NOT Do:

1. No JOINs
sql
-- SQL: Can do this
SELECT users.name, orders.total
FROM users JOIN orders ON users.id = orders.user_id

-- DynamoDB: Cannot do this
-- Must fetch users and orders separately or denormalize data


2. No Complex Queries
sql
-- SQL: Can do this
SELECT * FROM users
WHERE age > 25 AND city = 'Seattle' AND status = 'active'

-- DynamoDB: Cannot query on arbitrary attributes
-- Can only query on partition key (+ optional sort key)


3. No Schema Enforcement
sql
-- SQL: Table has fixed columns
CREATE TABLE users (id INT, name VARCHAR(50), email VARCHAR(100))
-- Every row must have these exact columns

-- DynamoDB: No fixed schema
-- Item 1: {id: "1", name: "John", email: "john@example.com"}
-- Item 2: {id: "2", name: "Jane", age: 30, city: "NYC"}  ← Different attributes OK


4. No Aggregations (without scanning)
sql
-- SQL: Easy
SELECT COUNT(*), AVG(price), SUM(total) FROM orders

-- DynamoDB: Must scan entire table (expensive) or track separately


5. No Foreign Keys / Referential Integrity
sql
-- SQL: Database enforces relationships
FOREIGN KEY (user_id) REFERENCES users(id)

-- DynamoDB: No enforcement
-- You can delete a user and orphan their orders


6. No Transactions Across Tables (limited)
sql
-- SQL: ACID transactions across multiple tables
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- DynamoDB: Transactions exist but limited (max 100 items, same region)


7. No Ad-Hoc Queries
sql
-- SQL: Can query anything anytime
SELECT * FROM users WHERE last_login < '2025-01-01'

-- DynamoDB: Must design table for specific access patterns upfront
-- Need to know your queries BEFORE creating the table


What "NoSQL" Really Means for DynamoDB:
• **Key-value access** instead of relational queries
• **Denormalized data** instead of normalized tables with JOINs
• **Flexible schema** instead of rigid structure
• **Partition key-based access** instead of arbitrary WHERE clauses
• **Eventual consistency** instead of always strongly consistent

The Trade-off:
• Give up: Query flexibility, JOINs, complex filtering
• Get: Predictable millisecond performance, infinite scale, high availability

Bottom Line: DynamoDB is "NoSQL" because it's optimized for fast key-value lookups at scale, not flexible relational queries.

## Level 2: Fundamental Concepts (What is it?)

### 6. What is a partition key and why is it absolutely necessary?

partition key is the attribute that DynamoDB uses to determine where to physically store your data.
#### Distribution & Scalability
Good partition key:
UserID → Evenly distributes data across partitions
User1 → Partition A
User2 → Partition B
User3 → Partition C

Bad partition key:
Country → Uneven distribution
USA → Partition A (90% of data - HOT PARTITION)
Canada → Partition B (5% of data)
Mexico → Partition C (5% of data)

Analogy:
Think of a library with 1000 rooms:
• **Partition Key** = Room number on a book
• Without it, you'd search all 1000 rooms
• With it, you go directly to the right room

Bottom Line:
The partition key is absolutely necessary because it's the addressing system for distributed storage. Without it, DynamoDB can't:
• Know where to store data
• Know where to retrieve data
• Distribute data evenly
• Guarantee fast performance

### 7. How does DynamoDB know WHERE to store your data?
DynamoDB uses a hash function on your partition key to determine where to store data.

The Process:

Step 1: You provide partition key
Item: {UserID: "12345", Name: "John"}
       ↓
Step 2: DynamoDB applies hash function
Hash("12345") = 8472619384756291847
       ↓
Step 3: Maps hash to partition
8472619384756291847 % Number_of_Partitions = Partition 7
       ↓
Step 4: Stores on that partition's servers
Partition 7 → Server A (AZ-1), Server B (AZ-2), Server C (AZ-3)


Concrete Example:

Your table has 10 partitions (0-9)

Write Item 1:
UserID: "alice" → Hash → 12847... → Mod 10 → Partition 2

Write Item 2:
UserID: "bob" → Hash → 98234... → Mod 10 → Partition 8

Write Item 3:
UserID: "charlie" → Hash → 45621... → Mod 10 → Partition 2


Key Properties of the Hash Function:

1. Deterministic - Same input always produces same output
   • "alice" always goes to Partition 2
   • Enables fast retrieval

2. Uniform Distribution - Spreads data evenly
   • Good partition keys → Even distribution across partitions
   • Bad partition keys → Hot spots

3. One-way - Can't reverse engineer the partition key from hash
   • Security benefit

Reading Data:

Query: Get item with UserID = "alice"
       ↓
Hash("alice") → Partition 2
       ↓
DynamoDB goes directly to Partition 2
       ↓
Returns item in milliseconds


Why This Matters:

• **No searching** - Direct lookup, not scanning
• **Predictable performance** - Always one hash calculation
• **Automatic distribution** - Hash function handles load balancing
• **Scalability** - Add more partitions, rehash data automatically

The Formula:
Partition = Hash(PartitionKey) mod NumberOfPartitions


Bottom Line: DynamoDB doesn't "search" for where to store data - it calculates the exact location using a hash function. This is why partition key access is so fast.

### 10. Why does DynamoDB use hash functions for partition keys?

Instant Location Lookup (O(1) Performance)

Without Hash (need to search):
"Where is UserID 12345?"
→ Check Partition 1? No
→ Check Partition 2? No
→ Check Partition 3? Yes! (slow)

Bottom Line:

Hash functions enable:
• **Even distribution** - No hot spots
• **Fast lookup** - O(1) direct access
• **Scalability** - Works with any number of partitions
• **Predictability** - Same key always goes to same place

Without hashing, DynamoDB would need to search or maintain complex indexes, destroying its performance guarantees.

### 11. What is a sort key and what fundamental problem does it solve?
A sort key (also called range key) solves the problem of storing and querying multiple related items efficiently.

The Fundamental Problem:

With partition key only:
- Can only store ONE item per partition key value
- Can't group related items together
- Can't query ranges or ordered data

Example problem:
UserID: "alice" → Can only store one item for alice


What Sort Key Solves:

1. Multiple Items Per Partition Key

Without sort key:
UserID: "alice" → One item only

With sort key:
UserID: "alice", OrderID: "order-001" → Item 1
UserID: "alice", OrderID: "order-002" → Item 2
UserID: "alice", OrderID: "order-003" → Item 3
↓
All stored together in same partition, sorted by OrderID


2. Range Queries

Query: Get all orders for alice between dates

Partition Key: UserID = "alice"
Sort Key: OrderDate BETWEEN "2026-01-01" AND "2026-01-31"

Returns all matching items in one efficient query


3. Ordered Storage

Items with same partition key are physically stored sorted by sort key:

Partition 7 (UserID: "alice"):
├─ OrderDate: "2026-01-15" → {order details}
├─ OrderDate: "2026-01-20" → {order details}
└─ OrderDate: "2026-02-10" → {order details}
     ↑
Automatically sorted on disk


Real-World Example:

Social Media App - User Posts

Partition Key: UserID
Sort Key: Timestamp

UserID: "alice", Timestamp: "2026-02-01T10:00:00" → Post 1
UserID: "alice", Timestamp: "2026-02-05T14:30:00" → Post 2
UserID: "alice", Timestamp: "2026-02-10T09:15:00" → Post 3

Query: "Get alice's last 10 posts"
→ Query UserID="alice", sort by Timestamp DESC, limit 10
→ Fast! All data in same partition, already sorted


What You Can Do With Sort Keys:

Operators:
- = (equals)
- < (less than)
- > (greater than)
- <= (less than or equal)
- >= (greater than or equal)
- BETWEEN
- begins_with (for strings)

Example:
Get orders where OrderID begins_with "2026-01"


The Key Insight:

Composite Primary Key = Partition Key + Sort Key

Partition Key → WHERE to store (which partition)
Sort Key → HOW to organize within that partition


Storage Layout:

Partition 7:
  UserID: "alice"
    ├─ SortKey: "A" → Item
    ├─ SortKey: "B" → Item
    └─ SortKey: "C" → Item

Partition 23:
  UserID: "bob"
    ├─ SortKey: "X" → Item
    └─ SortKey: "Y" → Item


Why It's Fundamental:

Without sort keys, you'd need:
• Separate items for each piece of data (inefficient)
• Multiple queries to get related data (slow)
• Application-side sorting (expensive)
• No way to query ranges efficiently

Bottom Line:

Sort key solves: "How do I store and query multiple related items together efficiently?"

It enables:
• One-to-many relationships
• Range queries
• Ordered data retrieval
• Efficient grouping of related items


#### Library Analogy for Sort Key:

Library with 1000 Rooms:

Partition Key = Room Number (which room)
Sort Key = Shelf Position (where in the room)


Without Sort Key (Partition Key Only):

Room 42 → Can only store ONE book
Room 43 → Can only store ONE book
Room 44 → Can only store ONE book

Problem: What if you have 50 books by the same author?
→ Need 50 different rooms!
→ Inefficient, scattered, hard to find related books


With Sort Key (Partition Key + Sort Key):

Room 42 (Author: "Stephen King")
  ├─ Shelf A1 → "Carrie" (1974)
  ├─ Shelf A2 → "The Shining" (1977)
  ├─ Shelf A3 → "It" (1986)
  ├─ Shelf A4 → "Misery" (1987)
  └─ Shelf A5 → "The Stand" (1990)

All Stephen King books in ONE room, organized by year on shelves


Real DynamoDB Example:

Table: Books

Partition Key: Author
Sort Key: PublicationYear

Items:
Author: "Stephen King", Year: 1974 → {Title: "Carrie", Pages: 199}
Author: "Stephen King", Year: 1977 → {Title: "The Shining", Pages: 447}
Author: "Stephen King", Year: 1986 → {Title: "It", Pages: 1138}
Author: "Stephen King", Year: 1987 → {Title: "Misery", Pages: 320}


Queries You Can Do:

1. Get all books by Stephen King:
   Room: "Stephen King" → Returns all shelves in that room

2. Get books by Stephen King from 1980-1990:
   Room: "Stephen King", Shelves: 1980 to 1990
   → Returns only shelves A3, A4, A5

3. Get Stephen King's 3 earliest books:
   Room: "Stephen King", Sort by Year ASC, Limit 3
   → Returns shelves A1, A2, A3

4. Get books published after 1985:
   Room: "Stephen King", Shelves: Year > 1985
   → Returns shelves A3, A4, A5


Physical Storage:

Partition 7 (Room for "Stephen King"):
┌─────────────────────────────────────┐
│ Shelf A1: 1974 - Carrie            │
│ Shelf A2: 1977 - The Shining       │
│ Shelf A3: 1986 - It                │
│ Shelf A4: 1987 - Misery            │
│ Shelf A5: 1990 - The Stand         │
└─────────────────────────────────────┘
     ↑
All physically stored together, sorted by year


Why This Is Efficient:

Without Sort Key:
"Get all Stephen King books from 1980-1990"
→ Search all 1000 rooms
→ Check each book's author and year
→ SLOW

With Sort Key:
"Get all Stephen King books from 1980-1990"
→ Go to Room 42 (hash "Stephen King")
→ Look at shelves between 1980-1990
→ FAST (one room, specific shelves)


The Key Insight:

Partition Key (Room) = Groups related items together
Sort Key (Shelf) = Organizes items within the group

Together they create:
- Efficient storage (related items co-located)
- Fast range queries (already sorted)
- Logical organization (easy to find what you need)


Another Example - Music Library:

Room 15 (Artist: "The Beatles")
  ├─ Shelf 1963 → "Please Please Me"
  ├─ Shelf 1965 → "Help!"
  ├─ Shelf 1967 → "Sgt. Pepper's"
  └─ Shelf 1969 → "Abbey Road"

Query: "Get Beatles albums from the 60s"
→ Go to Room 15, check shelves 1960-1969
→ All albums right there, already sorted by year

If sort keys are the same, the second write overwrites the first. To store multiple items, make the sort key unique by:
• Adding more detail (date instead of year)
• Combining multiple attributes (year#title)
• Adding unique identifiers (year#ISBN)

**Key Rule:**
Primary Key = Partition Key + Sort Key
Must be UNIQUE across the entire table
Same primary key = Same item = Overwrite

Bottom Line:

• **Partition Key** = Which room (groups related items)
• **Sort Key** = Which shelf in that room (orders items within the group)
• Together = Find and organize multiple related items efficiently

### 12. How does DynamoDB achieve "single-digit millisecond" performance?


## Level 3: Data Modeling from First Principles

### 13. Why can't you JOIN tables in DynamoDB? What's the fundamental architectural reason?

DynamoDB can't do JOINs because of its distributed architecture - the data you'd need to join is scattered across different physical servers.

The Fundamental Architectural Reason:

1. Data is Partitioned Across Servers

SQL Database (Single Server):
┌─────────────────────────┐
│  Users Table            │
│  Orders Table           │  ← All data on same server
│  Products Table         │     JOIN is local operation
└─────────────────────────┘

DynamoDB (Distributed):
Server 1        Server 2        Server 3        Server 4
Users           Users           Orders          Orders
(PK: 1-100)     (PK: 101-200)   (PK: 1-50)      (PK: 51-100)
    ↑               ↑               ↑               ↑
Different physical locations - can't JOIN efficiently


Why This Architecture Exists:

DynamoDB's Design Goal: Single-digit millisecond latency

JOIN requires:
- Cross-server communication (network latency)
- Scanning multiple partitions (unpredictable time)
- Coordinating results (processing overhead)
- Waiting for slowest server (tail latency)

Result: Can't guarantee millisecond performance

Bottom Line:

JOINs are impossible in DynamoDB because:

1. Physical separation - Data is on different servers
2. Hash distribution - Related data intentionally scattered
3. Performance guarantee - Can't promise millisecond latency with cross-server operations
4. Architectural choice - Traded query flexibility for speed and scale

The Design Philosophy:

SQL: "Store data normalized, JOIN when querying"
     → Flexible queries, slower at scale

DynamoDB: "Store data denormalized, no JOINs needed"
          → Fast queries, less flexible


DynamoDB forces you to denormalize and duplicate data so each query hits only ONE partition on ONE server - maintaining its speed guarantee.


### 14. If you can't JOIN, how do you model relationships between entities?
Without JOINs, you model relationships by denormalizing data and using access pattern-driven design. Here are the main strategies:

1. Embed Related Data (Denormalization)

SQL (Normalized):
Users Table:
  UserID: 1, Name: "Alice"

Orders Table:
  OrderID: 101, UserID: 1, Total: 50

Need JOIN to get user name with order

DynamoDB (Denormalized):
Orders Table:
  OrderID: 101, UserID: 1, UserName: "Alice", Total: 50
                            ↑
                    Duplicate user data in order

One query gets everything - no JOIN needed


2. Composite Keys (Store Related Items Together)

Single Table Design:

PK: UserID, SK: ItemType#ID

UserID: "alice", SK: "USER#alice" → {Name: "Alice", Email: "..."}
UserID: "alice", SK: "ORDER#001" → {Total: 50, Date: "2026-01-15"}
UserID: "alice", SK: "ORDER#002" → {Total: 75, Date: "2026-02-01"}
UserID: "alice", SK: "ADDRESS#home" → {Street: "123 Main St"}

Query: PK="alice" → Gets user + all orders + addresses in ONE query


3. Adjacency List Pattern

Social Network - Users and Followers:

PK: EntityID, SK: RelatedEntityID

"alice", "USER" → {Name: "Alice", Bio: "..."}
"alice", "FOLLOWS#bob" → {FollowDate: "2026-01-01"}
"alice", "FOLLOWS#charlie" → {FollowDate: "2026-01-15"}

Query: PK="alice", SK begins_with "FOLLOWS"
→ Gets all people Alice follows


4. Duplicate Data Across Tables

Users Table:
PK: UserID
"alice" → {Name: "Alice", Email: "alice@example.com"}

Orders Table:
PK: OrderID
"order-001" → {UserID: "alice", UserName: "Alice", UserEmail: "alice@example.com"}
                                 ↑
                        Duplicate user info in orders


5. Multiple Queries (Application-Side JOIN)

Step 1: Query Orders table
OrderID: "order-001" → {UserID: "alice", Total: 50}

Step 2: Query Users table
UserID: "alice" → {Name: "Alice", Email: "..."}

Step 3: Combine in application code
Result: {OrderID: "order-001", Total: 50, UserName: "Alice"}

Trade-off: 2 queries instead of 1, but still fast (2x 5ms = 10ms)


6. Single Table Design (Advanced)

One table for entire application:

PK              SK                  Attributes
─────────────────────────────────────────────────────────
USER#alice      PROFILE             {Name: "Alice", Email: "..."}
USER#alice      ORDER#2026-01-15    {OrderID: "001", Total: 50}
USER#alice      ORDER#2026-02-01    {OrderID: "002", Total: 75}
ORDER#001       METADATA            {UserID: "alice", Total: 50}
ORDER#001       ITEM#product-1      {Quantity: 2, Price: 25}

Access patterns:
- Get user profile: PK="USER#alice", SK="PROFILE"
- Get user's orders: PK="USER#alice", SK begins_with "ORDER"
- Get order details: PK="ORDER#001"


Real-World Example: E-commerce

SQL Approach (3 tables, JOINs):
Users → Orders → OrderItems

DynamoDB Approach (1 table):

PK: CustomerID, SK: Type#ID

"cust-123", "CUSTOMER" → {Name: "Alice", Email: "..."}
"cust-123", "ORDER#2026-01-15#001" → {Total: 100, Status: "shipped"}
"cust-123", "ORDER#2026-02-01#002" → {Total: 50, Status: "pending"}

Query: Get customer and all orders
PK="cust-123" → Returns everything in one query


Handling Updates (The Trade-off):

Problem: If Alice changes her email, need to update multiple places

Solution 1: Accept eventual consistency
- Update user record
- Background job updates denormalized copies

Solution 2: Only denormalize immutable data
- Duplicate: UserName (rarely changes)
- Don't duplicate: Email (changes frequently)
- Store UserID, query separately if needed

Solution 3: DynamoDB Streams
- Update user record
- Stream triggers Lambda
- Lambda updates all related records


Pattern Selection Guide:

One-to-One: Embed in same item
User → Profile: Store profile attributes in user item

One-to-Many: Composite key
User → Orders: PK=UserID, SK=OrderID

Many-to-Many: Adjacency list or dual writes
Users ↔ Groups:
  PK="USER#alice", SK="GROUP#admins"
  PK="GROUP#admins", SK="USER#alice"

Frequently accessed together: Denormalize
Order + Customer name: Store name in order

Rarely accessed together: Separate queries
Order + Full customer profile: Query separately


Key Principles:

1. Design for your access patterns first
   "How will I query this data?"

2. Duplicate data to avoid JOINs
   Storage is cheap, queries are expensive

3. One query per access pattern
   Each query should hit one partition

4. Accept data duplication
   Trade storage space for query speed


Bottom Line:

Instead of JOINs, you:
• **Denormalize** - Duplicate data where needed
• **Co-locate** - Store related items together using composite keys
• **Pre-compute** - Structure data for how you'll query it
• **Accept duplication** - Storage is cheap, speed is valuable

The mindset shift: Design tables around queries, not entities.
Many-to-Many: User Belongs to Multiple Groups

Table Structure:

PK              SK              Attributes
─────────────────────────────────────────────────────────
USER#alice      METADATA        {Name: "Alice", Email: "alice@example.com"}
USER#alice      GROUP#admins    {JoinedDate: "2026-01-01", Role: "owner"}
USER#alice      GROUP#devs      {JoinedDate: "2026-01-15", Role: "member"}
USER#alice      GROUP#managers  {JoinedDate: "2026-02-01", Role: "member"}

GROUP#admins    METADATA        {Name: "Admins", Description: "..."}
GROUP#admins    USER#alice      {JoinedDate: "2026-01-01", Role: "owner"}
GROUP#admins    USER#bob        {JoinedDate: "2026-01-10", Role: "member"}

GROUP#devs      METADATA        {Name: "Developers", Description: "..."}
GROUP#devs      USER#alice      {JoinedDate: "2026-01-15", Role: "member"}
GROUP#devs      USER#charlie    {JoinedDate: "2026-01-20", Role: "member"}

GROUP#managers  METADATA        {Name: "Managers", Description: "..."}
GROUP#managers  USER#alice      {JoinedDate: "2026-02-01", Role: "member"}

### 15. What is the minimum information needed to retrieve an item in DynamoDB?
Minimum information = Complete Primary Key

- Partition key only table → 1 value
- Composite key table → 2 values (partition key + sort key)

### 16. Why are secondary indexes necessary? What limitation do they overcome?
Without secondary indexes, you have only two options to access data:

1. GetItem - retrieve by exact primary key (partition key + sort key if composite)
2. Query - search within a partition key, optionally filtering by sort key
3. Scan - read the entire table (expensive and slow)

The core limitation: If you need to query data by any attribute other than the primary key, you're forced to scan the
entire table.

Example scenario:

Table with primary key: UserID (partition key)
UserID | Email              | Country
123    | alice@example.com  | USA
456    | bob@example.com    | Canada
789    | carol@example.com  | USA


Without a secondary index:
• ✅ Query by UserID: efficient
• ❌ Query by Email: must scan entire table
• ❌ Query by Country: must scan entire table

Secondary indexes solve this by:

1. Global Secondary Index (GSI) - Creates an alternate partition key + optional sort key, spans entire table
2. Local Secondary Index (LSI) - Uses same partition key but different sort key, scoped to partition

With a GSI on Email:
• ✅ Query by Email: now efficient
• ✅ Query by UserID: still efficient
### 17. What is the trade-off when creating a Global Secondary Index?
When you create a GSI, you're essentially:

1. DUPLICATING the collection
• You create a second physical copy of books in a different room
• Organized by a different system (author name, publication date, etc.)
• Each GSI is a complete, separate structure

The Trade-offs:

STORAGE COST 📚
• Main hall: 1000 books
• Add GSI by author: now 2000 books total (duplicated)
• Add GSI by date: now 3000 books total
• You're paying rent for multiple rooms storing duplicate information

WRITE COST ✍️
• Someone donates a new book → you must:
  • Catalog it in the main hall
  • Catalog it in the author reference room
  • Catalog it in the date reference room
• Every write operation now costs 3x (1 base table + 2 GSIs)
• If someone updates a book's information, you update all copies

THROUGHPUT CAPACITY 🚪
• Each GSI has its own read/write capacity units
• Like each room having its own entrance with limited capacity
• A bottleneck in one GSI doesn't block the main table
• But you pay for capacity in each GSI separately

### 18. How would you design a table if you could only ask ONE question of your data?
The question dictates the primary key.

Example 1: "What are all orders for a specific customer?"
Partition Key: CustomerID
Sort Key: OrderDate

CustomerID | OrderDate           | OrderID | Amount
CUST123    | 2026-02-25T10:00   | ORD001  | 50.00
CUST123    | 2026-02-24T15:30   | ORD002  | 75.00
CUST456    | 2026-02-25T09:15   | ORD003  | 100.00


Example 2: "What is the current status of a specific order?"
Partition Key: OrderID
(No sort key needed)

OrderID | CustomerID | Status    | Amount
ORD001  | CUST123    | Shipped   | 50.00
ORD002  | CUST123    | Pending   | 75.00
ORD003  | CUST456    | Delivered | 100.00


Example 3: "What are all posts in a specific forum thread?"
Partition Key: ThreadID
Sort Key: Timestamp

ThreadID  | Timestamp          | PostID | Author
THREAD99  | 2026-02-25T10:00  | POST1  | Alice
THREAD99  | 2026-02-25T10:05  | POST2  | Bob
THREAD99  | 2026-02-25T10:10  | POST3  | Carol


The Design Principle:

1. Identify the access pattern - your ONE question
2. Extract the lookup value - becomes partition key
3. Extract the ordering/filtering - becomes sort key (if needed)
4. Everything else - just attributes

Why this works:
• No secondary indexes needed (no duplication cost)
• No scans needed (always efficient queries)
• Minimal write cost (only one location to update)
• Strong consistency available
• Simplest mental model

The hard truth: Real applications ask multiple questions, which is why DynamoDB design is challenging. But starting with
"if I could only ask ONE question" forces you to identify your most critical access pattern - and that should drive
your primary key design. Everything else becomes a GSI trade-off decision.



## Level 4: Capacity and Performance (Why these limits?)

19. What is a Read Capacity Unit (RCU) measuring at its core?
The fundamental unit:
1 RCU = 4KB of data read with strong consistency in 1 second

20. What is a Write Capacity Unit (WCU) measuring at its core?
21. Why does strongly consistent read cost 2x eventually consistent read?
22. What causes "hot partitions" and why is it a problem?
23. How does DynamoDB scale horizontally? What happens behind the scenes?
24. Why is there a 400KB limit on item size?