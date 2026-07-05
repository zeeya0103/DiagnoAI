import { createContext, useContext, useEffect, useState } from "react";
import axios from "../api/axios";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check Login
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {

    const token = localStorage.getItem("token");

    if (!token) {
      setLoading(false);
      return;
    }

    try {

      const res = await axios.get("/auth/me", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      setUser(res.data);

    } catch (error) {

      console.log(error);

      logout();

    }

    setLoading(false);

  };

  // Login
  const login = async (email, password) => {

    const res = await axios.post("/auth/login", {
      email,
      password
    });

    const token = res.data.access_token;

    localStorage.setItem("token", token);
    localStorage.setItem("role", res.data.role);
    localStorage.setItem("name", res.data.name);
    localStorage.setItem("email", res.data.email);

    setUser(res.data);

    return res.data;

  };

  // Register
  const register = async (data) => {

    const res = await axios.post("/auth/register", data);

    return res.data;

  };

  // Logout
  const logout = () => {

    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("name");
    localStorage.removeItem("email");

    setUser(null);

    window.location.href = "/login";

  };

  return (

    <AuthContext.Provider

      value={{

        user,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!user

      }}

    >

      {children}

    </AuthContext.Provider>

  );

};

export const useAuth = () => useContext(AuthContext);

export default AuthContext;