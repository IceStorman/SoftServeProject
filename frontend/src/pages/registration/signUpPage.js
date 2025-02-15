import React, {useContext, useEffect, useState} from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "./AuthContext";

function SignUpPage() {
    const authContext = useContext(AuthContext);

    const [nickname, setNickname] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepPassword] = useState('');
    // Перевіряємо, чи контекст не null
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
                    username: nickname,
                    password_hash: password
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            console.log("Успішна реєстрація:", response.data);

            // Передаємо користувача у контекст (зберігаємо в кукі)
            login({ email: response?.data?.user?.email, username: response?.data?.user?.username });

            toast.success("Реєстрація успішна! Ви увійшли в акаунт.");
        } catch (error) {
            console.error("Помилка реєстрації:", error);
            toast.error("Не вдалося зареєструватися. Спробуйте ще раз.");
        }
    }

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>Sign Up</h2>
                <p>
                Nickname: <input value={nickname} onChange={e => setNickname(e.target.value)} />
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