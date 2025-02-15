import React, {useContext, useEffect, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "./AuthContext";

function SignUpPage() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [userName, setUserName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepPassword] = useState('');

    if (!authContext) {
        return <p>404</p>;
    }
    const { login } = authContext;

    function isValidEmail(email) {
        const emailRegex = /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        return emailRegex.test(email);
    }

    function isValidUserName(userName) {
        const userNameRegex = /^[^ @!#$%^&*()<>?/\\|}{~:;,+=]+$/;
        return userNameRegex.test(userName);
    }

    function isValidPassword(password) {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$/;
        return passwordRegex.test(password);
    }

    async function handleSubmit(e) {
        e.preventDefault();

        if (!isValidUserName(userName)){
            console.log("Incorrect username form!");
            return;
        }

        if (!isValidEmail(email)){
            console.log("Incorrect email form!");
            return;
        }

        if (password !== repeatPassword) {
            console.log("Passwords do not match!");
            return;
        }

        if (!isValidPassword(password)){
            console.log("Incorrect password form!");
            return;
        }


        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.login.signUp}`,
                {
                    email: email,
                    username: userName,
                    password_hash: password
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            console.log("Successful Registration:", response.data);

            login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
            navigate('/')
        } catch (error) {
            console.error("Registration Error:", error);
        }
    }

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>Sign Up</h2>
                <p>
                Nickname: <input value={userName} onChange={e => setUserName(e.target.value)} />
                </p>
                <p>
                Email: <input value={email} onChange={e => setEmail(e.target.value)} />
                </p>
                <p>
                Password: <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </p>
                <p>
                Repeat password: <input type="password" value={repeatPassword} onChange={e => setRepPassword(e.target.value)} />
                </p>
                <button className="filled text" type="submit">Sign up</button>
            </form>
            <div className="redirect">
                <p>Already have an account? <Link to={"/sign-in"}>Log in</Link></p>
            </div>
        </section>
    );
}

export default SignUpPage;