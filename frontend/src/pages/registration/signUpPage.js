import React, {useContext, useEffect, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "./AuthContext";
import AuthBtn from "../../components/containers/authBtn";

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
            toast.error("Username can not contain such symbol or be empty!");
            return;
        }

        if (!isValidEmail(email)){
            toast.error("Incorrect email form!");
            return;
        }

        if (password !== repeatPassword) {
            toast.error("Passwords do not match!");
            return;
        }

        if (!isValidPassword(password)){
            toast.error("Password must contain at least 8 symbols, where: 1 uppercase letter, 1 lowercase letter and 1 number!");
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

            login({ email: response?.data?.user?.email, username: response?.data?.user?.username });
            toast.success(`You are successfully signed up!`);
            navigate('/')
        } catch (error) {
            const errorStatus = error?.response?.status
            const errorMessage = error?.response?.data?.error;
            toast.error(
                `Registration Error! 
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
                        onFocus={ () => toast.info('email: example@email.com') }
                    />
                </p>
                <p>
                Password:
                    <input
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        onFocus={ () => toast.info('Password must contain at least 8 symbols, where: 1 uppercase letter, 1 lowercase letter and 1 number!') }
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