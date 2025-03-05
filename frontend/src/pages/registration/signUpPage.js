import React, {useContext, useEffect, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "./AuthContext";
import AuthBtn from "../../components/containers/authBtn";
import globalVariables from "../../globalVariables";
import useTranslations from "../../translationsContext";


function SignUpPage() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [userName, setUserName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepPassword] = useState('');
    const { t } = useTranslations();

    const { login, isValidEmail, isValidUserName, isValidPassword } = authContext;

    async function handleSubmit(e) {
        e.preventDefault();

        if (!isValidUserName(userName)){
            toast.error(globalVariables.authMessages.UsernameError);
            return;
        }

        if (!isValidEmail(email)){
            toast.error("Incorrect email form");
            return;
        }

        if (password !== repeatPassword) {
            toast.error("Passwords do not match");
            return;
        }

        if (!isValidPassword(password)){
            toast.error(globalVariables.authMessages.passwordMessage);
            return;
        }


        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.user.signUp}`,
                {
                    email: email,
                    username: userName,
                    password: password
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            login({ email: response?.data?.user?.email, username: response?.data?.user?.username, id: response?.data?.user?.id });
            toast.success(globalVariables.authMessages.successLogIn);
            navigate('/')
        } catch (error) {
            const errorStatus = error?.response?.status
            const errorMessage = error?.response?.data?.error;
            toast.error(
                `Registration Error 
                ${errorStatus ? errorStatus : ''} 
                ${errorMessage ? errorMessage : ''}`);
        }
    }

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>{t("sign_in")}</h2>
                <p>
                    {t("nickname")}
                    <input
                        value={userName}
                        onChange={e => setUserName(e.target.value)}
                    />
                </p>
                <p>
                    {t("email")}:
                    <input
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        onFocus={ () => toast.info(globalVariables.authMessages.EmailMessage) }
                    />
                </p>
                <p>
                    {t("password")}
                    <input
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        onFocus={ () => toast.info(globalVariables.authMessages.passwordMessage) }
                    />
                </p>
                <p>
                    {t("repeat_password")}
                    <input
                        type="password"
                        value={repeatPassword}
                        onChange={e => setRepPassword(e.target.value)}
                    />
                </p>
                <button className="filled text" type="submit">{t("sign_in")}</button>
            </form>

            <div className="redirect">
                <p className={"space"}> {t("have_account")} <Link to={"/sign-in"}>{t("log_in")}</Link></p>
                <AuthBtn />
            </div>
        </section>
    );
}

export default SignUpPage;