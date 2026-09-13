import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await register(form);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-shell">
      <div className="auth-card">
        <h1>Create your FinSight AI account</h1>
        <p className="muted">Start analyzing financial statements in seconds</p>

        {error && <div className="error">{error}</div>}

        <form onSubmit={submit}>
          <div className="form-row">
            <label>Full Name</label>
            <input value={form.full_name} onChange={update("full_name")} required />
          </div>
          <div className="form-row">
            <label>Email</label>
            <input type="email" value={form.email} onChange={update("email")} required />
          </div>
          <div className="form-row">
            <label>Password (min 6 characters)</label>
            <input
              type="password"
              value={form.password}
              onChange={update("password")}
              required
              minLength={6}
            />
          </div>
          <button type="submit" disabled={loading} style={{ width: "100%" }}>
            {loading ? "Creating account…" : "Create Account"}
          </button>
        </form>

        <p style={{ marginTop: 18, fontSize: 14, textAlign: "center" }}>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
