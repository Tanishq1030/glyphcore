# glyphcore

**glyphcore** is a terminal-first visualization engine for building applications where the terminal is the primary interface, but visual clarity is still essential.

It renders **semantic signals** as **glyph-based views** for fast scanning, while allowing optional escalation to **high-fidelity GUI inspection** when deeper analysis is needed.

This is not a charting library.
It is a framework for **intent-driven, multi-fidelity visualization**.

---

## Why glyphcore exists

Most visualization tools assume pixels, mice, and dashboards.

But many serious workflows live in terminals:
- traders
- DevOps engineers
- system monitors
- remote SSH environments
- keyboard-first users

Existing options force a bad trade-off:
- TUIs are fast but visually limited
- GUIs are rich but slow and workflow-breaking

**glyphcore removes that trade-off.**

It treats the terminal as a **semantic grid**, rendering meaning first, not geometry — and only uses GUI visuals when the user explicitly asks for them.

---

## Core ideas

### 1. Semantic first, visuals second
Data is interpreted into **signals** (direction, momentum, regime) before anything is rendered.

If the meaning is unclear, nothing is drawn.

### 2. Terminal as a semantic grid
The terminal is treated as a 2D canvas of glyphs, not a stream of text.

Rendering is done in memory using a virtual framebuffer, then flushed atomically.

### 3. Layered fidelity
- **TUI (always-on):** fast, glyph-based, SSH-safe
- **GUI (summonable):** pixel-based inspection for detail

Both views are driven by the same semantic core.

---

## What glyphcore is (and is not)

### It **is**
- a framework / engine
- terminal-first
- keyboard-native
- field-agnostic
- dependency-light

### It **is not**
- a plotting library
- a finance-only tool
- an ASCII art generator
- a dashboard framework

---

## Typical use cases

- Terminal-based trading or analytics tools
- Log, metric, or signal monitoring
- Developer tooling with optional visual inspection
- Remote or cloud-native observability
- Any application where **“Should I care?”** matters more than raw detail

---

## Minimal example (conceptual)

```python
from glyphcore import Engine

engine = Engine(width=80, height=24)

signal = engine.analyze(data)

tui_view = engine.render_tui(signal)
print(tui_view)

# When deeper inspection is needed
engine.render_gui(signal)
