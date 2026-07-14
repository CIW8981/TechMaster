---
title: "DORA Metrics - First Principles Understanding"
description: "Deep understanding of DORA metrics through first principles thinking - questions that build intuition from the ground up"
tags:
  - dora
  - devops
  - metrics
  - engineering-excellence
  - software-delivery
difficulty: intermediate
last_updated: "2026-07-14"
---

# DORA Metrics - First Principles Approach

!!! info "Learning Philosophy"
    This page uses a **first principles approach** — instead of memorizing definitions, we ask fundamental questions that force you to derive understanding from basic truths. Each section starts with foundational questions and builds toward deeper insight.

## Level 1: Why Do We Measure Anything?

Before understanding DORA, answer these foundational questions:

### Questions to Ponder

!!! question "Q1: What is the purpose of measurement in engineering?"
    Why do we measure anything at all? What does a measurement give us that intuition doesn't?
    
    **Think about**: If you can't measure it, can you improve it? What's the relationship between measurement and feedback loops?

!!! question "Q2: What makes a good metric vs. a bad metric?"
    What properties should a metric have to actually drive improvement rather than gaming behavior?
    
    **Think about**: Goodhart's Law — "When a measure becomes a target, it ceases to be a good measure." How do you design metrics that resist gaming?

!!! question "Q3: Why do software teams need different metrics than manufacturing?"
    A factory measures defects per unit and throughput. Why can't we just count lines of code or bugs fixed?
    
    **Think about**: Software is invisible, non-linear, and the "product" is never truly finished. How does this change what's worth measuring?

---

## Level 2: What Are We Actually Trying to Optimize?

### Questions to Ponder

!!! question "Q4: What does 'good' software delivery look like from first principles?"
    Forget existing frameworks. If you had to define what excellent software delivery means, what properties would it have?
    
    **Think about**: 
    
    - Speed: How fast can value reach users?
    - Stability: How often do things break?
    - Recovery: When things break, how fast can you fix them?
    - These create a natural tension — how do you balance them?

!!! question "Q5: Is there a fundamental tradeoff between speed and stability?"
    Common belief: 'Move fast and break things' vs. 'Go slow and be careful.' Is this actually true?
    
    **Think about**: What if the highest-performing teams are BOTH fast AND stable? What would that imply about how they work?

!!! question "Q6: What are the smallest number of signals that capture delivery performance?"
    If you could only measure 4 things about your team's delivery capability, what would they be and why?
    
    **Think about**: You want to capture both throughput (how much/fast you deliver) AND stability (how reliable that delivery is). What's the minimum set?

---

## Level 3: Deriving the Four DORA Metrics

### Throughput Metrics

!!! question "Q7: How do you measure 'speed of delivery' without incentivizing shortcuts?"
    If you measure 'features shipped per sprint', teams ship half-baked features. If you measure 'time to complete a feature', scope varies wildly. What's a better unit of measurement?
    
    **Think about**: What if we measure from the smallest meaningful unit — a single code change (commit)? The time from commit to production is... **Deployment Frequency** and **Lead Time for Changes**.

!!! question "Q8: Why 'Deployment Frequency' and not 'Release Frequency'?"
    What's the difference between a deployment and a release? Why does the distinction matter?
    
    **Think about**: 
    
    - A deployment = code reaching production
    - A release = feature reaching users (feature flags, dark launches)
    - Deployment frequency measures your *capability* to deliver, not your business decision about when to expose features

!!! question "Q9: Why measure 'Lead Time for Changes' from commit to production?"
    Why not measure from when a ticket is created? Or from when work starts? Why specifically commit-to-production?
    
    **Think about**: 
    
    - Ticket creation → work start: measures prioritization/planning, not delivery capability
    - Work start → commit: measures complexity/skill, not pipeline efficiency
    - Commit → production: measures your **delivery pipeline** — the thing DevOps actually controls

### Stability Metrics

!!! question "Q10: What's the best way to measure 'things going wrong' in production?"
    Options: total incidents? Severity-weighted incidents? Percentage of deployments that fail? Which gives the most useful signal?
    
    **Think about**: **Change Failure Rate** (% of deployments causing failures) normalizes for deployment volume. A team deploying 100 times/day with 2 failures (2%) is arguably better than a team deploying once/month with 0 failures (but terrified to deploy).

!!! question "Q11: Why is 'Time to Restore Service' more useful than 'Mean Time Between Failures'?"
    Traditional reliability engineering focuses on MTBF. Why did DORA choose MTTR (time to restore) instead?
    
    **Think about**: 
    
    - MTBF assumes you can prevent all failures — in complex distributed systems, this is impossible
    - MTTR accepts that failures WILL happen and measures your **resilience** — how fast can you recover?
    - This reflects a philosophical shift: from failure prevention to failure management

---

## Level 4: The System Behind the Metrics

### Questions About Relationships

!!! question "Q12: Why do these four metrics work as a SET rather than individually?"
    Could you just pick one? Why do you need all four?
    
    **Think about**:
    
    | If you only optimize... | You might... |
    |---|---|
    | Deployment Frequency | Deploy garbage frequently |
    | Lead Time | Rush changes without testing |
    | Change Failure Rate | Never deploy (0% failure rate!) |
    | Time to Restore | Not care about preventing failures |
    
    The four metrics create **balanced tension**. You can't game one without the others exposing the problem.

!!! question "Q13: What engineering practices enable ALL four metrics to improve simultaneously?"
    If speed and stability aren't actually in tension for elite teams, what practices make both possible?
    
    **Think about**:
    
    - Small batch sizes (small PRs, frequent commits)
    - Automated testing (confidence without manual gates)
    - CI/CD pipelines (fast, repeatable delivery)
    - Trunk-based development (reduce merge complexity)
    - Observability (fast detection → fast recovery)
    - Feature flags (decouple deployment from release)

