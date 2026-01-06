# StatusBlock

A StatusBlock answers exactly ONE question:

**"Is this system in a state that requires attention?"**

*(Previously called SignalBlock - renamed for domain-agnostic clarity)*

---

## Required Elements (in order)

### 1. Title
- Name of entity (system, metric, region, component)
- Single line, clear identifier

### 2. Verdict Line
- **Direction** (▲ / ▼ / →)
- **Magnitude Indicator** (e.g., % change, delta, score)
- **Regime** (TREND / RANGE / VOLATILE)

The magnitude indicator is supplied by the host application. The framework does not enforce units or formatting.

### 3. Span
- Explicit declaration of the observation window
- Must be human-readable
- Must never be inferred from visuals

Examples:
- `Span: 1H · 5s`
- `Span: 1D · 1m`
- `Span: 1M · Daily`

### 4. Context
- **Last value** (current state)
- **Recent range** (low → high)

### 5. Confirmation (optional, secondary)
- Minimal wave or sparkline
- Must never dominate text
- Max height: 2 rows
- Text-first, wave-last

---

## Forbidden Elements

- ❌ Candlesticks
- ❌ OHLC metaphors
- ❌ Dense bars
- ❌ Full axes
- ❌ Multiple series in one block
- ❌ Chart-like density
- ❌ Full-height block fills (█) except for alerts

---

## Invariant

**The StatusBlock must remain understandable if all visual elements are removed.**

If all glyphs, waves, and visual decorations are stripped away, the text content (Title, Verdict Line, Span, Context) must provide complete semantic meaning. Visual elements are confirmation only, never primary information.

---

## Output Format (ASCII sketch)

```
api-service      +8.3% ▲  TREND
Span: 1H · 5s
Last: 42.5ms
Range: 38.2ms ───── 42.5ms
Wave: ▁▂▃▄▅▆▇█
```

**Rules:**
- Text first
- Wave last
- Wave max height = 2 rows
- Wave is minimal, not dominant

---

## Semantic Contract

StatusBlock is a **decision surface**, not a chart.

It answers: **"Is this system in a state that requires attention?"**

Not: **"Show me everything."**

---

## Renderer Requirements

Any StatusBlock renderer must:

1. ✅ Prioritize text over graphics
2. ✅ Limit wave to 2 rows maximum
3. ✅ Enforce horizontal density limits
4. ✅ Ban chart-like elements
5. ✅ Remain understandable without wave
6. ✅ Use minimal visual weight

---

## Domain Examples

**Infrastructure:**
```
api-service      +8.3% ▲  TREND
Span: 1H · 5s
Last: 42.5ms
Range: 38.2ms ───── 42.5ms
Wave: ▁▂▃▄▅▆▇█
```

**AI/ML:**
```
training-loss    -12.5% ▼  TREND
Span: 100 epochs · per epoch
Last: 0.0234
Range: 0.0234 ───── 0.0456
Wave: █▇▆▅▄▃▂▁
```

**Security:**
```
threat-score     +15.2% ▲  VOLATILE
Span: 1D · 1m
Last: 7.8
Range: 5.2 ───── 7.8
Wave: ▁▃▅▇█▇▅▃
```

Same format. Different domains.

---

## This becomes law.

No renderer can violate these rules.

