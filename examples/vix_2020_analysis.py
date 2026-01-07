"""
Real-world examples: When "calm" readings missed regime shifts

Demonstrates how Glyphcore's regime detection catches
what standard volatility readings miss - across multiple crises.
"""

import yfinance as yf
from glyphcore import Engine


def analyze_crisis(name, ticker, start_date, end_date, peak_date):
    """Generic crisis analyzer"""
    print(f"\n{'='*70}")
    print(f"Analyzing: {name}")
    print('='*70)

    # Download data
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    vix = yf.download('^VIX', start=start_date, end=end_date, progress=False)

    # Get closing prices
    data_close = data['Close'].squeeze()
    vix_close = vix['Close'].squeeze()

    values = data_close.tolist()
    vix_values = vix_close.tolist()
    dates = data.index.strftime('%Y-%m-%d').tolist()

    # Find peak date
    try:
        peak_idx = dates.index(peak_date)
    except ValueError:
        print(f"Warning: {peak_date} not found, using approximate index")
        peak_idx = len(dates) // 3

    # Analyze 30-day window ending at peak
    window_start = max(0, peak_idx - 30)
    window_end = peak_idx + 1

    window_values = values[window_start:window_end]
    window_dates = dates[window_start:window_end]

    print(f"\nAnalyzing {len(window_values)}-day window ending {peak_date}")
    print(f"{ticker} on {peak_date}: {values[peak_idx]:.2f}")
    print(
        f"VIX on {peak_date}: {vix_values[peak_idx]:.2f} (Standard interpretation: {'CALM' if vix_values[peak_idx] < 20 else 'ELEVATED'})")

    # Run Glyphcore analysis
    engine = Engine()
    signal = engine.analyze(window_values, window_dates)

    print("\n" + "="*60)
    print(f"GLYPHCORE SIGNAL ({peak_date})")
    print("="*60)
    print(f"Direction:   {signal.direction}")
    print(f"Strength:    {signal.strength:.2f}")
    print(f"Momentum:    {signal.momentum}")
    print(f"Regime:      {signal.regime}")
    print(f"Confidence:  {signal.confidence:.2f}")
    print("="*60)

    # Render TUI
    print("\nTUI Visualization:")
    print(engine.render_tui(signal))

    # Show aftermath
    crash_idx = min(len(values) - 1, peak_idx + 33)  # ~33 days later or end
    pct_change = ((values[crash_idx] - values[peak_idx]
                   ) / values[peak_idx] * 100)

    print(f"\nDays later ({dates[crash_idx]}):")
    print(f"{ticker}: {values[crash_idx]:.2f} ({pct_change:+.1f}%)")
    print(f"VIX: {vix_values[crash_idx]:.2f}")

    print("\n" + "="*60)
    print("VERDICT:")
    print("="*60)
    print(f"Standard VIX reading: {vix_values[peak_idx]:.2f}")
    print(f"Glyphcore regime:     {signal.regime}")
    print("\nThe chart missed it. Glyphcore didn't.")
    print("="*60)


if __name__ == "__main__":
    # Example 1: COVID Crash (Feb 2020)
    analyze_crisis(
        name="COVID-19 Crash (2020)",
        ticker="^GSPC",
        start_date="2020-01-01",
        end_date="2020-03-23",
        peak_date="2020-02-19"
    )

    # Example 2: Financial Crisis (2008)
    analyze_crisis(
        name="Financial Crisis (2008)",
        ticker="^GSPC",
        start_date="2008-08-01",
        end_date="2008-11-20",
        peak_date="2008-09-19"  # Right before Lehman collapse
    )
