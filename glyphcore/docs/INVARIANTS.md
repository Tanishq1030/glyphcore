# glyphcore Invariants

This document defines the non-negotiable design invariants of glyphcore.
Any change that violates these rules is considered a breaking change,
even if tests pass.

---

## 1. Semantic Contract

- `Signal` is the single source of truth.
- Renderers (TUI / GUI) must consume `Signal`.
- Renderers must not compute semantics.
- If a value is not present in `Signal`, it must not be invented.

---

## 2. Engine Responsibilities

- The Engine orchestrates analysis and rendering.
- The Engine must never draw.
- The Engine must never select glyphs.
- The Engine must never format labels.

---

## 3. Rendering Invariants

### Geometry
- No diagonal glyphs are ever allowed.
- All lines are rendered using step interpolation:
  horizontal → vertical → horizontal.
- Vertical movement occurs only at step midpoints.
- Lines must be continuous; no teleporting gaps.

### Coordinate Truth
- Higher values must always render higher on screen.
- The minimum value anchors to the bottom of the plot area.
- The maximum value anchors to the top of the plot area.
- Flat data must render as a flat line.

---

## 4. Glyph Semantics

- Corner glyphs are chosen based on slope transitions, not direction alone.
- Vertical bridges must use `│`.
- Horizontal runs must use `─`.
- Terminal points must be marked explicitly (e.g. `●`).

---

## 5. Visual Weight

- The main stroke must be thinner than highlights.
- Highlight glyphs (e.g. anomalies) must never be ambiguous with the main stroke.
- Momentum or confidence may affect stroke weight, but never geometry.

---

## 6. Fidelity Separation

- TUI rendering is always-on and zero-dependency.
- GUI rendering is optional and summonable.
- GUI rendering must reuse the same `Signal`.
- GUI rendering must not recompute semantics.

---

## 7. Dependency Discipline

- Core engine must use Python standard library only.
- Optional dependencies (pandas, plotly, matplotlib) must be isolated.
- The TUI layer must work in SSH-only environments.

---

## 8. Terminal Reality

- Rendering must adapt to available terminal size.
- Truncation must be intentional and documented.
- Unicode glyphs must degrade gracefully if unsupported.

---

## Final Rule

If a feature conflicts with these invariants, the feature is wrong.

