def build_recommendations(ratios: dict, anomalies: dict, predictions: list) -> list:
    recs = []

    if ratios.get("current_ratio", 1) < 1:
        recs.append("Increase short-term liquidity to cover current liabilities.")
    if ratios.get("debt_ratio", 0) > 0.6:
        recs.append("Reduce overall debt — solvency risk is elevated.")
    if ratios.get("net_profit_margin", 0) < 0.05:
        recs.append("Improve net profit margin by reviewing cost structure.")
    if ratios.get("roe", 0) < 0.08:
        recs.append("Enhance return on equity — consider capital efficiency.")
    if anomalies.get("risk_level") == "High":
        recs.append("Investigate abnormal transactions flagged by the anomaly engine.")
    if predictions and predictions[0] < 0:
        recs.append("Cash flow is projected negative — delay non-critical spending.")
    if not recs:
        recs.append("Financial position is stable. Continue monitoring.")

    return recs
