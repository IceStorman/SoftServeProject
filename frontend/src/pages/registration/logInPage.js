import React, { useState } from "react";
import { Link } from "react-router-dom";
import useTranslations from "../../translationsContext";


function SignUpPage() {
    function handleSubmit(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        fetch('/some-api', { method: form.method, body: formData });

        const formJson = Object.fromEntries(formData.entries());
        console.log(formJson);
    }

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { t } = useTranslations();

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>{t("log_in")}</h2>
                <p>
                    {t("email")}: <input value={email} onChange={e => setEmail(e.target.value)} />
                </p>
                <p>
                    {t("password")} <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </p>
                <button className='filled text' type="submit">{t("log_in")}</button>
            </form>
            <div className="reset-passwrd">
                <Link to={"/sign-in/reset-password"}>{t("forget_password")}</Link>
            </div>
            <div className="redirect">
                <p> {t("no_account")} <Link to={"/sign-up"}>{t("create")}</Link></p>
            </div>
        </section>
    );
}

export default SignUpPage;