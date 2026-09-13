/**
 * Parse a CSV string into an array of objects.
 * Handles quoted fields, commas inside quotes, CRLF/LF.
 */
export function parseCSV(text) {
  const rows = [];
  let row = [];
  let field = "";
  let inQuotes = false;
  let i = 0;

  // strip BOM
  if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);

  while (i < text.length) {
    const ch = text[i];

    if (inQuotes) {
      if (ch === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i += 2;
          continue;
        }
        inQuotes = false;
        i++;
        continue;
      }
      field += ch;
      i++;
      continue;
    }

    if (ch === '"') {
      inQuotes = true;
      i++;
      continue;
    }

    if (ch === ",") {
      row.push(field);
      field = "";
      i++;
      continue;
    }

    if (ch === "\n") {
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
      i++;
      continue;
    }

    if (ch === "\r") {
      i++;
      continue;
    }

    field += ch;
    i++;
  }

  // last cell
  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }

  if (rows.length === 0) return [];

  const headers = rows[0].map((h) => h.trim());
  const dataRows = rows.slice(1).filter((r) => r.some((c) => c.trim() !== ""));

  return dataRows.map((r) => {
    const obj = {};
    headers.forEach((h, idx) => {
      obj[h] = (r[idx] ?? "").trim();
    });
    return obj;
  });
}

/** Convert parsed CSV rows into Statement objects for the API. */
export function rowsToStatements(rows) {
  const NUMERIC = [
    "revenue", "expenses", "assets", "liabilities", "equity",
    "inventory", "operating_cash_flow", "investing_cash_flow",
    "financing_cash_flow", "net_profit",
  ];

  return rows.map((r, i) => {
    if (!r.period) {
      throw new Error(`Row ${i + 2}: missing "period" column`);
    }
    const obj = { period: String(r.period).trim() };
    NUMERIC.forEach((f) => {
      const v = r[f];
      obj[f] = v === "" || v === undefined ? 0 : Number(v);
      if (Number.isNaN(obj[f])) {
        throw new Error(`Row ${i + 2}: "${f}" is not a number (got "${v}")`);
      }
    });
    return obj;
  });
}
