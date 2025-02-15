import React, {useContext, useState} from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import { AuthContext } from "./AuthContext";
import globalVariables from "../../globalVariables";
import GoogleButton from 'react-google-button'


function SignUpPage() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [emailOrUserName, setEmailOrUserName] = useState('');
    const [password, setPassword] = useState('');

    const { login } = authContext;

    function isValidPassword(password) {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$/;
        return passwordRegex.test(password);
    }

    async function handleSubmit(e) {
        e.preventDefault();

        if (!isValidPassword(password)) {
            console.log("Incorrect password form!");
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

            console.log("Successful auth:", response.data);
            login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
            navigate('/');
        } catch (error) {
            console.error("Auth Error:", error);
        }
    }

    function handleGoogleLogin() {
        const clientId = globalVariables.googleAuth.clientId;
        const redirectUri = globalVariables.googleAuth.redirectUri;
        const scope = globalVariables.googleAuth.scope;
        const responseType = globalVariables.googleAuth.responseType;

        const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}`;
        window.location.href = authUrl;
    }

    if (!authContext) {
        return <p>404</p>;
    }

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>Log In</h2>
                <p>
                    Email: <input value={emailOrUserName} onChange={e => setEmailOrUserName(e.target.value)} />
                </p>
                <p>
                    Password: <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </p>
                <button className='filled text' type="submit">Log in</button>
            </form>
            <div className="reset-passwrd">
                <Link to={"/sign-in/reset-password"}>Forget password?</Link>
            </div>
            <div className="redirect">
                <p>Do not have an account? <Link to={"/sign-up"}>Create</Link></p>
                {/*<GoogleButton*/}
                {/*    onClick={() => console.log("Google button clicked")}*/}
                {/*/>*/}
                <button className='google-login' onClick={handleGoogleLogin}>Log in with Google</button>
            </div>
        </section>
    );
}

export default SignUpPage;
