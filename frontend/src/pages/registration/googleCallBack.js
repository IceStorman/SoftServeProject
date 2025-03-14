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

    const {user} = useContext(AuthContext);

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get("code");

        if (code) {
            axios.post(`${apiEndpoints.url}${apiEndpoints.user.login}?code=${code}`,
                {
                    auth_provider: globalVariables.authStrategies.googleStrategy
                },)
                .then(response => {
                    login({ email: response?.data?.user?.email, username: response?.data?.user?.username, id: response?.data?.user?.id });
                    toast.success(globalVariables.authMessages.successLogIn);

                    user?.showPref === true ? navigate('/user/preferences') : navigate('/'); //waiting for Taras PR for this to work properly
                })
                .catch(error => {
                    const errorStatus = error?.response?.status
                    const errorMessage = error?.response?.data?.error;
                    toast.error(
                            `Google Authentication Error
                        ${errorStatus ? errorStatus : ''} 
                        ${errorMessage ? errorMessage : ''}`
                    );
                });
        }
    }, []);
    
    const { login } = authContext;

    return <></>;
}

export default GoogleAuthCallback;
