# Signal Semantics

This document defines the semantic properties of the Signal dataclass. These definitions are the single source of truth. Renderers may not reinterpret these meanings.

---

## Direction

**Type:** `str`  
**Values:** `"UP"` | `"DOWN"` | `"FLAT"`

**Definition:**

Direction indicates the net movement of the system over the observed span.

- **UP:** The final value exceeds the initial value.
- **DOWN:** The final value is less than the initial value.
- **FLAT:** The final value equals the initial value.

**Computation:**

Direction is determined by comparing the first and last values in the series:
- If `final_value > initial_value`: Direction is UP
- If `final_value < initial_value`: Direction is DOWN
- If `final_value == initial_value`: Direction is FLAT

**Semantic Stability:**

Direction describes net movement only. It does not imply:
- Whether the movement is desirable
- The rate of change
- The pattern of intermediate values
- Any domain-specific interpretation

### Direction Tolerance (Engine Policy)

An implementation may apply a tolerance when classifying Direction. Tolerance affects classification, not meaning.

Tolerance values are implementation-defined and must not be reinterpreted by renderers.

If an implementation applies tolerance (e.g., treating differences below a threshold as FLAT), this is an engine policy decision, not a semantic property. The semantic meaning of Direction remains: UP when final > initial, DOWN when final < initial, FLAT when final == initial.

---

## Strength

**Type:** `float`  
**Range:** `0.0` to `1.0`

**Definition:**

Strength is the normalized magnitude of change over the observed span, expressed as a ratio of the net change to the total range of values.

Strength is dimensionless and comparable across systems.

**Computation:**

```
strength = |final_value - initial_value| / (max_value - min_value)
```

If the range is zero (all values are identical), strength is `0.0`.

**Semantic Stability:**

Strength quantifies the significance of change relative to the system's observed variability. It does not indicate:
- Whether the change is positive or negative (see Direction)
- The absolute magnitude of change
- The rate of change (see Momentum)
- Any domain-specific significance

---

## Momentum

**Type:** `str`  
**Values:** `"ACCELERATING"` | `"DECELERATING"` | `"STABLE"`

**Definition:**

Momentum describes the change in the magnitude of sequential differences. It indicates whether the system's movement is speeding up, slowing down, or maintaining a constant rate.

- **ACCELERATING:** The absolute rate of change in the second half of the span exceeds the absolute rate of change in the first half by more than 20%.
- **DECELERATING:** The absolute rate of change in the second half of the span is less than 80% of the absolute rate of change in the first half.
- **STABLE:** The absolute rate of change in the second half is between 80% and 120% of the absolute rate of change in the first half.

**Computation:**

1. Divide the series into first and second halves.
2. Compute the average absolute change per unit in each half.
3. Compare the ratios as defined above.

**Semantic Stability:**

Momentum describes the acceleration of change, not the direction of change. It is independent of Direction. A system moving DOWN can be ACCELERATING (moving down faster) or DECELERATING (moving down slower).

---

## Regime

**Type:** `str`  
**Values:** `"TREND"` | `"RANGE"` | `"VOLATILE"`

**Definition:**

Regime characterizes the pattern of behavior exhibited by the system over the observed span.

- **TREND:** The system exhibits sustained directional movement. The net change exceeds 50% of the total range, and the direction of change is consistent across most segments.
- **RANGE:** The system oscillates within bounds without sustained directional movement. The net change is less than 50% of the total range, and the variance of changes is low relative to the range.
- **VOLATILE:** The system exhibits unstable or erratic change. The variance of changes is high relative to the total range, indicating unpredictable fluctuations.

**Computation:**

1. Compute net change as a percentage of total range.
2. Compute the variance of segment-to-segment changes.
3. Compute the coefficient of variation (standard deviation of changes / mean absolute change).
4. Classify:
   - If net change > 50% of range AND coefficient of variation < 0.3: TREND
   - If coefficient of variation > 0.3: VOLATILE
   - Otherwise: RANGE

**Semantic Stability:**

Regime describes the pattern of behavior, not the direction or magnitude. A system can be in a TREND regime while moving UP or DOWN. Regime is independent of Direction and Strength.

---

## Confidence

**Type:** `float`  
**Range:** `0.0` to `1.0`

**Definition:**

Confidence quantifies the reliability of the computed semantic properties. It reflects the consistency of the signal and the clarity of the pattern.

**Computation:**

For FLAT direction:
- Confidence = 1.0 - coefficient of variation (if all values are identical, confidence = 1.0)

For UP or DOWN direction:
- Consistency ratio: proportion of segments that align with the overall direction
- Magnitude ratio: net change / total range
- Confidence = (consistency_ratio × 0.6) + (magnitude_ratio × 0.4)

**Semantic Stability:**

Confidence measures the reliability of the signal, not its desirability or significance. A high-confidence signal may indicate a clear pattern that is undesirable. A low-confidence signal may indicate uncertainty in the pattern, not necessarily a weak signal.

---

## Span

**Type:** `str`  
**Required:** Yes

**Definition:**

Span declares the observation window over which the signal is computed. It is an explicit, human-readable description of scope and granularity.

**Format:**

Span must be provided by the host application. The framework does not infer or compute span.

Examples:
- `"1H · 5s"` - One hour window, 5-second granularity
- `"1D · 1m"` - One day window, 1-minute granularity
- `"1M · Daily"` - One month window, daily granularity
- `"100 samples · sequential"` - 100 sequential samples

**Requirements:**

- Span must be explicitly declared by the host application
- Span format is application-defined but must be human-readable
- The framework does not parse or interpret span format
- Span is metadata that accompanies the signal

**Semantic Stability:**

Span defines the observation window. All semantic properties (Direction, Strength, Momentum, Regime, Confidence) are computed relative to this span. Changing the span may change the semantic properties, as the system's behavior may differ across different observation windows.

Span must be declared, never inferred.

---

## Semantic Contract

These definitions are immutable. Renderers must use these exact meanings. Renderers may not:

- Reinterpret Direction, Momentum, or Regime
- Compute alternative confidence measures
- Modify strength calculations
- Infer domain-specific meanings

The Signal dataclass is domain-agnostic. The framework provides semantic properties. The host application provides domain-specific interpretation.

---

## Property Independence

These properties are computed independently:

- **Direction** and **Strength** are independent (a system can have high strength moving UP or DOWN)
- **Momentum** is independent of **Direction** (a system moving DOWN can be ACCELERATING)
- **Regime** is independent of **Direction** (a system can be in a TREND regime moving UP or DOWN)
- **Confidence** measures reliability, not desirability

The only dependency is that FLAT direction implies Strength = 0.0 (or near-zero if computed with tolerance).

---

## Stability Guarantee

These semantic definitions are stable across:
- Different domains
- Different value ranges
- Different time scales
- Different observation windows

The meanings do not change based on context. A TREND regime means the same thing whether the values represent latency, loss, scores, or any other metric.
