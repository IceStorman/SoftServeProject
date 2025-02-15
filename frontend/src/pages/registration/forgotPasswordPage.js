import React, {useEffect, useState} from "react";
import { Link, useNavigate } from "react-router-dom";
import { RiArrowLeftWideLine } from "react-icons/ri";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";

function ForgotPasswordPage() {
    const [email, setEmail] = useState('');
    const navigate = useNavigate();


    function isValidEmail(email) {
        const emailRegex = /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        return emailRegex.test(email);
    }

    async function handleSubmit(e) {
        e.preventDefault(); // Щоб форма не оновлювала сторінку

        if (!isValidEmail(email)) {
            console.log("Incorrect email format!");
            return;
        }

        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.login.resetPasswordRequest}`,
                { email },
                { headers: { 'Content-Type': 'application/json' } }
            );

            console.log("Letter was sent:", response.data);
        } catch (error) {
            console.error("Reset Password Error:", error);
        }
    }

    return (
        <section className="registration">
            <form onSubmit={handleSubmit}>
                <div className="title">
                    <Link className="backButton filled arrow" to="/sign-in">
                        <RiArrowLeftWideLine />
                    </Link>
                    <h2>Password reset</h2>
                </div>

                <p>
                    Email: <input value={email} onChange={e => setEmail(e.target.value)} />
                </p>
                <button className="filled text" type="submit">Continue?</button>
            </form>
        </section>
    );
}

export default ForgotPasswordPage;