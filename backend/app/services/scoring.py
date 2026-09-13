def financial_health_score(ratios: dict) -> dict:
    if not ratios:
        return {"score": 0.0, "risk_level": "Unknown"}

    score = 0.0
    score += min(ratios.get("current_ratio", 0) / 2.0, 1) * 20
    score += min(ratios.get("quick_ratio", 0) / 1.5, 1) * 15
    score += max(0.0, 1 - ratios.get("debt_ratio", 1)) * 20
    score += min(max(ratios.get("roa", 0), 0) / 0.10, 1) * 15
    score += min(max(ratios.get("roe", 0), 0) / 0.15, 1) * 15
    score += min(max(ratios.get("net_profit_margin", 0), 0) / 0.20, 1) * 15

    score = round(min(score, 100), 2)

    if score >= 80:
        risk = "Low"
    elif score >= 60:
        risk = "Medium"
    else:
        risk = "High"

    return {"score": score, "risk_level": risk}
