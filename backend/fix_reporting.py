"""Overwrites app/services/reporting.py with a robust version."""
from pathlib import Path

CONTENT = '''
import json
from typing import Any, Dict

from fpdf import FPDF


def build_summary_json(ratios, score, predictions, anomalies, recommendations) -> str:
    return json.dumps({
        "ratios": ratios,
        "score": score,
        "predictions": predictions,
        "anomalies": anomalies,
        "recommendations": recommendations,
    })


def _cell(pdf, h, text):
    """Write one line, safely encoding UTF-8 -> latin-1."""
    safe = str(text).encode("latin-1", "replace").decode("latin-1")
    pdf.cell(0, h, safe, ln=True)


def _multi(pdf, h, text):
    safe = str(text).encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, h, safe)


def build_pdf(summary: Dict[str, Any], company_name: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    _cell(pdf, 10, f"FinSight AI Report - {company_name}")

    pdf.set_font("Helvetica", "", 12)
    pdf.ln(4)
    _cell(pdf, 8, f"Health Score: {summary['score']['score']}/100")
    _cell(pdf, 8, f"Risk Level: {summary['score']['risk_level']}")

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    _cell(pdf, 8, "Financial Ratios")
    pdf.set_font("Helvetica", "", 11)
    for key, value in summary["ratios"].items():
        _cell(pdf, 7, f"{key}: {value}")

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 13)
    _cell(pdf, 8, "Cash Flow Forecast")
    pdf.set_font("Helvetica", "", 11)
    for i, v in enumerate(summary["predictions"]["predicted_values"], start=1):
        _cell(pdf, 7, f"Period +{i}: {v}")

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 13)
    _cell(pdf, 8, "Recommendations")
    pdf.set_font("Helvetica", "", 11)
    for rec in summary["recommendations"]:
        _multi(pdf, 7, f"- {rec}")

    # fpdf2 >= 2.7 returns bytes from output() regardless of dest kwarg.
    # Older versions return str. Handle both.
    result = pdf.output()
    if isinstance(result, str):
        return result.encode("latin-1")
    return bytes(result)
'''

path = Path("app/services/reporting.py")
path.write_text(CONTENT.lstrip("\n"), encoding="utf-8")
print(f"Overwritten: {path.resolve()}")