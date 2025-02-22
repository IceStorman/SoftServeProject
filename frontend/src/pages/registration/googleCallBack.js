import React, {useContext, useEffect, useState} from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {AuthContext} from "./AuthContext";
import globalVariables from "../../globalVariables";
import {toast} from "sonner";

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
                    login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
                    toast.success(`You are successfully logged in!`);
                    navigate('/')
                })
                .catch(error => {
                    toast.error(`Google Authentication Error!\n ${error?.response?.status} \n ${error?.response?.data?.error}`);
                });
        }
    }, []);
    
    const { login } = authContext;

    return <></>;
}

export default GoogleAuthCallback;
