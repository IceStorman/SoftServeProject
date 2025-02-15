import React, {useContext, useEffect, useState} from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {AuthContext} from "./AuthContext";
import globalVariables from "../../globalVariables";

function GoogleAuthCallback() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get("code");

        if (code) {
            axios.post(`${apiEndpoints.url}${apiEndpoints.login.login}?code=${code}`,
                {
                    auth_provider: globalVariables.authStrategies.googleStrategy
                },)
                .then(response => {
                    console.log("Successful auth:", response.data);
                    login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
                    navigate('/')
                })
                .catch(error => {
                    console.error("Google auth error:", error);
                });
        }
    }, []);

    const { login } = authContext;

    if (!authContext) {
        return <p>404</p>;
    }

    return <></>;
}

export default GoogleAuthCallback;
