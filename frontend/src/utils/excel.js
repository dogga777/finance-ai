import * as XLSX from "xlsx";

const NUMERIC = [
  "revenue", "expenses", "assets", "liabilities", "equity",
  "inventory", "operating_cash_flow", "investing_cash_flow",
  "financing_cash_flow", "net_profit",
];

export async function parseExcelFile(file) {
  const buf = await file.arrayBuffer();
  const wb = XLSX.read(buf, { type: "array" });
  const sheet = wb.Sheets[wb.SheetNames[0]];
  const rows = XLSX.utils.sheet_to_json(sheet, { defval: 0 });

  if (!rows.length) throw new Error("Excel sheet is empty");

  return rows.map((r, i) => {
    const norm = {};
    Object.keys(r).forEach((k) => {
      norm[k.trim().toLowerCase()] = r[k];
    });

    if (!norm.period) throw new Error(`Row ${i + 2}: missing "period" column`);
    const obj = { period: String(norm.period).trim() };
    NUMERIC.forEach((f) => {
      const v = norm[f];
      obj[f] = v === "" || v === undefined ? 0 : Number(v);
      if (Number.isNaN(obj[f])) {
        throw new Error(`Row ${i + 2}: "${f}" is not a number (got "${v}")`);
      }
    });
    return obj;
  });
}
