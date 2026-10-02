import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('rescuai_token') || null);
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('rescuai_user')) || null);

  const login = (accessToken, userData = { role: 'RESPONDER', email: 'responder@rescuai.org' }) => {
    setToken(accessToken);
    setUser(userData);
    localStorage.setItem('rescuai_token', accessToken);
    localStorage.setItem('rescuai_user', JSON.stringify(userData));
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('rescuai_token');
    localStorage.removeItem('rescuai_user');
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        isAuthenticated: !!token,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
