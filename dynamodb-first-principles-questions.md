# AWS DynamoDB - First Principles Learning Questions

## Level 1: Fundamental Concepts (What is it?)

1. What problem does DynamoDB solve that traditional databases cannot?
2. Why does DynamoDB exist? What fundamental need does it address?
3. What is the most basic unit of data in DynamoDB?
4. How does DynamoDB physically store data? (distributed vs centralized)
5. What makes DynamoDB "NoSQL"? What does it NOT do that SQL databases do?

## Level 2: Core Building Blocks (How does it work?)

6. What is a partition key and why is it absolutely necessary?
7. How does DynamoDB know WHERE to store your data?
8. What happens when you write an item? (trace the path from request to storage)
9. What is the relationship between partition key and data distribution?
10. Why does DynamoDB use hash functions for partition keys?
11. What is a sort key and what fundamental problem does it solve?
12. How does DynamoDB achieve "single-digit millisecond" performance?

## Level 3: Data Modeling from First Principles

13. Why can't you JOIN tables in DynamoDB? What's the fundamental architectural reason?
14. If you can't JOIN, how do you model relationships between entities?
15. What is the minimum information needed to retrieve an item in DynamoDB?
16. Why are secondary indexes necessary? What limitation do they overcome?
17. What is the trade-off when creating a Global Secondary Index?
18. How would you design a table if you could only ask ONE question of your data?

## Level 4: Capacity and Performance (Why these limits?)

19. What is a Read Capacity Unit (RCU) measuring at its core?
20. What is a Write Capacity Unit (WCU) measuring at its core?
21. Why does strongly consistent read cost 2x eventually consistent read?
22. What causes "hot partitions" and why is it a problem?
23. How does DynamoDB scale horizontally? What happens behind the scenes?
24. Why is there a 400KB limit on item size?

## Level 5: Consistency and Reliability

25. What does "eventually consistent" mean in physical terms?
26. Why does DynamoDB default to eventual consistency?
27. How does DynamoDB replicate data across availability zones?
28. What guarantees does DynamoDB provide for writes?
29. Why can't DynamoDB guarantee ACID transactions across multiple tables by default?

## Level 6: Query Patterns (Thinking in DynamoDB)

30. Why can you only query on partition key (and optionally sort key)?
31. What is a Scan and why is it expensive?
32. How would you implement "search by email" if email is not your partition key?
33. Why do you need to know your access patterns BEFORE designing your table?
34. What is the single-table design pattern and what problem does it solve?

## Level 7: Advanced Concepts

35. What is DynamoDB Streams and what fundamental capability does it enable?
36. How do conditional writes prevent race conditions?
37. What is the CAP theorem and where does DynamoDB sit?
38. Why use DAX (DynamoDB Accelerator)? What bottleneck does it address?
39. How do Time-To-Live (TTL) deletions work and why are they free?

## Level 8: Cost Optimization from First Principles

40. Why does on-demand pricing exist alongside provisioned capacity?
41. What is the fundamental trade-off between on-demand and provisioned mode?
42. Why do GSIs consume additional capacity?
43. How does data size affect your costs?
44. What operations are free in DynamoDB and why?

## Practical Application Questions

45. Design a DynamoDB table for a social media app where users can post and follow others. What's your partition key strategy?
46. You need to query items by date range. How do you structure your keys?
47. Your application has 1000 reads/sec and 100 writes/sec. Calculate the minimum RCU/WCU needed.
48. You're experiencing throttling. What are the 3 fundamental causes and solutions?
49. How would you migrate from a relational database to DynamoDB? What changes in thinking are required?
50. When should you NOT use DynamoDB? What are its fundamental limitations?

---

## Learning Approach

For each question:
1. Answer without looking at documentation first
2. Explain your reasoning from basic principles
3. Verify your answer with AWS documentation
4. Identify gaps in your mental model
5. Build up to more complex concepts

The goal is to understand WHY DynamoDB works the way it does, not just memorize HOW to use it.
