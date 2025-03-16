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
                    login({ email: response?.data?.email, username: response?.data?.username, id: response?.data?.user_id });
                    toast.success(globalVariables.authMessages.successLogIn);

                    response?.data?.new_user === true ? navigate('/user/preferences') : navigate('/');
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
