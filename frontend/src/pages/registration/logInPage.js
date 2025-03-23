import React, {useContext, useState} from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import { AuthContext } from "./AuthContext";
import globalVariables from "../../globalVariables";
import AuthBtn from "../../components/containers/authBtn";
import useTranslations from "../../translationsContext";
import {toast} from "sonner";


function SignInPage() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [emailOrUserName, setEmailOrUserName] = useState('');
    const [password, setPassword] = useState('');
    const { t } = useTranslations();

    const { login, isValidEmail, isValidUserName, isValidPassword } = authContext;

    function isValidEmailOrUserName(emailOrUserName) {
        if (!emailOrUserName.trim())
            return false;

        if (emailOrUserName.includes('@')) {
            return isValidEmail(emailOrUserName);
        }

        return isValidUserName(emailOrUserName);
    }

    async function handleSubmit(e) {
        e.preventDefault();

        if (!isValidEmailOrUserName(emailOrUserName)) {
            toast.error(globalVariables.authMessages.UsernameOrEmailError);
            return;
        }

        if (!isValidPassword(password)) {
            toast.error(globalVariables.authMessages.passwordMessage);
            return;
        }

        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.user.login}`,
                {
                    email_or_username: emailOrUserName,
                    password: password,
                    auth_provider: globalVariables.authStrategies.simpleStrategy
                },
                {
                    withCredentials: true // Will make project great again
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            login();
            toast.success(globalVariables.authMessages.successLogIn);
            navigate('/');
        } catch (error) {
            const errorStatus = error?.response?.status
            const errorMessage = error?.response?.data?.error;
            toast.error(
                `Authentication Error 
                ${errorStatus ? errorStatus : ''} 
                ${errorMessage ? errorMessage : ''}`);
        }
    }

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>{t("log_in")}</h2>
                <p>
                    Email/Username:
                    <input
                        value={emailOrUserName}
                        onChange={e => setEmailOrUserName(e.target.value)}
                        onFocus={ () => toast.info(globalVariables.authMessages.EmailMessage)}
                    />
                </p>
                <p>
                    {t("password")}
                    <input
                        type="password"
                        value={password} onChange={e => setPassword(e.target.value)}
                        onFocus={ () => toast.info(globalVariables.authMessages.passwordMessage)}
                    />
                </p>
                <button className='filled text' type="submit">{t("log_in")}</button>
            </form>

            <div className="reset-passwrd">
                <Link to={"/sign-in/reset-password"}>{t("forget_password")}</Link>
            </div>

            <div className="redirect">
                <p className="space"> {t("no_account")} <Link to={"/sign-up"}>{t("create")}</Link></p>
                <AuthBtn />
            </div>

        </section>
    );
}

export default SignInPage;
