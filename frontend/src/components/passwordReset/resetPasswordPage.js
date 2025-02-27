import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import useTranslations from "../../translationsContext";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";

function ResetPasswordPage() {
    const { token } = useParams();
    const navigate = useNavigate();
    const { t } = useTranslations();

    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        if (newPassword !== confirmPassword) {
            setError(t("passwords_do_not_match"));
            return;
        }

        try {
            const response = await fetch(`${apiEndpoints.url}${apiEndpoints.user.resetPassword}/${token}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ token, new_password: newPassword }),
            });

            if (!response.ok) {
                toast.error("Failed to reset password")
            }

            toast.success("You successfully reset password")
            navigate("/sign-in");
        } catch (err) {
            toast.error(t("error_resetting_password"))
        }
    };

    return (
        <section className="registration">
            <form onSubmit={handleSubmit}>
                <h2>{t("set_new_password")}</h2>

                <p>
                    {t("new_password")} <input type="password" value={newPassword}
                                               onChange={e => setNewPassword(e.target.value)}/>
                </p>
                <p>
                    {t("confirm_new_password")} <input type="password" value={confirmPassword}
                                                       onChange={e => setConfirmPassword(e.target.value)}/>
                </p>
                {error && <p className="error">{error}</p>}
                <button className="filled text" type="submit">{t("confirm")}</button>
            </form>
        </section>
    );
}

export default ResetPasswordPage;
