"""Generate natural language explanations of predictions."""


def explain_prediction(ratios: dict, predictions: dict, anomalies: dict) -> dict:
    """Build a human-readable explanation for the current forecast."""
    parts = []
    drivers = []

    rev = ratios.get("net_profit_margin", 0)
    debt = ratios.get("debt_ratio", 0)
    current = ratios.get("current_ratio", 0)

    if rev > 0.10:
        parts.append(f"Strong net profit margin of {rev*100:.1f}%")
        drivers.append(("profitability", "positive", rev))
    elif rev > 0:
        parts.append(f"Modest net profit margin of {rev*100:.1f}%")
        drivers.append(("profitability", "neutral", rev))
    else:
        parts.append(f"Negative profit margin ({rev*100:.1f}%)")
        drivers.append(("profitability", "negative", rev))

    if current < 1.0:
        parts.append("Current ratio below 1.0 suggests liquidity pressure")
        drivers.append(("liquidity", "negative", current))
    elif current > 2.0:
        parts.append(f"Healthy liquidity (current ratio {current:.2f})")
        drivers.append(("liquidity", "positive", current))

    if debt > 0.6:
        parts.append(f"High leverage (debt ratio {debt:.2f})")
        drivers.append(("leverage", "negative", debt))

    cf_values = predictions.get("predicted_values") or []
    if cf_values and len(cf_values) >= 2:
        delta = (cf_values[-1] - cf_values[0]) / abs(cf_values[0]) if cf_values[0] else 0
        if delta > 0.05:
            parts.append(f"Cash flow is projected to grow {delta*100:.1f}% over the horizon")
        elif delta < -0.05:
            parts.append(f"Cash flow is projected to decline {abs(delta)*100:.1f}% — consider cost controls")
        else:
            parts.append("Cash flow is expected to remain roughly stable")

    if anomalies.get("risk_level") == "High":
        parts.append("Multiple anomalous periods detected — investigate unusual transactions")

    summary = ". ".join(parts) + "."
    return {
        "summary": summary,
        "drivers": [
            {"factor": f, "impact": i, "value": round(float(v), 4)}
            for f, i, v in drivers
        ],
    }
