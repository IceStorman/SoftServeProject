import React, {useContext, useEffect, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "./AuthContext";
import AuthBtn from "../../components/containers/authBtn";
import globalVariables from "../../globalVariables";

function SignUpPage() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [userName, setUserName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepPassword] = useState('');

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

            login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
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
                <h2>Sign Up</h2>
                <p>
                Username:
                    <input
                        value={userName}
                        onChange={e => setUserName(e.target.value)}
                    />
                </p>
                <p>
                Email:
                    <input
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        onFocus={ () => toast.info(globalVariables.authMessages.EmailMessage) }
                    />
                </p>
                <p>
                Password:
                    <input
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        onFocus={ () => toast.info(globalVariables.authMessages.passwordMessage) }
                    />
                </p>
                <p>
                Repeat password:
                    <input
                        type="password"
                        value={repeatPassword}
                        onChange={e => setRepPassword(e.target.value)}
                    />
                </p>
                <button className="filled text" type="submit">Sign up</button>
            </form>
            <div className="redirect">
                <p>Already have an account? <Link to={"/sign-in"}>Log in</Link></p>
                <AuthBtn />
            </div>
        </section>
    );
}

export default SignUpPage;