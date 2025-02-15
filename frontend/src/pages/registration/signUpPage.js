import React, {useContext, useEffect, useState} from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "./AuthContext";

function SignUpPage() {
    const authContext = useContext(AuthContext);

    const [userName, setUserName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepPassword] = useState('');

    if (!authContext) {
        return <p>404</p>;
    }

    const { login } = authContext;

    async function handleSubmit(e) {
        e.preventDefault();

        if (password !== repeatPassword) {
            console.log("Паролі не співпадають!");
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

            console.log("Успішна реєстрація:", response.data);

            login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
        } catch (error) {
            console.error("Помилка реєстрації:", error);
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