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
    const [nickname, setNickname] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepPassword] = useState('');
    const { t } = useTranslations();

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>{t("sign_in")}</h2>
                <p>
                    {t("nickname")} <input value={nickname} onChange={e => setNickname(e.target.value)} />
                </p>
                <p>
                    {t("email")}: <input value={email} onChange={e => setEmail(e.target.value)} />
                </p>
                <p>
                    {t("password")} <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </p>
                <p>
                    {t("repeat_password")} <input type="password" value={repeatPassword} onChange={e => setRepPassword(e.target.value)} />
                </p>
                <button className="filled text" type="submit">{t("sign_in")}</button>
            </form>
            <div className="redirect">
                <p>{t("have_account")}<Link to={"/sign-in"}>{t("sign_in")}</Link></p>
            </div>
        </section>
    );
}

export default SignUpPage;