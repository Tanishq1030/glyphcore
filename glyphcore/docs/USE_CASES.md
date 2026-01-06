# Use Cases

glyphcore is a domain-agnostic semantic state summarization framework. These examples demonstrate how the same semantic properties apply across different domains, enabling consistent decision-making regardless of what the values represent.

---

## Example 1: Infrastructure System Health

### Context

An operations team monitors API service response times across multiple services. They need to quickly identify which services are degrading and require immediate attention.

### What the Values Represent

The values are API response latency measurements in milliseconds, sampled at regular intervals over a one-hour observation window. Each value represents the average response time for that service during a sampling period.

**Observation Span:** 1 hour, sampled every 5 seconds

### What Contributors Represent

Contributors are the individual services or service instances that contribute most significantly to the overall latency signal. In a multi-service architecture, some services may be experiencing degradation while others remain stable. Contributors identify which entities' changes correlate most strongly with the aggregate signal over the observed span.

**Note:** Contributors are an optional higher-level concept. They are not part of the core Signal or StatusBlock v1 and may be provided by the host application or future extensions.

For example, if overall latency is increasing, contributors might be:
- A specific microservice experiencing high load
- A database connection pool that is exhausted
- A downstream dependency that is slow
- A particular region or data center

The framework identifies which entities contribute most to the signal, without knowing what those entities are.

### What Decision the StatusBlock Enables

The StatusBlock answers: "Is this system in a state that requires attention?"

For infrastructure health, the StatusBlock enables the decision:

**Should I investigate this service now, or can it wait?**

The semantic properties provide the answer:
- **Direction UP + Regime TREND + Momentum ACCELERATING**: Service is degrading rapidly. Investigate immediately.
- **Direction UP + Regime RANGE + Momentum STABLE**: Service is operating within normal variation. Monitor but no immediate action.
- **Direction FLAT + Regime RANGE + High Confidence**: Service is stable. No action needed.

The framework does not know that latency is "bad" when it goes up. The application interprets: "UP direction with high strength in a TREND regime means this service requires attention."

---

## Example 2: AI/ML Training Run Monitoring

### Context

A machine learning engineer monitors a training run to determine whether the model is learning effectively, has plateaued, or is diverging. They need to decide whether to continue training, adjust hyperparameters, or stop the run.

### What the Values Represent

The values are validation loss measurements recorded after each epoch. Each value represents how well the model performs on a held-out validation set. Lower values indicate better performance.

**Observation Span:** Training run, per epoch

### What Contributors Represent

Contributors are the components of the training process that contribute most to the loss signal. In complex training scenarios, multiple factors influence the loss:

- Specific layers or modules in the model architecture
- Different datasets or data sources
- Training hyperparameters or learning rate schedules
- Data augmentation strategies

Contributors identify which entities' changes correlate most strongly with the aggregate signal over the observed span, enabling the engineer to focus optimization efforts.

### What Decision the StatusBlock Enables

The StatusBlock answers: "Is this system in a state that requires attention?"

For training run monitoring, the StatusBlock enables the decision:

**Should I continue training, adjust parameters, or stop this run?**

The semantic properties provide the answer:
- **Direction DOWN + Regime TREND + Momentum ACCELERATING**: Model is learning effectively. Continue training.
- **Direction FLAT + Regime RANGE + High Confidence**: Model has plateaued. Consider adjusting learning rate or architecture.
- **Direction UP + Regime TREND + Momentum ACCELERATING**: Model is diverging. Stop training and investigate.

The framework does not know that loss going DOWN is "good" and loss going UP is "bad." The application interprets: "DOWN direction with high strength in a TREND regime means the model is learning; UP direction means the model is diverging."

---

## Example 3: Security Threat Surface

### Context

A security operations center monitors threat scores across multiple endpoints, networks, or user accounts. They need to identify which entities are driving increased threat activity and require immediate investigation.

### What the Values Represent

The values are normalized threat scores on a scale from 0 to 10, computed at regular intervals. Each value represents the aggregate threat level based on multiple indicators: failed authentication attempts, unusual network traffic patterns, suspicious file access, and other security signals.

**Observation Span:** Rolling 24 hours, sampled every 1 minute

### What Contributors Represent

Contributors are the specific entities that contribute most to the overall threat signal. In a distributed system, threats may originate from:

- Specific IP addresses or network ranges
- Individual user accounts or service principals
- Particular endpoints or API routes
- Geographic regions or data centers
- Time windows or activity patterns

Contributors identify which entities' changes correlate most strongly with the aggregate signal over the observed span, enabling security analysts to focus investigation on the most significant contributors.

### What Decision the StatusBlock Enables

The StatusBlock answers: "Is this system in a state that requires attention?"

For security threat monitoring, the StatusBlock enables the decision:

**Should I investigate this threat now, or is it within normal variation?**

The semantic properties provide the answer:
- **Direction UP + Regime VOLATILE + Momentum ACCELERATING**: Threat is increasing rapidly and erratically. Immediate investigation required.
- **Direction UP + Regime TREND + High Confidence**: Sustained threat increase. Investigate systematically.
- **Direction FLAT + Regime RANGE + High Confidence**: Threat level is stable. Continue monitoring.

The framework does not know that threat scores going UP is "bad." The application interprets: "UP direction with high strength in a VOLATILE regime means immediate security attention is required."

---

## Pattern Recognition

These three examples demonstrate the same pattern:

1. **Same semantic properties** (Direction, Strength, Momentum, Regime, Confidence)
2. **Same StatusBlock format** (Title, Verdict Line, Span, Context, Confirmation)
3. **Same decision framework** ("Is this system in a state that requires attention?")
4. **Different nouns** (latency vs loss vs threat scores)
5. **Different interpretations** (degradation vs learning vs security risk)

The framework computes semantic properties without knowing what the values represent. The host application provides domain-specific interpretation:
- Infrastructure: UP direction means degradation (bad)
- AI/ML: DOWN direction means learning (good), UP direction means diverging (bad)
- Security: UP direction means increased threat (bad)

The framework's role is to answer: "Is this system in a state that requires attention?"

The application's role is to answer: "What does that mean for my domain, and what action should I take?"

---

## Domain-Agnostic Design

glyphcore is domain-agnostic because:

1. **Semantic properties are universal**: Direction, Momentum, Regime, and Confidence describe system behavior patterns that exist in any domain.

2. **Values are opaque**: The framework does not interpret what the numbers mean. It only computes how they change.

3. **Contributors are generic** (optional): Contributors identify which entities' changes correlate most strongly with the aggregate signal. They are not part of core Signal or StatusBlock v1 and may be provided by the host application or future extensions.

4. **Decision surface is consistent**: The same question—"Is this system in a state that requires attention?"—applies across all domains.

5. **Interpretation is external**: The host application decides whether UP is good or bad, what action to take, and what the values represent.

This design enables glyphcore to be used for any domain where:
- Signals exist (values change over time)
- Trends matter (direction and momentum are meaningful)
- Decisions must be made quickly (StatusBlock provides fast scanning)
- Multiple entities contribute (contributors identify key drivers)

---

## Key Insight

glyphcore is not a visualization library. It is a **terminal-native status language** for answering:

**"Is this system in a state that requires attention?"**

The framework provides semantic analysis. The application provides domain-specific meaning.

Very few frameworks live in that space.
