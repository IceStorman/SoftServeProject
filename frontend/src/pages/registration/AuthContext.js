import {createContext, useEffect, useState} from "react";
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {wait} from "@testing-library/user-event/dist/utils";


export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const initializeUser = async () => {
            login()
        };

        initializeUser();
    }, []);

    const login = async () => {
        const token = await getRefresh();

        if (token) {
            const userData = decodeJwt(token);

            if (userData) {
                Cookies.set("user", JSON.stringify(userData), { expires: 1/24 });
                setUser(userData);
            }
        }
    };

    const decodeJwt = (token) => {
        try {
            return jwtDecode(token);
        } catch (error) {
            return null;
        }
    };

    const getRefresh = async () => {
        await wait(500);
        let token = Cookies.get("access_token_cookie");

        if (!token) {
            const refreshToken = Cookies.get("refresh_token_cookie");

            if (refreshToken) {
                try {
                    await axios.post(`${apiEndpoints.url}${apiEndpoints.user.refresh}`,
                        {},
                        { withCredentials: true }
                    );
                    token = Cookies.get("access_token_cookie");
                } catch (error) {
                    logout();
                    token = null
                }
            }
        }

        return token;
    }

    const logout = () => {
        Cookies.remove("user");
        Cookies.remove("access_token_cookie");
        Cookies.remove("refresh_token_cookie");
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
