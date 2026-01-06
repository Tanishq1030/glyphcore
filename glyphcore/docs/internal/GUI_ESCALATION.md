# GUI Escalation Rules

This document defines the design rules for GUI rendering escalation.
These rules ensure GUI and TUI remain synchronized and maintain semantic consistency.

---

## Core Principle

**GUI rendering only accepts Signal.**

GUI rendering is a presentation layer that visualizes the semantic Signal.
It does not recompute, reinterpret, or invent semantics.

---

## GUI Escalation Rules

### 1. Input Contract

- ✅ GUI rendering **only** accepts `Signal`
- ❌ GUI rendering **never** accepts raw data (values, labels)
- ❌ GUI rendering **never** accepts DataFrames or other data structures

**Correct API:**
```python
signal = engine.analyze(values, labels)
engine.render_tui(signal)      # TUI rendering
engine.render_gui(signal)    # GUI escalation
```

**Incorrect API:**
```python
engine.render_gui(values, labels)  # ❌ Never do this
engine.render_gui(df)              # ❌ Never do this
```

---

### 2. Read-Only Semantics

GUI rendering must **never**:
- ❌ Normalize data again
- ❌ Compute direction
- ❌ Compute momentum
- ❌ Reinterpret regime
- ❌ Recalculate confidence
- ❌ Modify the Signal

GUI rendering **may**:
- ✅ Display raw values from `signal.values`
- ✅ Display labels from `signal.labels`
- ✅ Show annotations derived from Signal properties
- ✅ Visualize direction, momentum, regime, confidence as metadata

---

### 3. Mental Model

**TUI answers: "Should I care?"**
- Fast, scannable, always-on
- Glyph-based, zero-lag
- Keyboard-native

**GUI answers: "Show me why."**
- Detailed, interactive, on-demand
- Pixel-based, high-fidelity
- Mouse-enabled (zoom, hover, pan)

Both consume the same Signal. No divergence.

---

### 4. Implementation Requirements

GUI renderer must:
1. Accept `Signal` as the only input
2. Use `signal.values` for data points
3. Use `signal.labels` for x-axis labels
4. Display Signal properties (direction, momentum, regime, confidence) as metadata
5. Be optional (graceful degradation if plotly/matplotlib unavailable)
6. Be read-only (no side effects on Signal)

---

### 5. Example GUI Display

When rendering a Signal, GUI should show:

**Main visualization:**
- Line chart of `signal.values`
- X-axis labels from `signal.labels`
- Y-axis with appropriate scaling

**Metadata display:**
- Title or subtitle showing: `{direction} | {momentum} | {regime}`
- Confidence indicator
- Strength indicator

**Annotations (derived from Signal):**
- Highlight volatile segments (if `regime == "VOLATILE"`)
- Mark direction changes (if `direction` changes)
- Show momentum transitions (if `momentum` changes)

---

### 6. What GUI Must NOT Do

❌ **Recompute semantics:**
```python
# WRONG
def render_gui(signal):
    direction = compute_direction(signal.values)  # ❌ No!
    momentum = compute_momentum(signal.values)      # ❌ No!
```

✅ **Use Signal properties:**
```python
# CORRECT
def render_gui(signal):
    title = f"{signal.direction} | {signal.momentum} | {signal.regime}"
    plot(signal.values, title=title)
```

---

### 7. Synchronization Guarantee

Because both TUI and GUI consume the same Signal:
- ✅ No sync drift (single source of truth)
- ✅ Consistent semantics (same analysis)
- ✅ Deterministic rendering (same input → same output)

---

## Final Rule

If GUI rendering needs information that is not in Signal,
the solution is to **add it to Signal** (and recompute via `analyze()`),
not to compute it in the renderer.

---

## Status

Current implementation in `glyphcore/renderers/gui.py` follows these rules:
- ✅ Accepts Signal only
- ✅ Uses signal.values and signal.labels
- ✅ Displays Signal properties as metadata
- ✅ Read-only (no Signal modification)
- ✅ Optional dependency (plotly/matplotlib)

