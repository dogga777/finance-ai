import { createContext, useContext, useEffect, useState } from "react";

import { getMe, login as apiLogin, register as apiRegister } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadUser = async () => {
    const token = localStorage.getItem("finsight_token");
    if (!token) {
      setLoading(false);
      return;
    }
    try {
      const { data } = await getMe();
      setUser(data);
    } catch {
      localStorage.removeItem("finsight_token");
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  const login = async (payload) => {
    const { data } = await apiLogin(payload);
    localStorage.setItem("finsight_token", data.access_token);
    await loadUser();
  };

  const register = async (payload) => {
    const { data } = await apiRegister(payload);
    localStorage.setItem("finsight_token", data.access_token);
    await loadUser();
  };

  const logout = () => {
    localStorage.removeItem("finsight_token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
