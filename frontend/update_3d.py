"""FinSight AI — 3D experience upgrade."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "src"
FILES = {}

# =====================================================
# hooks/useTilt.js — 3D tilt-on-hover
# =====================================================
FILES["hooks/useTilt.js"] = '''
import { useRef, useState, useCallback } from "react";

/**
 * Returns props to attach to any element for a 3D tilt effect
 * that follows the mouse cursor.
 */
export function useTilt({ max = 8, scale = 1.02, speed = 220 } = {}) {
  const ref = useRef(null);
  const [style, setStyle] = useState({
    transform: "perspective(900px) rotateX(0deg) rotateY(0deg) scale(1)",
    transition: `transform ${speed}ms cubic-bezier(0.4, 0, 0.2, 1)`,
    transformStyle: "preserve-3d",
  });

  const onMouseMove = useCallback(
    (e) => {
      const el = ref.current;
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      const rotX = (-y * max).toFixed(2);
      const rotY = (x * max).toFixed(2);
      setStyle({
        transform: `perspective(900px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(${scale})`,
        transition: `transform ${speed}ms cubic-bezier(0.4, 0, 0.2, 1)`,
        transformStyle: "preserve-3d",
      });
    },
    [max, scale, speed]
  );

  const onMouseLeave = useCallback(() => {
    setStyle({
      transform: "perspective(900px) rotateX(0deg) rotateY(0deg) scale(1)",
      transition: `transform ${speed}ms cubic-bezier(0.4, 0, 0.2, 1)`,
      transformStyle: "preserve-3d",
    });
  }, [speed]);

  return { ref, style, onMouseMove, onMouseLeave };
}
'''

# =====================================================
# components/Hero3D.jsx — animated 3D scene
# =====================================================
FILES["components/Hero3D.jsx"] = '''
import { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, OrbitControls } from "@react-three/drei";

function CoreOrb() {
  const outer = useRef();
  const inner = useRef();
  const ringA = useRef();
  const ringB = useRef();

  useFrame((state) => {
    const t = state.clock.elapsedTime;
    if (outer.current) {
      outer.current.rotation.y = t * 0.35;
      outer.current.rotation.x = t * 0.18;
    }
    if (inner.current) {
      inner.current.rotation.y = -t * 0.6;
    }
    if (ringA.current) {
      ringA.current.rotation.z = t * 0.5;
      ringA.current.rotation.x = Math.PI / 3 + Math.sin(t * 0.3) * 0.15;
    }
    if (ringB.current) {
      ringB.current.rotation.z = -t * 0.4;
      ringB.current.rotation.x = Math.PI / 2 + Math.cos(t * 0.35) * 0.2;
    }
  });

  return (
    <group>
      {/* Outer wireframe icosahedron */}
      <mesh ref={outer}>
        <icosahedronGeometry args={[1.35, 1]} />
        <meshBasicMaterial color="#8b5cf6" wireframe transparent opacity={0.55} />
      </mesh>

      {/* Inner glowing sphere */}
      <mesh ref={inner}>
        <icosahedronGeometry args={[0.65, 0]} />
        <meshStandardMaterial
          color="#6366f1"
          emissive="#6366f1"
          emissiveIntensity={1.4}
          roughness={0.2}
          metalness={0.6}
        />
      </mesh>

      {/* Orbiting ring A */}
      <mesh ref={ringA}>
        <torusGeometry args={[1.85, 0.008, 16, 128]} />
        <meshBasicMaterial color="#a5b4fc" transparent opacity={0.7} />
      </mesh>

      {/* Orbiting ring B */}
      <mesh ref={ringB}>
        <torusGeometry args={[2.05, 0.006, 16, 128]} />
        <meshBasicMaterial color="#ec4899" transparent opacity={0.55} />
      </mesh>

      {/* Ambient glow balls */}
      <ambientLight intensity={0.7} />
      <pointLight position={[3, 3, 3]} intensity={1.4} color="#6366f1" />
      <pointLight position={[-3, -3, -3]} intensity={1.0} color="#8b5cf6" />
      <pointLight position={[0, 0, 4]} intensity={0.6} color="#ec4899" />
    </group>
  );
}

function Particles() {
  const group = useRef();

  const positions = [];
  for (let i = 0; i < 180; i++) {
    const r = 2.4 + Math.random() * 1.6;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    positions.push(
      r * Math.sin(phi) * Math.cos(theta),
      r * Math.sin(phi) * Math.sin(theta),
      r * Math.cos(phi)
    );
  }

  useFrame((state) => {
    if (group.current) {
      group.current.rotation.y = state.clock.elapsedTime * 0.08;
      group.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.15) * 0.15;
    }
  });

  return (
    <group ref={group}>
      <points>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={positions.length / 3}
            array={new Float32Array(positions)}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          color="#c7d2fe"
          size={0.03}
          sizeAttenuation
          transparent
          opacity={0.75}
        />
      </points>
    </group>
  );
}

export default function Hero3D() {
  return (
    <div className="hero-3d-canvas">
      <Canvas
        camera={{ position: [0, 0, 5.5], fov: 45 }}
        dpr={[1, 1.8]}
        gl={{ antialias: true, alpha: true }}
      >
        <Float speed={1.3} rotationIntensity={0.4} floatIntensity={0.6}>
          <CoreOrb />
        </Float>
        <Particles />
        <OrbitControls
          enableZoom={false}
          enablePan={false}
          rotateSpeed={0.4}
          autoRotate={false}
        />
      </Canvas>
    </div>
  );
}
'''

# =====================================================
# pages/Dashboard.jsx — hero now uses Hero3D + tilt cards
# =====================================================
FILES["pages/Dashboard.jsx"] = '''
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { createCompany, listCompanies } from "../api/client";
import Hero3D from "../components/Hero3D";
import {
  IconBuilding,
  IconPlus,
  IconSparkles,
  IconTrending,
  IconShield,
} from "../components/Icons";
import { useTilt } from "../hooks/useTilt";

function CompanyCard({ company }) {
  const { ref, style, onMouseMove, onMouseLeave } = useTilt({ max: 6, scale: 1.03 });

  return (
    <div
      ref={ref}
      className="company-card"
      style={style}
      onMouseMove={onMouseMove}
      onMouseLeave={onMouseLeave}
    >
      <div className="company-card-top">
        <div className="company-avatar">
          {company.name.slice(0, 2).toUpperCase()}
        </div>
        <div className="company-id">ID #{company.id}</div>
      </div>
      <h3 className="company-name">{company.name}</h3>
      <div className="company-meta">
        <span className="chip">{company.industry}</span>
        <span className="chip">{company.currency}</span>
      </div>
      <div className="company-actions">
        <Link className="btn" to={`/upload?company=${company.id}`}>
          Upload Data
        </Link>
        <Link className="btn btn-ghost-dark" to="/analysis">
          Analyze
        </Link>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [companies, setCompanies] = useState([]);
  const [form, setForm] = useState({ name: "", industry: "General", currency: "USD" });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const load = async () => {
    const { data } = await listCompanies();
    setCompanies(data);
  };

  useEffect(() => {
    load();
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    if (!form.name.trim()) return;
    setLoading(true);
    setMessage("");
    try {
      await createCompany(form);
      setForm({ name: "", industry: "General", currency: "USD" });
      setMessage("Company added successfully");
      await load();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to add company");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* ---------- 3D Hero ---------- */}
      <div className="hero-3d">
        <div className="hero-3d-content">
          <div className="hero-badge">
            <IconSparkles size={14} />
            AI-Powered Financial Intelligence
          </div>
          <h1 className="hero-title">Your Companies</h1>
          <p className="hero-subtitle">
            Analyze financial statements, forecast cash flow, and detect anomalies —
            all in one intelligent workspace.
          </p>
        </div>
        <div className="hero-3d-scene">
          <Hero3D />
        </div>
      </div>

      {/* ---------- Stat strip ---------- */}
      <div className="stats-strip">
        <div className="stat-tile">
          <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#4f6ef7,#6366f1)" }}>
            <IconBuilding size={20} />
          </div>
          <div>
            <div className="stat-tile-label">Companies</div>
            <div className="stat-tile-value">{companies.length}</div>
          </div>
        </div>
        <div className="stat-tile">
          <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#8b5cf6,#ec4899)" }}>
            <IconTrending size={20} />
          </div>
          <div>
            <div className="stat-tile-label">Forecasting Models</div>
            <div className="stat-tile-value">Ready</div>
          </div>
        </div>
        <div className="stat-tile">
          <div className="stat-tile-icon" style={{ background: "linear-gradient(135deg,#10b981,#059669)" }}>
            <IconShield size={20} />
          </div>
          <div>
            <div className="stat-tile-label">Explainable AI</div>
            <div className="stat-tile-value">Active</div>
          </div>
        </div>
      </div>

      {/* ---------- Add Company ---------- */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Add a Company</h3>
            <p className="card-subtitle">Set up a new workspace for financial analysis</p>
          </div>
        </div>
        <form onSubmit={submit} className="grid grid-3" style={{ alignItems: "end" }}>
          <div>
            <label>Company Name</label>
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="e.g. Acme Corp"
              required
            />
          </div>
          <div>
            <label>Industry</label>
            <input
              value={form.industry}
              onChange={(e) => setForm({ ...form, industry: e.target.value })}
            />
          </div>
          <div>
            <label>Currency</label>
            <input
              value={form.currency}
              onChange={(e) => setForm({ ...form, currency: e.target.value })}
            />
          </div>
          <button type="submit" disabled={loading}>
            <IconPlus size={16} />
            {loading ? "Adding…" : "Add Company"}
          </button>
        </form>
        {message && <div className="success" style={{ marginTop: 14 }}>{message}</div>}
      </div>

      {/* ---------- Company Grid ---------- */}
      <div className="section-heading">
        <h3>Your Workspaces</h3>
        <span className="muted" style={{ fontSize: 13 }}>
          {companies.length} {companies.length === 1 ? "company" : "companies"}
        </span>
      </div>

      {companies.length === 0 ? (
        <div className="card empty-state">
          <IconBuilding size={64} />
          <h3>No companies yet</h3>
          <p className="muted">Add your first company above to start analyzing financial data.</p>
        </div>
      ) : (
        <div className="grid grid-3">
          {companies.map((c) => (
            <CompanyCard key={c.id} company={c} />
          ))}
        </div>
      )}
    </div>
  );
}
'''

# =====================================================
# components/RatioCard.jsx — 3D tilt
# =====================================================
FILES["components/RatioCard.jsx"] = '''
import { useTilt } from "../hooks/useTilt";

export default function RatioCard({ label, value, suffix = "" }) {
  const display = typeof value === "number" ? value.toFixed(4) : value ?? "—";

  let trend = "neutral";
  if (typeof value === "number") {
    if (label.toLowerCase().includes("debt")) {
      trend = value < 0.5 ? "good" : value < 0.7 ? "warn" : "bad";
    } else {
      trend = value > 0 ? "good" : "bad";
    }
  }

  const { ref, style, onMouseMove, onMouseLeave } = useTilt({ max: 10, scale: 1.05 });

  return (
    <div
      ref={ref}
      className="ratio-card"
      style={style}
      onMouseMove={onMouseMove}
      onMouseLeave={onMouseLeave}
    >
      <div className="ratio-label">{label}</div>
      <div className={`ratio-value ratio-${trend}`}>
        {display}
        {suffix}
      </div>
      <div className="ratio-bar">
        <div className={`ratio-bar-fill ratio-fill-${trend}`} />
      </div>
    </div>
  );
}
'''

# =====================================================
# Append 3D CSS
# =====================================================
CSS_3D = '''

/* =====================================================
   3D EXPERIENCE
   ===================================================== */

/* ---------- 3D Hero (with canvas) ---------- */
.hero-3d {
  position: relative;
  padding: 40px 36px;
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at 15% 80%, rgba(99, 102, 241, 0.35), transparent 55%),
    radial-gradient(circle at 85% 20%, rgba(139, 92, 246, 0.3), transparent 55%),
    linear-gradient(135deg, rgba(20, 25, 50, 0.9), rgba(10, 14, 30, 0.95));
  border: 1px solid rgba(165, 180, 252, 0.14);
  margin-bottom: 24px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    0 24px 60px rgba(0, 0, 0, 0.45),
    0 0 100px rgba(99, 102, 241, 0.08);
  display: grid;
  grid-template-columns: minmax(0, 1fr) 380px;
  gap: 24px;
  align-items: center;
  min-height: 340px;
}

.hero-3d-content { position: relative; z-index: 2; max-width: 560px; }

.hero-3d-scene {
  position: relative;
  width: 100%;
  height: 340px;
  z-index: 1;
}

.hero-3d-canvas {
  width: 100%;
  height: 100%;
  cursor: grab;
}

.hero-3d-canvas:active { cursor: grabbing; }

/* ---------- 3D page entrance ---------- */
@keyframes pageEnter3D {
  from {
    opacity: 0;
    transform: perspective(1200px) rotateX(6deg) translateY(20px);
  }
  to {
    opacity: 1;
    transform: perspective(1200px) rotateX(0deg) translateY(0);
  }
}

.content {
  animation: pageEnter3D 480ms cubic-bezier(0.22, 1, 0.36, 1);
}

/* ---------- Cards: 3D depth (preserve-3d) ---------- */
.card,
.company-card,
.ratio-card,
.stat-tile,
.score-card {
  transform-style: preserve-3d;
  will-change: transform;
  transition:
    transform 220ms cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 220ms cubic-bezier(0.4, 0, 0.2, 1),
    border-color 220ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Deeper layered shadows create floating sensation */
.card {
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.055),
    0 1px 2px rgba(0, 0, 0, 0.3),
    0 4px 8px rgba(0, 0, 0, 0.25),
    0 12px 32px rgba(0, 0, 0, 0.28);
}

.card:hover {
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.09),
    0 2px 4px rgba(0, 0, 0, 0.35),
    0 8px 16px rgba(0, 0, 0, 0.3),
    0 24px 56px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(99, 102, 241, 0.12);
}

/* Subtle 3D text lift on titles */
.card-title,
.page-title,
.hero-title,
.company-name,
.ratio-label {
  transform: translateZ(8px);
  transform-style: preserve-3d;
}

.ratio-value,
.stat-tile-value {
  transform: translateZ(16px);
  transform-style: preserve-3d;
}

/* Company card gets a thicker top light for extra 3D depth */
.company-card::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: var(--radius-lg);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.08) 0%,
    transparent 30%
  );
  pointer-events: none;
  opacity: 0;
  transition: opacity 220ms ease;
}

.company-card:hover::after { opacity: 1; }

/* Ratio card shine stripe */
.ratio-card {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.055) 0%,
    rgba(255, 255, 255, 0.02) 100%
  );
}

/* Score card gets 3D edge highlights */
.score-card {
  transform-style: preserve-3d;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    inset 0 -1px 0 rgba(0, 0, 0, 0.35),
    0 2px 4px rgba(0, 0, 0, 0.3),
    0 16px 40px rgba(0, 0, 0, 0.4),
    0 0 80px rgba(99, 102, 241, 0.1);
}

/* ---------- Sidebar 3D depth ---------- */
.sidebar {
  box-shadow:
    inset -1px 0 0 rgba(255, 255, 255, 0.04),
    4px 0 24px rgba(0, 0, 0, 0.4);
}

/* ---------- Topbar elevation ---------- */
.topbar {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
}

/* ---------- Stat tiles: hover lift with 3D ---------- */
.stat-tile {
  transition:
    transform 220ms cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 220ms cubic-bezier(0.4, 0, 0.2, 1),
    border-color 220ms cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-tile:hover {
  transform: perspective(900px) translateY(-4px) translateZ(20px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 4px 8px rgba(0, 0, 0, 0.3),
    0 16px 32px rgba(0, 0, 0, 0.4),
    0 0 40px rgba(99, 102, 241, 0.15);
}

/* ---------- Responsive ---------- */
@media (max-width: 1024px) {
  .hero-3d {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .hero-3d-scene { height: 300px; }
  .hero-3d-content { max-width: 100%; }
}

@media (max-width: 768px) {
  .hero-3d { padding: 28px 22px; }
  .hero-3d-scene { height: 240px; }
}
'''

path_css = ROOT / "index.css"
existing = path_css.read_text(encoding="utf-8")

marker = "/* =====================================================\n   3D EXPERIENCE"
if marker in existing:
    existing = existing.split(marker)[0].rstrip() + "\n"

path_css.write_text(existing + CSS_3D, encoding="utf-8")
print("  updated  src/index.css (3D section)")

# ---------- Write files ----------
for rel, content in FILES.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.lstrip("\n"), encoding="utf-8")
    print(f"  updated  src/{rel}")

print("\nDone. 3D experience installed.")