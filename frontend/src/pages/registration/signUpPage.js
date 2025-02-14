import React, { useState } from "react";
import { Link } from "react-router-dom";

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

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>Sign Up</h2>
                <p>
                Nickname: <input value={nickname} onChange={e => setNickname(e.target.value)} />
                </p>
                <p>
                Email: <input value={email} onChange={e => setEmail(e.target.value)} />
                </p>
                <p>
                Password: <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </p>
                <p>
                Repeat password: <input type="password" value={repeatPassword} onChange={e => setRepPassword(e.target.value)} />
                </p>
                <button className="filled text" type="submit">Sign up</button>
            </form>
            <div className="redirect">
                <p>Already have an account? <Link to={"/sign-in"}>Log in</Link></p>
            </div>
        </section>
    );
}

export default SignUpPage;