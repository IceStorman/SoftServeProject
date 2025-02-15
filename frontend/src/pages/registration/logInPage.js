import React, {useContext, useState} from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "./AuthContext";


function SignUpPage() {
    const authContext = useContext(AuthContext);
    const [emailOrNick, setEmailOrNick] = useState('');
    const [password, setPassword] = useState('');

    // Перевіряємо, чи контекст не null
    if (!authContext) {
        return <p>404</p>;
    }

    const { login } = authContext;
    async function handleSubmit(e) {
        e.preventDefault();


        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.login.login}`,
                {
                    email_or_username: emailOrNick,
                    password_hash: password,
                    auth_provider: "simple"
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            console.log("Успішна авторизація:", response.data);
            console.log(response.data.email);

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
                <h2>Log In</h2>
                <p>
                Email: <input value={emailOrNick} onChange={e => setEmailOrNick(e.target.value)} />
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