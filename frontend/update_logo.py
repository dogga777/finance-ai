"""FinSight AI — Pure glass logo update."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "src"

# =====================================================
# Layout.jsx — new glass logo markup
# =====================================================
LAYOUT = '''
import { NavLink, Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import {
  IconDashboard,
  IconUpload,
  IconChart,
  IconTrending,
  IconAlert,
  IconFile,
} from "./Icons";

const links = [
  { to: "/dashboard", label: "Dashboard", Icon: IconDashboard },
  { to: "/upload", label: "Upload Data", Icon: IconUpload },
  { to: "/analysis", label: "Analysis", Icon: IconChart },
  { to: "/predictions", label: "Predictions", Icon: IconTrending },
  { to: "/anomalies", label: "Anomalies", Icon: IconAlert },
  { to: "/reports", label: "Reports", Icon: IconFile },
];

function GlassLogo() {
  return (
    <div className="glass-logo">
      <div className="glass-logo-mark">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <defs>
            <linearGradient id="glass-grad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#a5b4fc" />
              <stop offset="50%" stopColor="#c4b5fd" />
              <stop offset="100%" stopColor="#f0abfc" />
            </linearGradient>
          </defs>
          <path
            d="M5 19V7.5c0-1 .8-1.8 1.8-1.8h5.4c2 0 3.6 1.6 3.6 3.6s-1.6 3.6-3.6 3.6H8"
            stroke="url(#glass-grad)"
            strokeWidth="2.2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <circle cx="17.5" cy="15.5" r="2" stroke="url(#glass-grad)" strokeWidth="2" />
        </svg>
      </div>
      <div className="glass-logo-text">
        <span className="glass-brand-main">FinSight</span>
        <span className="glass-brand-tag">AI</span>
      </div>
    </div>
  );
}

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <GlassLogo />

        <div className="nav-section-label">Workspace</div>

        <nav className="nav-list">
          {links.map(({ to, label, Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => (isActive ? "active" : "")}
            >
              <span className="nav-icon"><Icon size={18} /></span>
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-chip">
            <div className="user-avatar">
              {user?.full_name?.[0]?.toUpperCase() || "U"}
            </div>
            <div className="user-meta">
              <div className="user-name">{user?.full_name || "User"}</div>
              <div className="user-email">{user?.email}</div>
            </div>
          </div>
          <button className="btn-ghost" onClick={handleLogout}>
            Sign out
          </button>
        </div>
      </aside>

      <div className="main">
        <header className="topbar">
          <div className="title">Intelligent Financial Analytics</div>
          <div className="actions">
            <div className="status-pill">
              <span className="status-dot" />
              API Online
            </div>
          </div>
        </header>
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
'''

# =====================================================
# index.css — new glass logo styles + remove old
# =====================================================
CSS_OVERRIDE = '''

/* =====================================================
   PURE GLASS LOGO
   ===================================================== */

.glass-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  margin: 0 4px 28px;
  border-radius: 14px;

  /* glass morphism */
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
    0 12px 32px rgba(79, 110, 247, 0.2);
}

.glass-logo-mark {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  position: relative;

  /* inner glass tile */
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
  background: linear-gradient(
    135deg,
    #a5b4fc 0%,
    #c4b5fd 50%,
    #e9d5ff 100%
  );
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

/* Neutralize the old .sidebar .brand styles */
.sidebar .brand { display: none; }
'''

path_css = ROOT / "index.css"
existing = path_css.read_text(encoding="utf-8")

# Remove any old block if re-run
marker = "/* =====================================================\n   PURE GLASS LOGO"
if marker in existing:
    existing = existing.split(marker)[0].rstrip() + "\n"

path_css.write_text(existing + CSS_OVERRIDE, encoding="utf-8")
print(f"  updated  src/index.css")

path_layout = ROOT / "components" / "Layout.jsx"
path_layout.write_text(LAYOUT.lstrip("\\n"), encoding="utf-8")
print(f"  updated  src/components/Layout.jsx")

print("\\nDone. 2 files updated.")