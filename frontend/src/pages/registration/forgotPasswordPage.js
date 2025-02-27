import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { RiArrowLeftWideLine } from "react-icons/ri";
import useTranslations from "../../translationsContext";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";


function ForgotPasswordPage() {
    const [email, setEmail] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { t } = useTranslations();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

        if (!email || !emailRegex.test(email)) {
            toast.error("Please enter a valid email address");
            return;
        }

        try {
            const response = await fetch(`${apiEndpoints.url}${apiEndpoints.user.resetPasswordRequest}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email })
            });

            if (!response.ok) {
                toast.error("Failed to send reset request")
                return
            }

            toast.success("Success")
            navigate("/check-email");
        } catch (err) {
            toast.error("Error when sending email")
        }
    };

    return (
        <section className="registration">
            <form onSubmit={handleSubmit}>
                <div className="title">
                    <button className='filled arrow' type="button" onClick={() => navigate(-1)}>
                        <RiArrowLeftWideLine/>
                    </button>
                    <h2>{t("password_reset")}</h2>
                </div>
                <p>
                    {t("email")}:
                    <input
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        onBlur={() => !email.trim() && setError(t("required_field"))}
                        className={error ? "input-error" : ""}
                        placeholder={t("enter_email")}
                    />
                </p>
                {error && <p className="error">{error}</p>}
                <button className='filled text' type="submit">{t("continue")}</button>
            </form>
        </section>
    );
}

export default ForgotPasswordPage;
