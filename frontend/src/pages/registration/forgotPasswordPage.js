import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { RiArrowLeftWideLine } from "react-icons/ri";

function ForgotPasswordPage() {

const [email, setEmail] = useState('');
 const navigate = useNavigate();

    return (
        <section className="registration ">
            <form>
                <div className="title">
                    <button className='filled arrow' onClick={() => navigate(-1)}><RiArrowLeftWideLine /></button>
                    <h2>Password reset</h2>
                </div>

                <p>
                    Email: <input value={email} onChange={e => setEmail(e.target.value)} />
                </p>
                <button className='filled text'>Continue?</button>
            </form>
        </section>
    );
}

export default ForgotPasswordPage;