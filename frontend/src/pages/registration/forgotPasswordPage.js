import React, {useContext, useState} from "react";
import { useNavigate } from "react-router-dom";
import { RiArrowLeftWideLine } from "react-icons/ri";
import useTranslations from "../../translationsContext";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "./AuthContext";
import globalVariables from "../../globalVariables";


function ForgotPasswordPage() {
    const authContext = useContext(AuthContext);
    const [email, setEmail] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { t } = useTranslations();
    const {isValidEmail} = authContext;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        if (!isValidEmail(email)){
            toast.error("Incorrect email form");
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
