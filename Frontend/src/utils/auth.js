import jwtDecode from "jwt-decode";

/**
 * Get JWT Token
 */
export const getToken = () => {
  return localStorage.getItem("token");
};

/**
 * Check Login Status
 */
export const isAuthenticated = () => {
  return !!getToken();
};

/**
 * Logout User
 */
export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("name");
  localStorage.removeItem("email");
  localStorage.removeItem("role");

  window.location.href = "/login";
};

/**
 * Get Logged-in User Role
 */
export const getRole = () => {
  return localStorage.getItem("role");
};

/**
 * Check Admin Access
 */
export const isAdmin = () => {
  return getRole() === "admin";
};

/**
 * Get User Details from JWT (Optional)
 */
export const getUser = () => {
  const token = getToken();

  if (!token) return null;

  try {
    return jwtDecode(token);
  } catch (error) {
    return null;
  }
};