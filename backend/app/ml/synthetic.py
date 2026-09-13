import random


def generate_synthetic(periods: int = 36, base_revenue: float = 100000) -> list:
    rows = []
    revenue = base_revenue
    for i in range(periods):
        revenue *= 1 + random.uniform(-0.03, 0.06)
        expenses = revenue * random.uniform(0.6, 0.85)
        assets = revenue * random.uniform(3.5, 6.0)
        liabilities = assets * random.uniform(0.3, 0.55)
        equity = assets - liabilities
        inventory = assets * random.uniform(0.08, 0.18)
        net_profit = revenue - expenses
        operating_cf = net_profit * random.uniform(0.7, 1.2)
        year = 2022 + (i // 12)
        month = (i % 12) + 1
        rows.append({
            "period": f"{year}-{month:02d}",
            "revenue": round(revenue, 2),
            "expenses": round(expenses, 2),
            "assets": round(assets, 2),
            "liabilities": round(liabilities, 2),
            "equity": round(equity, 2),
            "inventory": round(inventory, 2),
            "operating_cash_flow": round(operating_cf, 2),
            "investing_cash_flow": round(-revenue * 0.03, 2),
            "financing_cash_flow": round(revenue * 0.02, 2),
            "net_profit": round(net_profit, 2),
        })
    return rows