!!! question "Q14: What does the data show about elite vs. low performers?"
    DORA research surveyed thousands of teams. What's the magnitude of difference?
    
    **Think about**:
    
    | Metric | Elite | Low |
    |---|---|---|
    | Deployment Frequency | Multiple times/day | Once per month to once per 6 months |
    | Lead Time for Changes | Less than one hour | One to six months |
    | Change Failure Rate | 0-15% | 46-60% |
    | Time to Restore Service | Less than one hour | More than six months |
    
    Elite teams are not 2x better — they're **100x-1000x** better. This isn't incremental improvement; it's a fundamentally different way of working.

---

## Level 5: Deeper First Principles Questions

### Causality and Implementation

!!! question "Q15: Are DORA metrics causes or effects?"
    Do good metrics CAUSE good outcomes, or do good practices cause good metrics? Does it matter?
    
    **Think about**: The metrics are **lagging indicators** of underlying capabilities. You don't improve Lead Time by watching a dashboard — you improve it by fixing your CI pipeline, reducing PR review bottlenecks, automating deployments. The metric tells you whether your improvements are working.

!!! question "Q16: Can you have excellent DORA metrics and still build the wrong product?"
    You deploy 50 times a day with 0% failure rate and sub-hour recovery. Are you successful?
    
    **Think about**: DORA measures **delivery performance**, not **product-market fit**. You also need product metrics (user engagement, revenue, NPS). DORA tells you how well your engineering machine works, not whether you're building the right thing.

!!! question "Q17: How do DORA metrics interact with team size and architecture?"
    Can a 500-person monolith team have elite DORA metrics? What about a 3-person startup?
    
    **Think about**: 
    
    - Architecture constrains metrics: monoliths create coupling that slows deployment
    - Conway's Law: team structure mirrors system structure
    - Microservices enable independent deployment → higher frequency per team
    - But: coordination costs in distributed systems can slow things down differently

!!! question "Q18: What's the relationship between DORA metrics and developer experience?"
    Do developers on elite-performing teams have better work-life? Or are they just grinding harder?
    
    **Think about**: DORA research shows elite teams have **less** burnout, not more. Fast feedback loops, automated toil, and low failure rates reduce stress. The pain isn't in going fast — it's in going slow with broken processes.

---

## Level 6: Critical Thinking and Limitations

!!! question "Q19: What are the blind spots of DORA metrics?"
    No framework is perfect. What does DORA NOT capture?
    
    **Think about**:
    
    - **Security**: Fast deployment of insecure code isn't good
    - **Technical debt**: You can have great metrics while accruing debt
    - **Team health**: Burnout, turnover, knowledge silos
    - **Customer impact**: Fast recovery doesn't mean users weren't affected
    - **Cost efficiency**: Elite metrics at 10x the infrastructure cost?

!!! question "Q20: How would you extend DORA from first principles?"
    If you were designing DORA v2, what 5th metric would you add and why?
    
    **Think about**: Candidates that have been proposed:
    
    - **Reliability** (SLO adherence) — added by Google in 2021 as a 5th metric
    - **Developer productivity** (time in flow state)
    - **Security posture** (time to patch vulnerabilities)
    - **Infrastructure cost per deployment**
    - What first principle would guide your choice?

---

## Synthesis: Building Your Mental Model

!!! success "The First Principles Summary"
    
    **Start from**: Software delivery has two fundamental dimensions — **throughput** and **stability**
    
    **Derive**: You need at least one metric for each:
    
    - Throughput → How often? (Deployment Frequency) + How fast? (Lead Time)
    - Stability → How often broken? (Change Failure Rate) + How fast to fix? (Time to Restore)
    
    **Realize**: These four create balanced tension — gaming one exposes problems in others
    
    **Discover**: Elite teams prove speed and stability are NOT in conflict — they reinforce each other
    
    **Conclude**: The metrics are symptoms of deeper capabilities (automation, small batches, fast feedback, loosely coupled architecture)

---

## Practice: Apply First Principles to Your Team

### Self-Assessment Questions

- [ ] Can you measure all four metrics for your team today? If not, what's blocking you?
- [ ] Which metric is your weakest? What's the root cause (not the symptom)?
- [ ] What ONE practice change would improve multiple metrics simultaneously?
- [ ] Are you optimizing metrics or optimizing the capabilities that drive metrics?
- [ ] Is your architecture enabling or constraining your delivery performance?

### Discussion Prompts for Team Retrospectives

1. "If we could only deploy once per quarter, what would we change about how we work?"
2. "What's our actual lead time from commit to production? Where does time get stuck?"
3. "When was our last production incident? How long did it take to detect vs. resolve?"
4. "What percentage of our deployments need a hotfix or rollback?"
5. "What's one automation we could build this sprint that would permanently reduce lead time?"

---

## Resources

### Foundational Reading

- [Accelerate (Book)](https://itrevolution.com/product/accelerate/) - The research behind DORA metrics
- [State of DevOps Reports](https://dora.dev/research/) - Annual research data
- [DORA Quick Check](https://dora.dev/quickcheck/) - Assess your team's performance

### Related Topics

- [Docker](../docker/index.md) - Containerization for consistent deployments
- [Kubernetes](../kubernetes/index.md) - Orchestration for deployment automation
- [Terraform](../terraform/index.md) - Infrastructure as Code for reproducibility

---

**Tags**: #dora #devops #metrics #engineering-excellence #software-delivery #first-principles

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
