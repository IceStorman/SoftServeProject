import React, {useContext, useState} from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import { AuthContext } from "./AuthContext";
import globalVariables from "../../globalVariables";
import AuthBtn from "../../components/containers/authBtn";
import {toast} from "sonner";


function SignInPage() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [emailOrUserName, setEmailOrUserName] = useState('');
    const [password, setPassword] = useState('');

    const { login, isValidEmail, isValidUserName, isValidPassword } = authContext;

    function isValidEmailOrUserName(emailOrUserName) {
        if (!emailOrUserName.trim())
            return false;

        const isEmailRegex = /^[^@]$/
        if (isEmailRegex.test(emailOrUserName))
            return isValidEmail(emailOrUserName);

        return isValidUserName(emailOrUserName);
    }

    async function handleSubmit(e) {
        e.preventDefault();

        if (!isValidEmailOrUserName(emailOrUserName)) {
            toast.error("Username or email can not be empty or contain such symbols!");
            return;
        }

        if (!isValidPassword(password)) {
            toast.error("Password must contain at least 8 symbols, where: 1 uppercase letter, 1 lowercase letter and 1 number!");
            return;
        }

        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.login.login}`,
                {
                    email_or_username: emailOrUserName,
                    password_hash: password,
                    auth_provider: globalVariables.authStrategies.simpleStrategy
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
            toast.success(`You are successfully logged in!`);
            navigate('/');
        } catch (error) {
            const errorStatus = error?.response?.status
            const errorMessage = error?.response?.data?.error;
            toast.error(
                `Authentication Error! 
                ${errorStatus ? errorStatus : ''} 
                ${errorMessage ? errorMessage : ''}`);
        }
    }

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>Log In</h2>
                <p>
                    Email/Username:
                    <input
                        value={emailOrUserName}
                        onChange={e => setEmailOrUserName(e.target.value)}
                        onFocus={ () => toast.info('email: example@email.com') }
                    />
                </p>
                <p>
                    Password:
                    <input
                        type="password"
                        value={password} onChange={e => setPassword(e.target.value)}
                        onFocus={ () => toast.info('Password must contain at least 8 symbols, where: 1 uppercase letter, 1 lowercase letter and 1 number!') }
                    />
                </p>
                <button className='filled text' type="submit">Log in</button>
            </form>
            <div className="reset-passwrd">
                <Link to={"/sign-in/reset-password"}>Forget password?</Link>
            </div>
            <div className="redirect">
                <p>Do not have an account? <Link to={"/sign-up"}>Create</Link></p>
                <AuthBtn />
            </div>
        </section>
    );
}

export default SignInPage;
