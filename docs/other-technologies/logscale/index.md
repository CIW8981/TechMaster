---
title: "CrowdStrike LogScale (Humio) - Practice Questions"
description: "Practice questions for LogScale basics and query language, bridging from SQL/RDBMS knowledge"
tags:
  - logscale
  - humio
  - observability
  - log-management
  - siem
difficulty: beginner
last_updated: "2026-06-04"
---

# CrowdStrike LogScale (Humio) - Practice Questions

!!! info "About This Guide"
    These questions are designed for someone with SQL/RDBMS experience who is new to LogScale Query Language (LQL). Each section maps familiar SQL concepts to their LogScale equivalents.

## Key Concepts: SQL vs LogScale

| SQL Concept | LogScale Equivalent |
|-------------|-------------------|
| `SELECT` columns | Field extraction (auto or with `parseJson`, regex) |
| `WHERE` clause | Filter expressions (e.g., `status=404`) |
| `GROUP BY` | `groupBy()` function |
| `COUNT(*)` | `count()` aggregate |
| `ORDER BY` | `sort()` function |
| `LIKE '%pattern%'` | `"*pattern*"` or `regex()` |
| `JOIN` | No direct equivalent (denormalized at ingest) |
| Tables | Repositories |
| Rows | Events |
| Columns | Fields |
| `DISTINCT` | `groupBy(field)` |
| `LIMIT` | `head()` or `tail()` |
| `HAVING` | Filter after `groupBy()` using `test()` |

---

## Section 1: LogScale Fundamentals

### Q1: What is LogScale?

??? question "Click to reveal answer"
    LogScale (formerly Humio) is a **log management and observability platform** built on a streaming architecture. Unlike traditional databases that index everything on write, LogScale uses:

    - **Schema-on-read**: No predefined schema; fields are extracted at query time
    - **Streaming queries**: Data is analyzed as it arrives
    - **Compression-based storage**: Uses minimal indexing, relies on brute-force search over compressed data

    **SQL analogy**: Imagine a database where you never run `CREATE TABLE` — you just insert JSON blobs and query any field on the fly.

### Q2: What is a Repository in LogScale?

??? question "Click to reveal answer"
    A **Repository** is the equivalent of a **database/table** in SQL. It's a logical container for events (log data).

    - Each repository has its own retention policy
    - Data is ingested into a specific repository
    - Queries run against one or more repositories
    - Repositories can have parsers attached to structure incoming data

### Q3: What is the difference between a Repository and a View?

??? question "Click to reveal answer"
    | | Repository | View |
    |---|---|---|
    | **What it is** | Stores actual data (events are ingested here) | A virtual layer that queries one or more repositories |
    | **Data** | Owns the data | References data from repositories |
    | **SQL analogy** | A table with actual rows | A SQL VIEW (read-only query over tables) |
    | **Ingest** | Yes, data lands here | No, cannot ingest data |
    | **Retention** | Has its own retention policy | Inherits from source repositories |
    | **Filters** | None (sees everything in the repo) | Can have a permanent filter applied |

    **How to check if you're in a Repository or View in the UI:**

    1. **Look at the icon** next to the name in the header:
        - Repository = database/cylinder icon
        - View = eye icon or layered/stacked icon

    2. **Go to Settings** (gear icon in the sidebar):
        - If you see **Ingest Tokens**, **Parsers**, **Retention** → it's a **Repository**
        - If you see **Connections** (list of source repositories) and no ingest options → it's a **View**

    3. **Check the dropdown** — click on the name at the top. The dropdown labels items as "Repository" or "View".

    **Example**: A URL like `https://logscale.example.com/mdlz_networks/search` — `mdlz_networks` could be a View that aggregates logs from multiple repositories (`firewall_logs`, `vpc_flow_logs`, `dns_logs`) into one searchable interface for the network team.

    **Typical pattern in organizations:**

    - **Repositories**: `firewall_logs`, `vpc_flow_logs`, `dns_logs` (raw data ingested here)
    - **Views**: `networks_combined` (queries across multiple repos, team-scoped access)

### Q4: What is an Event in LogScale?

??? question "Click to reveal answer"
    An **Event** is the equivalent of a **row** in SQL. It represents a single log entry with:

    - A **timestamp** (`@timestamp`) — always present
    - A **raw string** (`@rawstring`) — the original log line
    - **Fields** — extracted key-value pairs (like columns, but dynamic)

    Unlike SQL rows, events don't need to share the same fields. One event might have `statusCode` while another has `errorMessage`.

