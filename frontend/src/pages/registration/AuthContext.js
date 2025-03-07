import { createContext, useState } from "react";
import Cookies from "js-cookie";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        const storedUser = Cookies.get("user");
        return storedUser ? JSON.parse(storedUser) : null;
    });

    const login = (userData) => {
        Cookies.set("user", JSON.stringify(userData), { expires: 30 });
        setUser(userData);
    };

    const logout = () => {
        Cookies.remove("user");
        setUser(null);
    };

    function isValidEmail(email) {
        const emailRegex = /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        return emailRegex.test(email);
    }

    function isValidUserName(userName) {
        const userNameRegex = /^[^ @!#$%^&*()<>?/\\|}{~:;,+=]+$/;
        return userNameRegex.test(userName);
    }

    function isValidPassword(password) {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$/;
        return passwordRegex.test(password);
    }


    return (
        <AuthContext.Provider value={{ user, login, logout, isValidEmail, isValidUserName, isValidPassword }}>
            {children}
        </AuthContext.Provider>
    );
};
