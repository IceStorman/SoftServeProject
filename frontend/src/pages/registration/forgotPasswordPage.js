import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { RiArrowLeftWideLine } from "react-icons/ri";
import useTranslations from "../../translationsContext";
import apiEndpoints from "../../apiEndpoints";


function ForgotPasswordPage() {
    const [email, setEmail] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { t } = useTranslations();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const response = await fetch(`${apiEndpoints.url}${apiEndpoints.user.resetPasswordRequest}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email })
            });

            if (!response.ok) {
                throw new Error("Failed to send reset request");
            }

            navigate("/check-email");
        } catch (err) {
            setError(t("error_sending_email"));
        }
    };

    return (
        <section className="registration">
            <form onSubmit={handleSubmit}>
                <div className="title">
                    <button className='filled arrow' type="button" onClick={() => navigate(-1)}>
                        <RiArrowLeftWideLine />
                    </button>
                    <h2>{t("password_reset")}</h2>
                </div>
                <p>
                    {t("email")}: <input value={email} onChange={e => setEmail(e.target.value)} required />
                </p>
                {error && <p className="error">{error}</p>}
                <button className='filled text' type="submit">{t("continue")}</button>
            </form>
        </section>
    );
}

export default ForgotPasswordPage;