### Q4: What is the difference between schema-on-write (SQL) and schema-on-read (LogScale)?

??? question "Click to reveal answer"
    | | Schema-on-Write (SQL) | Schema-on-Read (LogScale) |
    |---|---|---|
    | **When** | Define structure before inserting data | Define structure when querying |
    | **Flexibility** | Must ALTER TABLE to add columns | New fields appear automatically |
    | **Performance** | Fast reads (indexed) | Fast writes (no indexing overhead) |
    | **Trade-off** | Rigid but predictable | Flexible but query-time cost |

### Q5: How do you identify Tags in LQL?

??? question "Click to reveal answer"
    **Tags are identified by the `#` prefix** in LogScale queries.

    ```humio
    #host = "webserver01"
    #source = "/var/log/syslog"
    #type = "accesslog"
    ```

    **Tags vs Regular Fields:**

    | | Tags | Regular Fields |
    |---|---|---|
    | Prefix | `#fieldname` | `fieldname` (no prefix) |
    | Indexed | Yes (fast lookup) | No (scanned at query time) |
    | Set at | Ingest time by parsers | Extracted at ingest or query time |
    | Performance | Filters data segments before scanning | Requires scanning events |

    **How to spot them:**

    - In the **UI sidebar**, tags appear in the "Tags" section of a repository
    - In **queries**, anything prefixed with `#` is a tag
    - In **parser configurations**, fields assigned as tags are declared explicitly

    **Checking available tags:**
    ```humio
    #type=*
    | groupBy(#type)
    ```

    **SQL analogy**: Tags are like a **partitioned/indexed column** — filtering on `#host="web01"` skips irrelevant data partitions entirely, while filtering on a regular field like `statusCode=404` requires scanning all events within the time range.

    **Rule of thumb**: Use tags for low-cardinality fields that you filter on frequently (host, source type, environment). Don't tag high-cardinality fields (user IDs, request IDs) — it degrades performance.

---

## Section 2: Basic Query Syntax

### Q6: How do you search for all events containing the word "error"?

??? question "Click to reveal answer"
    ```humio
    error
    ```

    A bare word performs a **free-text search** across `@rawstring`.

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs WHERE rawstring LIKE '%error%';
    ```

### Q7: How do you filter events where `statusCode` equals 404?

??? question "Click to reveal answer"
    ```humio
    statusCode=404
    ```

    Or with quotes for string values:
    ```humio
    statusCode="404"
    ```

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs WHERE statusCode = 404;
    ```

### Q8: How do you combine multiple filters (AND logic)?

??? question "Click to reveal answer"
    **Piping** (`|`) or space-separated filters (implicit AND):

    ```humio
    statusCode=500 | method="POST"
    ```

    Or:
    ```humio
    statusCode=500 method="POST"
    ```

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs WHERE statusCode = 500 AND method = 'POST';
    ```

### Q9: How do you perform OR logic in LogScale?

??? question "Click to reveal answer"
    Use the `or` operator:

    ```humio
    statusCode=404 or statusCode=500
    ```

    Or use `in()` for multiple values:
    ```humio
    statusCode=in(values=[404, 500, 503])
    ```

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs WHERE statusCode IN (404, 500, 503);
    ```

### Q10: How do you negate a filter (NOT logic)?

??? question "Click to reveal answer"
    Use `!=` or the `not` operator:

    ```humio
    statusCode!=200
    ```

    Or:
    ```humio
    not statusCode=200
    ```

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs WHERE statusCode != 200;
    ```

### Q11: How do you search with wildcards?

??? question "Click to reveal answer"
    Use `*` for wildcards:

    ```humio
    url="/api/v1/*"
    ```

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs WHERE url LIKE '/api/v1/%';
    ```

---

## Section 3: Aggregation & Grouping

### Q12: How do you count all events?

??? question "Click to reveal answer"
    ```humio
    count()
    ```

    **SQL equivalent**:
    ```sql
    SELECT COUNT(*) FROM logs;
    ```

### Q13: How do you count events grouped by `statusCode`?

??? question "Click to reveal answer"
    ```humio
    groupBy(statusCode, function=count())
    ```

    **SQL equivalent**:
    ```sql
    SELECT statusCode, COUNT(*) FROM logs GROUP BY statusCode;
    ```

