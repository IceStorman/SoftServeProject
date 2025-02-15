import { createContext, useState, useEffect } from "react";
import Cookies from "js-cookie";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        const storedUser = Cookies.get("user");
        return storedUser ? JSON.parse(storedUser) : null;
    });

    const login = (userData) => {
        Cookies.set("user", JSON.stringify(userData), { expires: 7 });
        setUser(userData);
    };

    const logout = () => {
        Cookies.remove("user");
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
