# API Refactor Summary

## Overview

The codebase has been refactored to match the clean API design where:
- **Signal** is the semantic contract between TUI and GUI
- **Engine** is the orchestrator that never draws directly
- Internal details (glyph selection, framebuffer, interpolation) are hidden

## New Structure

```
glyphcore/
├── __init__.py           # exports Engine, Signal
├── core/
│   ├── __init__.py
│   └── signal.py         # Signal dataclass (frozen, semantic contract)
├── engine/
│   ├── __init__.py
│   ├── analyzer.py       # Semantic analysis (direction, momentum, regime, confidence)
│   ├── normalize.py      # Coordinate transformation
│   └── engine.py         # Main Engine orchestrator
└── renderers/
    ├── __init__.py
    ├── tui.py            # TUI glyph renderer (takes Signal)
    └── gui.py            # GUI pixel renderer (optional, takes Signal)
```

## API Changes

### Before (Old API)
```python
from glyphcore import GlyphEngine

engine = GlyphEngine(width=80, height=24)
output = engine.render_tui(df, price_col='price', time_col='time', threshold=0.2)
```

### After (New API)
```python
from glyphcore import Engine

engine = Engine(width=80, height=24)

# Step 1: Analyze raw data → Signal
signal = engine.analyze(
    values=[42000, 43000, 48000, 45500, 46000],
    labels=['00:00', '01:00', '02:00', '03:00', '04:00']
)

# Step 2: Render Signal → TUI string
output = engine.render_tui(signal)

# Step 3: Optional GUI escalation
engine.render_gui(signal)
```

## Key Improvements

### 1. Signal as Semantic Contract
- **Frozen dataclass**: Immutable contract
- **Rich semantics**: direction, strength, momentum, regime, confidence
- **Shared truth**: Both TUI and GUI consume the same Signal
- **No invention**: Renderers cannot add properties not in Signal

### 2. Engine as Orchestrator
- **analyze()**: Converts raw data → Signal (the brain)
- **render_tui()**: Takes Signal → returns ANSI string
- **render_gui()**: Takes Signal → opens GUI window (optional)
- **Never draws**: All rendering delegated to renderers

### 3. Hidden Implementation Details
- ❌ Glyph selection rules (internal to TUIRenderer)
- ❌ Framebuffer internals (internal to TUIRenderer)
- ❌ Interpolation strategies (internal to TUIRenderer)
- ❌ Signal thresholds (computed by Analyzer)
- ❌ Rendering styles (internal to renderers)

### 4. Clean Separation
- **core/**: Signal contract (what)
- **engine/**: Analysis and orchestration (how)
- **renderers/**: Visualization (presentation)

## Signal Properties

```python
@dataclass(frozen=True)
class Signal:
    direction: str        # "UP" | "DOWN" | "FLAT"
    strength: float      # 0.0 - 1.0 (normalized magnitude)
    momentum: str         # "ACCELERATING" | "DECELERATING" | "STABLE"
    regime: str           # "TREND" | "RANGE" | "VOLATILE"
    confidence: float     # 0.0 - 1.0 (certainty)
    values: list[float]   # raw data series
    labels: list[str]     # optional x-axis labels
```

## Example Usage

```python
import pandas as pd
from glyphcore import Engine

# Load data
df = pd.DataFrame({
    'time': pd.date_range('2026-01-03', periods=5, freq='h'),
    'price': [42000, 43000, 48000, 45500, 46000]
})

# Create engine
engine = Engine(width=80, height=24)

# Analyze
labels = [t.strftime('%H:%M') for t in df['time']]
signal = engine.analyze(values=df['price'].tolist(), labels=labels)

# Inspect signal
print(f"Direction: {signal.direction}")      # UP
print(f"Strength: {signal.strength:.2f}")    # 0.67
print(f"Momentum: {signal.momentum}")        # DECELERATING
print(f"Regime: {signal.regime}")            # VOLATILE
print(f"Confidence: {signal.confidence:.2f}") # 0.72

# Render TUI
output = engine.render_tui(signal)
print(output)

# Optional: GUI escalation
engine.render_gui(signal)  # Opens interactive window
```

## Migration Guide

If you have code using the old API:

1. **Replace GlyphEngine with Engine**
   ```python
   # Old
   from glyphcore import GlyphEngine
   engine = GlyphEngine(width=80, height=24)
   
   # New
   from glyphcore import Engine
   engine = Engine(width=80, height=24)
   ```

2. **Extract values and labels before rendering**
   ```python
   # Old
   output = engine.render_tui(df, price_col='price', time_col='time')
   
   # New
   signal = engine.analyze(
       values=df['price'].tolist(),
       labels=df['time'].astype(str).tolist()
   )
   output = engine.render_tui(signal)
   ```

3. **Access signal properties instead of engine.signals**
   ```python
   # Old
   for s in engine.signals:
       print(s.type, s.strength)
   
   # New
   print(signal.direction, signal.strength)
   print(signal.momentum, signal.regime, signal.confidence)
   ```

## Benefits

✅ **Clean API**: Clear separation of concerns  
✅ **Extensible**: Easy to add new renderers  
✅ **Testable**: Signal is pure data, renderers are isolated  
✅ **Understandable**: Architecture matches mental model  
✅ **Trustworthy**: Internal details hidden, contract enforced  
✅ **Production-ready**: Framework quality, not prototype  

## Status

✅ All components refactored  
✅ Tests updated  
✅ Examples updated  
✅ README updated  
✅ No linter errors  
✅ Backward compatibility: None (breaking change, but cleaner API)