### Q14: How do you get the top 5 most common URLs?

??? question "Click to reveal answer"
    ```humio
    top(url, limit=5)
    ```

    Or explicitly:
    ```humio
    groupBy(url, function=count()) | sort(_count, order=desc) | head(5)
    ```

    **SQL equivalent**:
    ```sql
    SELECT url, COUNT(*) as cnt FROM logs GROUP BY url ORDER BY cnt DESC LIMIT 5;
    ```

### Q15: How do you calculate the average response time?

??? question "Click to reveal answer"
    ```humio
    avg(responseTime)
    ```

    With grouping:
    ```humio
    groupBy(endpoint, function=avg(responseTime))
    ```

    **SQL equivalent**:
    ```sql
    SELECT endpoint, AVG(responseTime) FROM logs GROUP BY endpoint;
    ```

### Q16: How do you get min, max, and percentiles?

??? question "Click to reveal answer"
    ```humio
    min(responseTime)
    max(responseTime)
    percentile(field=responseTime, percentiles=[50, 95, 99])
    ```

    Combined in a groupBy:
    ```humio
    groupBy(service, function=[count(), avg(responseTime), percentile(field=responseTime, percentiles=[95, 99])])
    ```

### Q17: How do you use HAVING-like filtering (filter after aggregation)?

??? question "Click to reveal answer"
    Use `test()` after aggregation:

    ```humio
    groupBy(url, function=count()) | test(_count > 100)
    ```

    **SQL equivalent**:
    ```sql
    SELECT url, COUNT(*) as cnt FROM logs GROUP BY url HAVING COUNT(*) > 100;
    ```

---

## Section 4: Sorting, Limiting & Field Selection

### Q18: How do you sort results?

??? question "Click to reveal answer"
    ```humio
    sort(responseTime, order=desc)
    ```

    Sort by multiple fields:
    ```humio
    sort(field=[statusCode, responseTime], order=[asc, desc])
    ```

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs ORDER BY statusCode ASC, responseTime DESC;
    ```

### Q19: How do you limit results (like SQL LIMIT)?

??? question "Click to reveal answer"
    ```humio
    head(10)
    ```

    For the last N events:
    ```humio
    tail(10)
    ```

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs ORDER BY @timestamp DESC LIMIT 10;
    ```

### Q20: How do you select specific fields (like SQL SELECT)?

??? question "Click to reveal answer"
    Use `select()` or `table()`:

    ```humio
    select([@timestamp, statusCode, url, responseTime])
    ```

    For display in a table widget:
    ```humio
    table([@timestamp, statusCode, url, responseTime])
    ```

    **SQL equivalent**:
    ```sql
    SELECT timestamp, statusCode, url, responseTime FROM logs;
    ```

### Q21: How do you rename a field (like SQL AS)?

??? question "Click to reveal answer"
    Use the `rename()` function:

    ```humio
    rename(responseTime, as=latency)
    ```

    **SQL equivalent**:
    ```sql
    SELECT responseTime AS latency FROM logs;
    ```

---

## Section 5: String & Regex Operations

### Q22: How do you use regex to extract fields?

??? question "Click to reveal answer"
    ```humio
    regex("(?<ip>\d+\.\d+\.\d+\.\d+)\s+(?<method>\w+)\s+(?<url>\S+)")
    ```

    This extracts named groups into fields.

    **SQL analogy**: Like `REGEXP_SUBSTR` but creates new columns dynamically.

### Q23: How do you do case-insensitive search?

??? question "Click to reveal answer"
    ```humio
    regex("error", flags="i")
    ```

    Or for field matching:
    ```humio
    message = /error/i
    ```

### Q24: How do you parse JSON fields?

??? question "Click to reveal answer"
    If your log lines are JSON:
    ```humio
    parseJson()
    ```

    Parse a specific field containing JSON:
    ```humio
    parseJson(field=metadata)
    ```

    This automatically extracts all JSON keys as fields — no schema definition needed.

### Q25: How do you use `replace()` for string manipulation?

??? question "Click to reveal answer"
    ```humio
    replace(field=url, regex="/api/v[0-9]+/", with="/api/")
    ```

    **SQL equivalent**:
    ```sql
    SELECT REGEXP_REPLACE(url, '/api/v[0-9]+/', '/api/') FROM logs;
    ```

