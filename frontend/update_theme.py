"""FinSight AI — Full dark glassmorphism theme."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "src"

CSS = r'''
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  /* Dark canvas */
  --bg-base: #05060c;
  --bg-deep: #080b18;
  --bg-glow-1: rgba(79, 110, 247, 0.18);
  --bg-glow-2: rgba(139, 92, 246, 0.15);
  --bg-glow-3: rgba(236, 72, 153, 0.10);

  /* Glass surfaces */
  --glass-1: rgba(255, 255, 255, 0.045);
  --glass-2: rgba(255, 255, 255, 0.028);
  --glass-border: rgba(255, 255, 255, 0.09);
  --glass-border-hover: rgba(165, 180, 252, 0.28);
  --glass-inner: inset 0 1px 0 rgba(255, 255, 255, 0.06);

  /* Text */
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --text-dim: #64748b;

  /* Accents */
  --accent: #6366f1;
  --accent-2: #8b5cf6;
  --accent-3: #ec4899;
  --accent-soft: rgba(99, 102, 241, 0.15);
  --accent-glow: rgba(99, 102, 241, 0.4);

  --success: #10b981;
  --success-soft: rgba(16, 185, 129, 0.15);
  --warning: #f59e0b;
  --warning-soft: rgba(245, 158, 11, 0.15);
  --danger: #ef4444;
  --danger-soft: rgba(239, 68, 68, 0.15);

  --radius: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --transition: 180ms cubic-bezier(0.4, 0, 0.2, 1);
}

* { box-sizing: border-box; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
html, body, #root { height: 100%; }

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  color: var(--text-primary);
  background: var(--bg-base);
  line-height: 1.5;
  overflow-x: hidden;
}

/* =====================================================
   AMBIENT BACKGROUND (fixed, spans whole viewport)
   ===================================================== */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 70% 55% at 15% 10%, var(--bg-glow-1), transparent 60%),
    radial-gradient(ellipse 60% 50% at 85% 90%, var(--bg-glow-2), transparent 60%),
    radial-gradient(ellipse 50% 40% at 50% 50%, var(--bg-glow-3), transparent 70%),
    linear-gradient(180deg, #05060c 0%, #080b18 40%, #05060c 100%);
  z-index: -2;
  pointer-events: none;
}

body::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
  background-size: 56px 56px;
  z-index: -1;
  pointer-events: none;
  mask-image: radial-gradient(ellipse 90% 80% at 50% 50%, black 40%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 90% 80% at 50% 50%, black 40%, transparent 100%);
}

a {
  color: #a5b4fc;
  text-decoration: none;
  transition: color var(--transition);
}
a:hover { color: #c7d2fe; }

/* =====================================================
   APP SHELL
   ===================================================== */
.app-shell {
  display: flex;
  min-height: 100vh;
  position: relative;
}

/* =====================================================
   SIDEBAR — frosted glass column
   ===================================================== */
.sidebar {
  width: 268px;
  flex-shrink: 0;
  padding: 22px 14px;
  display: flex;
  flex-direction: column;
  position: relative;
  background: linear-gradient(180deg, rgba(10, 14, 28, 0.75) 0%, rgba(5, 6, 12, 0.85) 100%);
  backdrop-filter: blur(24px) saturate(150%);
  -webkit-backdrop-filter: blur(24px) saturate(150%);
  border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 1px;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(165, 180, 252, 0.15) 50%,
    transparent 100%
  );
}

.nav-section-label {
  color: #4b5563;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.4px;
  padding: 0 14px;
  margin: 6px 0 8px;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
}

.sidebar a {
  color: var(--text-muted);
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 500;
  text-decoration: none;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  border: 1px solid transparent;
}

.sidebar a .nav-icon {
  display: inline-flex;
  opacity: 0.85;
  transition: opacity var(--transition);
}

.sidebar a:hover {
  background: rgba(255, 255, 255, 0.04);
  color: #e2e8f0;
  border-color: rgba(255, 255, 255, 0.05);
}

.sidebar a.active {
  color: #fff;
  background: linear-gradient(
    135deg,
    rgba(99, 102, 241, 0.22) 0%,
    rgba(139, 92, 246, 0.16) 100%
  );
  border-color: rgba(165, 180, 252, 0.22);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 4px 18px rgba(99, 102, 241, 0.25);
}

.sidebar a.active::before {
  content: '';
  position: absolute;
  left: -14px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 22px;
  border-radius: 0 3px 3px 0;
  background: linear-gradient(180deg, #a5b4fc, #c4b5fd);
  box-shadow: 0 0 12px rgba(165, 180, 252, 0.7);
}

.sidebar a.active .nav-icon { opacity: 1; }

/* ---------- Footer ---------- */
.sidebar-footer {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  margin-bottom: 10px;
}

.user-avatar {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-weight: 700;
  font-size: 14px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.user-meta { min-width: 0; flex: 1; }
.user-name {
  color: #e2e8f0;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.user-email {
  color: #64748b;
  font-size: 11px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-ghost {
  width: 100%;
  background: rgba(255, 255, 255, 0.035);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: none;
  font-size: 13px;
  padding: 9px 12px;
}
.btn-ghost:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.07);
  color: #fff;
  transform: none;
  box-shadow: none;
  border-color: rgba(255, 255, 255, 0.12);
}

/* =====================================================
   MAIN AREA
   ===================================================== */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  position: relative;
}

/* ---------- Topbar ---------- */
.topbar {
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  background: rgba(8, 11, 24, 0.55);
  backdrop-filter: blur(20px) saturate(150%);
  -webkit-backdrop-filter: blur(20px) saturate(150%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  position: sticky;
  top: 0;
  z-index: 10;
}

.topbar .title {
  font-weight: 600;
  font-size: 15px;
  color: var(--text-secondary);
  letter-spacing: -0.1px;
}

.topbar .actions { display: flex; gap: 12px; align-items: center; }

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: rgba(16, 185, 129, 0.1);
  color: #6ee7b7;
  border: 1px solid rgba(16, 185, 129, 0.2);
  font-size: 12px;
  font-weight: 600;
  border-radius: 999px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25), 0 0 12px rgba(16, 185, 129, 0.8);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25), 0 0 12px rgba(16, 185, 129, 0.8); }
  50%      { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.1), 0 0 8px rgba(16, 185, 129, 0.5); }
}

.content {
  padding: 32px;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  animation: fadeInUp 380ms cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* =====================================================
   PAGE HEADER
   ===================================================== */
.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
}

.page-icon {
  width: 54px;
  height: 54px;
  border-radius: 14px;
  color: #fff;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.18),
    0 8px 24px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.page-title {
  margin: 0;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.7px;
  color: #f1f5f9;
}

.page-subtitle {
  margin: 4px 0 0;
  color: var(--text-muted);
  font-size: 14px;
}

/* =====================================================
   GLASS CARDS — the core visual language
   ===================================================== */
.card {
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.048) 0%,
    rgba(255, 255, 255, 0.018) 100%
  );
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 20px;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.055),
    0 12px 32px rgba(0, 0, 0, 0.28);
  transition: all var(--transition);
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.14),
    transparent
  );
  pointer-events: none;
}

.card:hover {
  border-color: var(--glass-border-hover);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 16px 40px rgba(0, 0, 0, 0.35),
    0 0 0 1px rgba(165, 180, 252, 0.06);
}

.card h2, .card h3 { color: #f1f5f9; letter-spacing: -0.3px; }

.card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 12px;
}

.header-icon-wrap {
  width: 42px;
  height: 42px;
  border-radius: 11px;
  color: #fff;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 6px 16px rgba(0, 0, 0, 0.3);
}

.card-title {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.3px;
  color: #f1f5f9;
}

.card-subtitle {
  margin: 2px 0 0;
  color: var(--text-muted);
  font-size: 13px;
}

.section-heading {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin: 26px 0 14px;
}

.section-heading h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.3px;
  color: #e2e8f0;
}

/* =====================================================
   GRIDS
   ===================================================== */
.grid { display: grid; gap: 16px; }
.grid-2 { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
.grid-3 { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
.grid-4 { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }

/* =====================================================
   BUTTONS
   ===================================================== */
button, .btn {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 11px 18px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  letter-spacing: -0.1px;
  transition: all var(--transition);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 4px 14px rgba(99, 102, 241, 0.35);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

button::after, .btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.15), transparent 50%);
  pointer-events: none;
  opacity: 0.5;
}

button:hover:not(:disabled), .btn:hover {
  transform: translateY(-1px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.25),
    0 8px 26px rgba(99, 102, 241, 0.5);
  color: #fff;
}

button:active:not(:disabled), .btn:active { transform: translateY(0); }
button:disabled { opacity: 0.45; cursor: not-allowed; box-shadow: none; }

.btn-success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 4px 14px rgba(16, 185, 129, 0.35);
}
.btn-success:hover:not(:disabled) {
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.25),
    0 8px 26px rgba(16, 185, 129, 0.5);
}

.btn-ghost-dark {
  background: rgba(255, 255, 255, 0.05);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.btn-ghost-dark::after { display: none; }
.btn-ghost-dark:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: none;
  transform: translateY(-1px);
}

/* =====================================================
   INPUTS — glass fields
   ===================================================== */
input, textarea, select {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  background: rgba(255, 255, 255, 0.035);
  color: #f1f5f9;
  transition: all var(--transition);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

input:hover, textarea:hover, select:hover {
  border-color: rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.05);
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: rgba(165, 180, 252, 0.5);
  background: rgba(99, 102, 241, 0.06);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.05),
    0 0 0 4px rgba(99, 102, 241, 0.15);
}

input::placeholder, textarea::placeholder { color: #64748b; }

select option { background: #0b1120; color: #f1f5f9; }

label {
  display: block;
  font-size: 12.5px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #cbd5e1;
  letter-spacing: 0.1px;
  text-transform: uppercase;
}

.form-row { margin-bottom: 16px; }
textarea { resize: vertical; line-height: 1.6; font-family: 'Inter', monospace; }

/* =====================================================
   TABLES
   ===================================================== */
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 13.5px;
  color: #e2e8f0;
}

th, td {
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

th {
  color: #94a3b8;
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.9px;
  background: rgba(255, 255, 255, 0.025);
}

tbody tr { transition: background var(--transition); }
tbody tr:hover { background: rgba(255, 255, 255, 0.025); }
tbody tr:last-child td { border-bottom: none; }

/* =====================================================
   BADGES & CHIPS
   ===================================================== */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 11px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: -0.1px;
  border: 1px solid transparent;
}

.badge::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
  box-shadow: 0 0 8px currentColor;
}

.badge.low {
  background: rgba(16, 185, 129, 0.12);
  color: #6ee7b7;
  border-color: rgba(16, 185, 129, 0.25);
}
.badge.medium {
  background: rgba(245, 158, 11, 0.12);
  color: #fcd34d;
  border-color: rgba(245, 158, 11, 0.25);
}
.badge.high {
  background: rgba(239, 68, 68, 0.12);
  color: #fca5a5;
  border-color: rgba(239, 68, 68, 0.25);
}

.chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.055);
  color: #cbd5e1;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

/* =====================================================
   COMPANY CARDS
   ===================================================== */
.company-card {
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.02) 100%
  );
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    0 12px 32px rgba(0, 0, 0, 0.28);
  overflow: hidden;
}

.company-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(165, 180, 252, 0.25), transparent);
}

.company-card:hover {
  transform: translateY(-4px);
  border-color: rgba(165, 180, 252, 0.28);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 20px 48px rgba(0, 0, 0, 0.4),
    0 0 32px rgba(99, 102, 241, 0.15);
}

.company-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.company-avatar {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-weight: 800;
  font-size: 15px;
  display: grid;
  place-items: center;
  letter-spacing: 0.5px;
  box-shadow: 0 8px 22px rgba(99, 102, 241, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.company-id {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 600;
  padding: 4px 9px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  letter-spacing: 0.3px;
}

.company-name {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.3px;
  color: #f1f5f9;
}

.company-meta { display: flex; gap: 6px; flex-wrap: wrap; }
.company-actions { display: flex; gap: 8px; margin-top: 4px; }
.company-actions .btn { flex: 1; padding: 8px 12px; font-size: 13px; }

/* =====================================================
   RATIO CARDS
   ===================================================== */
.ratio-card {
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.018) 100%
  );
  backdrop-filter: blur(18px) saturate(160%);
  -webkit-backdrop-filter: blur(18px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: var(--radius);
  padding: 18px;
  overflow: hidden;
  transition: all var(--transition);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.05),
    0 8px 20px rgba(0, 0, 0, 0.22);
}

.ratio-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
  opacity: 0.7;
}

.ratio-card:hover {
  border-color: rgba(165, 180, 252, 0.22);
  transform: translateY(-3px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 16px 32px rgba(0, 0, 0, 0.32),
    0 0 24px rgba(99, 102, 241, 0.12);
}

.ratio-label {
  color: #94a3b8;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.9px;
  margin-bottom: 10px;
}

.ratio-value {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.7px;
  margin-bottom: 14px;
  font-variant-numeric: tabular-nums;
}

.ratio-good { color: #6ee7b7; text-shadow: 0 0 20px rgba(16, 185, 129, 0.35); }
.ratio-warn { color: #fcd34d; text-shadow: 0 0 20px rgba(245, 158, 11, 0.35); }
.ratio-bad  { color: #fca5a5; text-shadow: 0 0 20px rgba(239, 68, 68, 0.35); }
.ratio-neutral { color: #c7d2fe; }

.ratio-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 999px;
  overflow: hidden;
}

.ratio-bar-fill {
  height: 100%;
  width: 100%;
  border-radius: 999px;
  animation: growBar 900ms cubic-bezier(0.4, 0, 0.2, 1);
}

.ratio-fill-good {
  background: linear-gradient(90deg, #10b981, #34d399);
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
}
.ratio-fill-warn {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.6);
}
.ratio-fill-bad {
  background: linear-gradient(90deg, #ef4444, #f87171);
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.6);
}
.ratio-fill-neutral {
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.6);
}

@keyframes growBar {
  from { transform: scaleX(0); transform-origin: left; }
  to   { transform: scaleX(1); transform-origin: left; }
}

/* =====================================================
   SCORE CARD (analysis / reports hero)
   ===================================================== */
.score-card {
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(99, 102, 241, 0.08) 0%,
    rgba(139, 92, 246, 0.05) 50%,
    rgba(255, 255, 255, 0.02) 100%
  );
  backdrop-filter: blur(24px) saturate(160%);
  -webkit-backdrop-filter: blur(24px) saturate(160%);
  border: 1px solid rgba(165, 180, 252, 0.15);
  border-radius: var(--radius-lg);
  padding: 32px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 32px;
  align-items: center;
  margin-bottom: 20px;
  overflow: hidden;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 16px 40px rgba(0, 0, 0, 0.35),
    0 0 64px rgba(99, 102, 241, 0.08);
}

.score-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899, #f59e0b, #10b981);
  background-size: 200% 100%;
  animation: gradientShift 6s linear infinite;
}

@keyframes gradientShift {
  from { background-position: 0% 0; }
  to   { background-position: 200% 0; }
}

.score-card-left { min-width: 0; }

.score-card-label {
  font-size: 19px;
  font-weight: 800;
  color: #f1f5f9;
  letter-spacing: -0.4px;
}

/* =====================================================
   RECOMMENDATIONS
   ===================================================== */
.recommendation {
  position: relative;
  padding: 14px 18px 14px 52px;
  background: linear-gradient(
    135deg,
    rgba(99, 102, 241, 0.1) 0%,
    rgba(139, 92, 246, 0.06) 100%
  );
  border: 1px solid rgba(165, 180, 252, 0.15);
  border-left: 3px solid #6366f1;
  border-radius: 10px;
  margin-bottom: 10px;
  font-size: 14px;
  color: #e2e8f0;
  line-height: 1.55;
  transition: all var(--transition);
}

.recommendation:hover {
  transform: translateX(4px);
  border-color: rgba(165, 180, 252, 0.3);
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
}

.rec-num {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  display: grid;
  place-items: center;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* =====================================================
   STAT TILES
   ===================================================== */
.stats-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-tile {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.02) 100%
  );
  backdrop-filter: blur(18px) saturate(160%);
  -webkit-backdrop-filter: blur(18px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: var(--radius);
  transition: all var(--transition);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.05),
    0 8px 20px rgba(0, 0, 0, 0.22);
}

.stat-tile:hover {
  transform: translateY(-2px);
  border-color: rgba(165, 180, 252, 0.22);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 12px 28px rgba(0, 0, 0, 0.3),
    0 0 24px rgba(99, 102, 241, 0.1);
}

.stat-tile-icon {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  color: #fff;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.25),
    0 6px 18px rgba(0, 0, 0, 0.35);
}

.stat-tile-label {
  color: #94a3b8;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.9px;
  font-weight: 700;
  margin-bottom: 2px;
}

.stat-tile-value {
  font-size: 22px;
  font-weight: 800;
  color: #f1f5f9;
  letter-spacing: -0.5px;
}

/* =====================================================
   HERO BANNER
   ===================================================== */
.hero {
  position: relative;
  padding: 36px;
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at 88% 25%, rgba(139, 92, 246, 0.35), transparent 55%),
    radial-gradient(circle at 12% 80%, rgba(99, 102, 241, 0.3), transparent 55%),
    linear-gradient(135deg, rgba(20, 25, 50, 0.85), rgba(10, 14, 30, 0.9));
  border: 1px solid rgba(165, 180, 252, 0.12);
  margin-bottom: 24px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 20px 50px rgba(0, 0, 0, 0.4);
}

.hero-content { position: relative; z-index: 2; max-width: 640px; }

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 13px;
  border-radius: 999px;
  background: rgba(165, 180, 252, 0.1);
  border: 1px solid rgba(165, 180, 252, 0.25);
  color: #c7d2fe;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 16px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.hero-title {
  font-size: 34px;
  font-weight: 800;
  letter-spacing: -1.1px;
  margin: 0 0 10px;
  background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 50%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  color: #94a3b8;
  font-size: 15px;
  margin: 0;
  line-height: 1.6;
}

/* =====================================================
   EMPTY STATES
   ===================================================== */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.empty-state svg { opacity: 0.5; margin-bottom: 12px; }
.empty-state h3 {
  margin: 0;
  color: #e2e8f0;
  font-size: 18px;
  font-weight: 700;
}
.empty-state p { margin: 0; max-width: 400px; }

/* =====================================================
   SKELETON
   ===================================================== */
.skeleton {
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.03) 0%,
    rgba(255, 255, 255, 0.08) 50%,
    rgba(255, 255, 255, 0.03) 100%
  );
  background-size: 200% 100%;
  border-radius: 8px;
  animation: shimmer 1.4s infinite;
}
@keyframes shimmer {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}
.skeleton-card { padding: 24px; }

/* =====================================================
   AUTH PAGES — full glass experience
   ===================================================== */
.auth-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  position: relative;
  overflow: hidden;
  background: var(--bg-base);
}

.auth-shell::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 50% at 30% 20%, rgba(99, 102, 241, 0.35), transparent 60%),
    radial-gradient(ellipse 55% 45% at 75% 80%, rgba(139, 92, 246, 0.28), transparent 60%),
    radial-gradient(ellipse 45% 40% at 60% 30%, rgba(236, 72, 153, 0.18), transparent 65%),
    linear-gradient(135deg, #05060c 0%, #0b1120 50%, #1e1b4b 100%);
  pointer-events: none;
}

.auth-shell::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse 70% 60% at 50% 50%, black 40%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 50%, black 40%, transparent 100%);
  pointer-events: none;
}

.auth-card {
  width: 100%;
  max-width: 440px;
  padding: 40px;
  border-radius: var(--radius-xl);
  position: relative;
  z-index: 1;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.07) 0%,
    rgba(255, 255, 255, 0.025) 100%
  );
  backdrop-filter: blur(28px) saturate(180%);
  -webkit-backdrop-filter: blur(28px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.12),
    inset 0 -1px 0 rgba(0, 0, 0, 0.2),
    0 24px 64px rgba(0, 0, 0, 0.5),
    0 0 80px rgba(99, 102, 241, 0.1);
  animation: fadeInUp 400ms cubic-bezier(0.4, 0, 0.2, 1);
}

.auth-card h1 {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.7px;
  background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 60%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-card p.muted {
  color: #94a3b8;
  margin: 0 0 28px;
  font-size: 14px;
}

.auth-card button[type="submit"] {
  padding: 13px 18px;
  font-size: 15px;
  margin-top: 6px;
  width: 100%;
}

/* =====================================================
   MESSAGES
   ===================================================== */
.error {
  background: rgba(239, 68, 68, 0.1);
  color: #fca5a5;
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 14px;
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-left: 3px solid #ef4444;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.success {
  background: rgba(16, 185, 129, 0.1);
  color: #6ee7b7;
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 14px;
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-left: 3px solid #10b981;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* =====================================================
   UTILITY
   ===================================================== */
.muted { color: #94a3b8; }

/* =====================================================
   GLASS LOGO (kept from previous design)
   ===================================================== */
.glass-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  margin: 0 4px 28px;
  border-radius: 14px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.07) 0%,
    rgba(255, 255, 255, 0.02) 100%
  );
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.09);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    inset 0 -1px 0 rgba(0, 0, 0, 0.15),
    0 8px 24px rgba(0, 0, 0, 0.25);
  position: relative;
  overflow: hidden;
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-logo::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 200%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.05) 45%,
    rgba(255, 255, 255, 0.08) 50%,
    rgba(255, 255, 255, 0.05) 55%,
    transparent 100%
  );
  transform: skewX(-20deg);
  animation: glassSheen 6s ease-in-out infinite;
  pointer-events: none;
}

@keyframes glassSheen {
  0%, 100% { transform: translateX(-30%) skewX(-20deg); }
  50%      { transform: translateX(30%) skewX(-20deg); }
}

.glass-logo:hover {
  border-color: rgba(165, 180, 252, 0.25);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.12),
    0 12px 32px rgba(99, 102, 241, 0.25);
}

.glass-logo-mark {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(165, 180, 252, 0.15) 0%,
    rgba(196, 181, 253, 0.06) 100%
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.14);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.18),
    inset 0 -2px 6px rgba(0, 0, 0, 0.15);
}

.glass-logo-mark::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 10px;
  background: radial-gradient(
    circle at 30% 20%,
    rgba(255, 255, 255, 0.25),
    transparent 55%
  );
  pointer-events: none;
}

.glass-logo-text {
  display: flex;
  align-items: baseline;
  gap: 6px;
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.5px;
  line-height: 1;
}

.glass-brand-main {
  background: linear-gradient(135deg, #a5b4fc 0%, #c4b5fd 50%, #e9d5ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 1px 12px rgba(165, 180, 252, 0.35);
}

.glass-brand-tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  padding: 2px 7px;
  border-radius: 6px;
  color: #c7d2fe;
  background: rgba(165, 180, 252, 0.1);
  border: 1px solid rgba(165, 180, 252, 0.2);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  text-transform: uppercase;
}

.sidebar .brand { display: none; }

/* =====================================================
   SCROLLBAR
   ===================================================== */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.15); background-clip: padding-box; }

/* =====================================================
   RESPONSIVE
   ===================================================== */
@media (max-width: 900px) {
  .score-card { grid-template-columns: 1fr; text-align: center; }
}

@media (max-width: 768px) {
  .sidebar { width: 76px; padding: 18px 10px; }
  .glass-logo { padding: 8px; justify-content: center; margin-bottom: 22px; }
  .glass-logo-text, .nav-section-label { display: none; }
  .sidebar a { justify-content: center; font-size: 0; padding: 12px; }
  .sidebar a .nav-icon { font-size: 18px; }
  .sidebar-footer .user-meta, .sidebar-footer .btn-ghost { display: none; }
  .topbar { padding: 0 16px; }
  .content { padding: 20px 16px; }
  .page-title { font-size: 22px; }
  .hero-title { font-size: 26px; }
  .hero { padding: 26px 22px; }
}
'''

path = ROOT / "index.css"
path.write_text(CSS.lstrip("\n"), encoding="utf-8")
print(f"  updated  src/index.css ({len(CSS)} chars)")
print("\nDone. Full dark glass theme applied.")