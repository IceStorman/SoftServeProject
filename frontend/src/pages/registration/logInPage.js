import React, {useContext, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "./AuthContext";
import authStrategies from "../../authStrategies";

function SignUpPage() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [emailOrUserName, setEmailOrUserName] = useState('');
    const [password, setPassword] = useState('');

    if (!authContext) {
        return <p>404</p>;
    }
    const { login } = authContext;

    function isValidPassword(password) {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$/;
        return passwordRegex.test(password);
    }


    async function handleSubmit(e) {
        e.preventDefault();

        if (!isValidPassword(password)){
            console.log("Incorrect password form!");
            return;
        }

        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.login.login}`,
                {
                    email_or_username: emailOrUserName,
                    password_hash: password,
                    auth_provider: authStrategies.simpleStrategy
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            console.log("Successful auth:", response.data);
            login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
            navigate('/')
        } catch (error) {
            console.error("Auth Error:", error);
        }
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
                <button className='filled text' type="submit">log in</button>
            </form>
            <div className="reset-passwrd">
                <Link to={"/sign-in/reset-password"}>Forget password?</Link>
            </div>
            <div className="redirect">
                <p>Do not have an account? <Link to={"/sign-up"}>Create</Link></p>
            </div>
        </section>
    );
}

export default SignUpPage;