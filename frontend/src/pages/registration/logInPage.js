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

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    return (
        <section className="registration">
            <form method="post" onSubmit={handleSubmit}>
                <h2>Log In</h2>
                <p>
                Email: <input value={email} onChange={e => setEmail(e.target.value)} />
                </p>
                <p>
                Password: <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </p>
                <button className='filled text' type="submit">log in</button>
            </form>
            <div className="reset-passwrd">
                <Link to={"/sign-in/reset-password"}>Forget password?</Link>
            </div>
            <div className="redirect">
                <p>Do not have an account? <Link to={"/sign-up"}>Create</Link></p>
            </div>
        </section>
    );
}

export default SignUpPage;