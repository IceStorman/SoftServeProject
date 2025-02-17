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

    const { login } = authContext;

    function isValidPassword(password) {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$/;
        return passwordRegex.test(password);
    }

    async function handleSubmit(e) {
        e.preventDefault();

        if (!emailOrUserName.trim()) {
            toast.error("Username or email can not be empty!");
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

            console.log("Successful auth:", response.data);
            login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
            toast.success(`You are successfully logged in!`);
            navigate('/');
        } catch (error) {
            toast.error(`Authentication error!\n ${error.response.status}`);
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