---

## Section 6: Time-Based Queries

### Q26: How does time filtering work in LogScale?

??? question "Click to reveal answer"
    Time is selected via the **time picker** in the UI (last 5m, 1h, 24h, 7d, custom range). You can also filter in query:

    ```humio
    @timestamp > now() - 1h
    ```

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs WHERE timestamp > NOW() - INTERVAL '1 hour';
    ```

### Q27: How do you create time-series buckets (like date_trunc in SQL)?

??? question "Click to reveal answer"
    Use `bucket()` for time-based aggregation:

    ```humio
    bucket(span=5m, function=count())
    ```

    Bucket by a field and time:
    ```humio
    bucket(span=1h, field=statusCode, function=count())
    ```

    **SQL equivalent**:
    ```sql
    SELECT date_trunc('hour', timestamp), statusCode, COUNT(*)
    FROM logs
    GROUP BY date_trunc('hour', timestamp), statusCode;
    ```

### Q28: How do you calculate rate of events over time?

??? question "Click to reveal answer"
    ```humio
    bucket(span=1m, function=count())
    | rate := _count / 60
    ```

    Or use the built-in timeChart:
    ```humio
    timeChart(span=1m, function=count())
    ```

---

## Section 7: Field Manipulation & Computed Fields

### Q29: How do you create a computed/calculated field?

??? question "Click to reveal answer"
    Use `:=` assignment:

    ```humio
    duration_ms := responseTime * 1000
    ```

    Conditional assignment:
    ```humio
    status_category := if(statusCode < 300, then="success", else="failure")
    ```

    **SQL equivalent**:
    ```sql
    SELECT *, responseTime * 1000 AS duration_ms,
           CASE WHEN statusCode < 300 THEN 'success' ELSE 'failure' END AS status_category
    FROM logs;
    ```

### Q30: How do you check if a field exists?

??? question "Click to reveal answer"
    ```humio
    errorMessage=*
    ```

    To find events where a field does NOT exist:
    ```humio
    not errorMessage=*
    ```

    **SQL equivalent**:
    ```sql
    SELECT * FROM logs WHERE errorMessage IS NOT NULL;
    SELECT * FROM logs WHERE errorMessage IS NULL;
    ```

---

## Section 8: Joins, Lookups & Combining Data

### Q31: Does LogScale support JOINs like SQL?

??? question "Click to reveal answer"
    **No direct JOINs**. LogScale is designed for denormalized event data. Alternatives:

    1. **Lookup files** (like a dimension table):
    ```humio
    match(file="ip-to-hostname.csv", field=src_ip, column=ip)
    ```

    2. **Saved queries** as building blocks (like views/CTEs)

    3. **Enrichment at ingest time** — add context fields when data arrives

    **Key mindset shift**: Denormalize at ingest time rather than normalizing and joining at query time.

### Q32: How do lookup files work?

??? question "Click to reveal answer"
    Lookup files are CSV files uploaded to a repository acting like **reference/dimension tables**:

    ```humio
    match(file="users.csv", field=userId, column=id, include=[name, department])
    ```

    **SQL equivalent**:
    ```sql
    SELECT l.*, u.name, u.department
    FROM logs l
    LEFT JOIN users u ON l.userId = u.id;
    ```

### Q33: How do you achieve SQL UNION in LogScale?

??? question "Click to reveal answer"
    LogScale does **not** have a direct `UNION` operator. Workarounds:

    **Option 1: Use `or` (same data, different filters):**
    ```humio
    (statusCode=404 url="/api/*") or (statusCode=500 method="POST")
    ```

    **Option 2: Use `case{}` to tag and merge different pipelines:**
    ```humio
    case {
      statusCode>=500 | source:="server_errors" ;
      statusCode>=400 statusCode<500 | source:="client_errors" ;
    }
    | table([@timestamp, source, statusCode, url])
    ```

    **Option 3: `case{}` with field renaming (unify different column names):**
    ```humio
    case {
      type="firewall" | src := sourceIP | dst := destIP ;
      type="loadbalancer" | src := clientIP | dst := backendIP ;
    }
    | table([@timestamp, src, dst, type])
    ```

    **SQL equivalent of Option 3:**
    ```sql
    SELECT timestamp, sourceIP as src, destIP as dst, 'firewall' as type FROM firewall_logs
    UNION ALL
    SELECT timestamp, clientIP as src, backendIP as dst, 'loadbalancer' as type FROM lb_logs;
    ```

    | SQL | LogScale Equivalent |
    |-----|-------------------|
    | `UNION` (same table, different filters) | `or` operator |
    | `UNION` (different columns, rename to match) | `case{}` + field assignment (`:=`) |
    | `UNION` (across tables) | Use a **View** spanning multiple repos |

### Q34: Can you combine multiple queries where some are filters and one is an aggregation?

??? question "Click to reveal answer"
    **No — all results in a single query must have the same shape.** You cannot mix raw events with aggregated output.

    **Example problem:**
    ```
    Query 1: #type="firewall" action="DENY"     → returns events (rows)
    Query 2: #type="vpn" status="failed"        → returns events (rows)
    Query 3: #type="firewall" | count()         → returns a single number
    ```

    These can't be combined because queries 1 & 2 produce event lists while query 3 produces an aggregate.

    **Solution A: Make all three event-level (use `case{}`):**
    ```humio
    case {
      #type="firewall" action="DENY" | source:="firewall_deny" ;
      #type="vpn" status="failed" | source:="vpn_failed" ;
      #type="firewall" statusCode>=500 | source:="firewall_errors" ;
    }
    | table([@timestamp, source, #type, action, status])
    ```

    **Solution B: Make all three aggregations (same shape):**
    ```humio
    case {
      #type="firewall" action="DENY" | category:="firewall_deny" ;
      #type="vpn" status="failed" | category:="vpn_failed" ;
      #type="firewall" | category:="firewall_total" ;
    }
    | groupBy(category, function=count())
    ```

    Result:
    ```
    category         | _count
    -----------------+-------
    firewall_deny    | 342
    vpn_failed       | 56
    firewall_total   | 12049
    ```

    **Solution C: Use a Dashboard (most common in practice):**

    Create a dashboard with **3 separate panels** — each runs its own query independently. This is the standard way to display different "shapes" of data together.

    **Key rule**: A single LogScale query = one result shape. This is the same in SQL — you can't `UNION` a `SELECT *` with a `SELECT COUNT(*)`.

### Q35: Real-World Example — How to combine separate aggregations into one result (e.g., Cisco ISE metrics)?

??? question "Click to reveal answer"
    **Scenario**: You want three metrics from Cisco ISE logs displayed as rows:

    ```humio
    // Query 1: Unique failed MACs
    #type=cisco-ise "log_type"="Failed_Attempts"
    | count(field="Calling-Station-ID", distinct=true, as=count)

    // Query 2: Unique passed MACs
    #type=cisco-ise "log_type"="Passed_Authentications"
    | count(field="Calling-Station-ID", distinct=true, as=count)

    // Query 3: Average auth response time
    #type=cisco-ise ("log_type"="Passed_Authentications" or "log_type"="Failed_Attempts")
    | avg(RequestLatency, as=AVG_Auth_Response)
    ```

    **In SQL you'd simply UNION them:**
    ```sql
    SELECT 'Failed_Unique_MACs' as metric, COUNT(DISTINCT calling_station_id) as value
    FROM logs WHERE log_type = 'Failed_Attempts'
    UNION ALL
    SELECT 'Passed_Unique_MACs', COUNT(DISTINCT calling_station_id)
    FROM logs WHERE log_type = 'Passed_Authentications'
    UNION ALL
    SELECT 'AVG_Auth_Response', AVG(RequestLatency)
    FROM logs WHERE log_type IN ('Passed_Authentications', 'Failed_Attempts');
    ```

    **In LogScale this is NOT possible in a single query** because:

    - `case{}` routes events **before** aggregation — not after
    - `or` combines filters on events, not aggregation results
    - Piping (`|`) is sequential — after aggregation, original fields are gone
    - There is no post-aggregation UNION operator

    ```
    SQL:      aggregate → aggregate → aggregate → UNION (stack results)
    LogScale: tag events → single aggregation pass → done
    ```

    **Why every approach fails:**

    | Approach | Why It Doesn't Work |
    |----------|-------------------|
    | `case{}` after aggregation | Only 1 summary row exists, nothing to route |
    | Pipe results together | Pipeline is one linear stream, not a merge |
    | `or` on aggregations | `or` only works on event filters |
    | Group then pipe `avg()` | Original fields lost after `groupBy()` |

    ---

    **All possible solutions — ranked:**

    **✅ Solution 1: Single query with columns (closest)**
    ```humio
    #type=cisco-ise ("log_type"="Passed_Authentications" or "log_type"="Failed_Attempts")
    | groupBy(log_type, function=[count(field="Calling-Station-ID", distinct=true, as=Unique_MACs), avg(RequestLatency, as=AVG_Auth_Response)])
    | table([log_type, Unique_MACs, AVG_Auth_Response])
    ```

    Output (columns instead of rows — all data in one query):
    ```
    log_type                | Unique_MACs | AVG_Auth_Response
    ------------------------+-------------+------------------
    Failed_Attempts         | 142         | 35.2
    Passed_Authentications  | 1089        | 28.7
    ```

    **✅ Solution 2: Dashboard with separate panels**

    Create 3 single-value widgets on one dashboard. Each runs independently. This is the LogScale-native approach.

    **✅ Solution 3: LogScale API + external script**

    Call the Query API three times and merge results programmatically:
    ```python
    import requests

    queries = [
        '#type=cisco-ise "log_type"="Failed_Attempts" | count(field="Calling-Station-ID", distinct=true, as=value) | metric:="Failed_Unique_MACs"',
        '#type=cisco-ise "log_type"="Passed_Authentications" | count(field="Calling-Station-ID", distinct=true, as=value) | metric:="Passed_Unique_MACs"',
        '#type=cisco-ise ("log_type"="Passed_Authentications" or "log_type"="Failed_Attempts") | avg(RequestLatency, as=value) | metric:="AVG_Auth_Response"',
    ]

    results = []
    for q in queries:
        resp = requests.post(
            "https://logscale.example.com/api/v1/repositories/REPO/query",
            headers={"Authorization": "Bearer TOKEN", "Content-Type": "application/json"},
            json={"queryString": q, "start": "5m"}
        )
        results.append(resp.json())
    # results is now your 3-row "UNION"
    ```

    **✅ Solution 4: Scheduled Search → Lookup file (complex)**

    Run each query as a Scheduled Search that writes to a shared lookup file, then query the lookup file. Requires admin access.

    ---

    **Summary:**

    | Solution | 3 Rows? | Single Query? | Complexity |
    |----------|---------|---------------|------------|
    | `groupBy` with multiple functions | ❌ (2 rows, columns) | ✅ | Low |
    | Dashboard panels | ✅ (visually) | ❌ (3 queries) | Low |
    | API + script | ✅ | ❌ (external) | Medium |
    | Scheduled Search → Lookup | ✅ | ❌ | High |

    **Recommendation**: Solution 1 for simplicity, Solution 2 for presentation, Solution 3 for programmatic access.

---

## Section 9: Repositories, Views & Data Management

### Q36: What is the difference between a Repository and a View?

??? question "Click to reveal answer"
    | | Repository | View |
    |---|---|---|
    | **What it is** | Stores actual data (events ingested here) | Virtual layer querying one or more repositories |
    | **Data** | Owns the data | References data from repositories |
    | **SQL analogy** | A table with actual rows | A SQL VIEW (read-only query over tables) |
    | **Ingest** | Yes, data lands here | No, cannot ingest data |
    | **Retention** | Has its own retention policy | Inherits from source repositories |
    | **Filters** | None (sees everything in the repo) | Can have a permanent filter applied |

    **How to check if you're in a Repository or View in the UI:**

    1. **Look at the icon** next to the name in the header:
        - Repository = database/cylinder icon
        - View = eye icon or layered/stacked icon

    2. **Go to Settings** (gear icon in the sidebar):
        - If you see **Ingest Tokens**, **Parsers**, **Retention** → it's a **Repository**
        - If you see **Connections** (list of source repositories) and no ingest options → it's a **View**

    3. **Check the dropdown** — click the name at the top. The dropdown labels items as "Repository" or "View".

    **Typical organizational pattern:**

    - **Repositories**: `firewall_logs`, `vpc_flow_logs`, `dns_logs` (raw data ingested here)
    - **Views**: `networks_combined` (queries across multiple repos, team-scoped access)

### Q37: Are lookup files created from queries real-time or static snapshots?

??? question "Click to reveal answer"
    **Static snapshot** — like exporting to CSV. The data is captured **at the time the query ran** and does NOT auto-update.

    | Aspect | Behavior |
    |--------|----------|
    | **When data is captured** | At the moment the query executes |
    | **Auto-update** | ❌ No — frozen in time |
    | **SQL analogy** | `SELECT INTO` or `CREATE TABLE AS SELECT` — not a materialized view with refresh |
    | **Format** | Stored as a CSV file in the repository |

    **To keep a lookup file updated:**

    - Set up a **Scheduled Search** (requires admin permissions) that periodically re-runs the query and overwrites the lookup file
    - Found under **Automation → Scheduled Searches** or **Alerts → Scheduled Searches** (depends on UI version and permissions)
    - If you don't see this option, your role may not have permissions — ask your LogScale admin

---

## Section 10: Real-World Scenarios

### Q38: Find all 5xx errors grouped by endpoint

??? question "Click to reveal answer"
    ```humio
    statusCode >= 500
    | groupBy(endpoint, function=count())
    | sort(_count, order=desc)
    ```

### Q39: Find the 95th percentile response time per service where count > 100

??? question "Click to reveal answer"
    ```humio
    groupBy(service, function=[count(), percentile(field=responseTime, percentiles=[95])])
    | test(_count > 100)
    | sort(_95, order=desc)
    ```

### Q40: Create a timechart showing error rate per minute

??? question "Click to reveal answer"
    ```humio
    statusCode >= 400
    | timeChart(span=1m, function=count())
    ```

### Q41: Find users who generated more than 1000 requests in 5 minutes

??? question "Click to reveal answer"
    ```humio
    groupBy(userId, function=count())
    | test(_count > 1000)
    | sort(_count, order=desc)
    ```

### Q42: Find slow queries (response time > 2s) with details

??? question "Click to reveal answer"
    ```humio
    responseTime > 2000
    | table([@timestamp, method, url, responseTime, userId])
    | sort(responseTime, order=desc)
    | head(50)
    ```

---

## Section 11: Pipeline Thinking

### Q43: What is the "pipe" model and how does it differ from SQL?

??? question "Click to reveal answer"
    **SQL** is declarative — you describe *what* you want:
    ```sql
    SELECT endpoint, COUNT(*) FROM logs WHERE status=500 GROUP BY endpoint ORDER BY COUNT(*) DESC LIMIT 10;
    ```

    **LogScale** is a **pipeline** — data flows through transformations step by step:
    ```humio
    status=500
    | groupBy(endpoint, function=count())
    | sort(_count, order=desc)
    | head(10)
    ```

    Each `|` passes events to the next stage. Think of it like Unix pipes (`cat file | grep error | wc -l`).

### Q44: Why should you filter before aggregating?

??? question "Click to reveal answer"
    **Performance**. LogScale processes events sequentially through the pipeline.

    ❌ Slow:
    ```humio
    groupBy(url, function=count()) | test(url="/api/*")
    ```

    ✅ Fast:
    ```humio
    url="/api/*" | groupBy(url, function=count())
    ```

    **SQL analogy**: Like putting conditions in `WHERE` vs `HAVING`. SQL's optimizer helps; in LogScale, **you are the optimizer**.

---

## Quick Reference Card

```humio
// Free text search
error

// Field filter
statusCode=404

// Tag filter (indexed, fast)
#host="webserver01"

// AND (pipe or space)
statusCode=500 | method="POST"

// OR
statusCode=404 or statusCode=500

// NOT
statusCode!=200

// Wildcard
url="/api/*"

// Count
count()

// Group by
groupBy(field, function=count())

// Top N
top(field, limit=10)

// Sort
sort(field, order=desc)

// Limit
head(10) / tail(10)

// Time bucket
bucket(span=5m, function=count())

// Regex extract
regex("(?<name>pattern)")

// Computed field
newField := expression

// Field exists / not exists
field=*
not field=*

// Table output
table([field1, field2, field3])

// Lookup
match(file="ref.csv", field=key, column=csvKey)

// Parse JSON
parseJson()
```

---

## Resources

- [LogScale Documentation](https://library.humio.com/)
- [LogScale Query Language Reference](https://library.humio.com/falcon-logscale/syntax.html)
- [CrowdStrike LogScale Training](https://www.crowdstrike.com/products/observability/falcon-logscale/)
