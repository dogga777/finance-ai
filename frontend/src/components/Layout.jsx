
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
          
        </header>
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

