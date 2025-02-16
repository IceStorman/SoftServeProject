import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { RiArrowLeftWideLine } from "react-icons/ri";
import useTranslations from "../../translationsContext";

function ForgotPasswordPage() {

const [email, setEmail] = useState('');
const navigate = useNavigate();
const { t } = useTranslations();

    return (
        <section className="registration ">
            <form>
                <div className="title">
                    <button className='filled arrow' onClick={() => navigate(-1)}><RiArrowLeftWideLine /></button>
                    <h2>{t("password_reset")}</h2>
                </div>

                <p>
                    {t("email")}: <input value={email} onChange={e => setEmail(e.target.value)} />
                </p>
                <button className='filled text'>{t("continue")}</button>
            </form>
        </section>
    );
}

export default ForgotPasswordPage;