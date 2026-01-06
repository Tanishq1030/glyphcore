"""
Example usage of Engine for TUI charting with new API.

Demonstrates:
- Semantic analysis (analyze)
- TUI rendering (render_tui)
- Signal properties (direction, momentum, regime, confidence)
"""

import pandas as pd
from glyphcore import Engine

# Example 1: BTC price spike (from spec)
print("=" * 80)
print("Example 1: BTC Price Spike (Jan 3, 2026)")
print("=" * 80)
print()

data1 = {
    'time': pd.date_range('2026-01-03', periods=5, freq='h'),
    'price': [42000, 43000, 48000, 45500, 46000]
}
df1 = pd.DataFrame(data1)

engine1 = Engine(width=80, height=24)
labels1 = [t.strftime('%H:%M') if hasattr(t, 'strftime') else str(t) for t in df1['time']]
signal1 = engine1.analyze(
    values=df1['price'].tolist(),
    labels=labels1
)

output1 = engine1.render_tui(signal1)
print(output1)
print(f"\nSignal: {signal1.direction} | {signal1.momentum} | {signal1.regime}")
print(f"Strength: {signal1.strength:.2f}, Confidence: {signal1.confidence:.2f}")

print("\n" + "=" * 80)
print("Example 2: Smaller Canvas")
print("=" * 80)
print()

# Example 2: Smaller canvas
engine2 = Engine(width=60, height=15)
signal2 = engine2.analyze(
    values=df1['price'].tolist(),
    labels=labels1
)

output2 = engine2.render_tui(signal2)
print(output2)
print(f"\nSignal: {signal2.direction} | {signal2.momentum} | {signal2.regime}")

print("\n" + "=" * 80)
print("Example 3: Flatline Handling")
print("=" * 80)
print()

# Example 3: Test flatline
data3 = {
    'time': pd.date_range('2026-01-03', periods=3, freq='h'),
    'price': [45000, 45000, 45000]  # Flatline
}
df3 = pd.DataFrame(data3)

engine3 = Engine(width=60, height=15)
labels3 = [t.strftime('%H:%M') if hasattr(t, 'strftime') else str(t) for t in df3['time']]
signal3 = engine3.analyze(
    values=df3['price'].tolist(),
    labels=labels3
)

output3 = engine3.render_tui(signal3)
print(output3)
print(f"\nSignal: {signal3.direction} | {signal3.momentum} | {signal3.regime}")
print(f"Confidence: {signal3.confidence:.2f} (should be high for consistent flatline)")

print("\n" + "=" * 80)
print("Example 4: Volatile Regime")
print("=" * 80)
print()

# Example 4: Volatile data
data4 = {
    'time': pd.date_range('2026-01-03', periods=10, freq='h'),
    'price': [42000, 45000, 41000, 46000, 40000, 47000, 39000, 48000, 38000, 49000]
}
df4 = pd.DataFrame(data4)

engine4 = Engine(width=70, height=18)
labels4 = [t.strftime('%H:%M') if hasattr(t, 'strftime') else str(t) for t in df4['time']]
signal4 = engine4.analyze(
    values=df4['price'].tolist(),
    labels=labels4
)

output4 = engine4.render_tui(signal4)
print(output4)
print(f"\nSignal: {signal4.direction} | {signal4.momentum} | {signal4.regime}")
print(f"Strength: {signal4.strength:.2f}, Confidence: {signal4.confidence:.2f}")
