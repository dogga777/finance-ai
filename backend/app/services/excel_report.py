"""Generate Excel report from the summary."""
import io
from typing import Any, Dict

import pandas as pd


def build_excel(summary: Dict[str, Any], company_name: str) -> bytes:
    """Return Excel file as bytes with multiple sheets."""
    buf = io.BytesIO()

    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        # Sheet 1: Overview
        overview = pd.DataFrame({
            "Metric": ["Company", "Financial Health Score", "Risk Level"],
            "Value": [
                company_name,
                summary["score"]["score"],
                summary["score"]["risk_level"],
            ],
        })
        overview.to_excel(writer, sheet_name="Overview", index=False)

        # Sheet 2: Ratios
        ratios_df = pd.DataFrame(
            [{"Ratio": k, "Value": v} for k, v in summary["ratios"].items()]
        )
        ratios_df.to_excel(writer, sheet_name="Ratios", index=False)

        # Sheet 3: Cash Flow Forecast
        fc = pd.DataFrame({
            "Period": [f"+{i+1}" for i in range(len(summary["predictions"]["predicted_values"]))],
            "Predicted Cash Flow": summary["predictions"]["predicted_values"],
        })
        fc.to_excel(writer, sheet_name="Forecast", index=False)

        # Sheet 4: Anomalies
        anom = pd.DataFrame({
            "Flagged Period Index": summary["anomalies"].get("indices", []),
        })
        anom.to_excel(writer, sheet_name="Anomalies", index=False)

        # Sheet 5: Recommendations
        recs = pd.DataFrame({"Recommendation": summary["recommendations"]})
        recs.to_excel(writer, sheet_name="Recommendations", index=False)

    return buf.getvalue()
