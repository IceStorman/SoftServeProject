import React from "react";
import {Link} from "react-router-dom";

function SignUpPage(){

    return(
        <>
            <section className={"sign-page"}>

                <section className={"sign-container"}>

                    <div className={"sign-box"}>

                        <h1>Реєстрація</h1>

                        <div className={"input-box"}>
                            <input id={"name-input-sign-in"} className={"name-input"} type={"text"} placeholder={"Нік нейм"}/>
                            <input id={"email-input-sign-in"} className={"email-input"} type={"email"} placeholder={"Email"}/>
                            <input id={"password-input-sign-in"} className={"password-input"} placeholder={"Пароль"} type={"password"}/>
                            <input id={"password-confirm-sign-in"} className={"password-input"} placeholder={"Повторіть пароль"} type={"password"}/>
                        </div>

                        <Link to={""}>Забули пароль?</Link>

                        <button id={"sign-btn"}>Зареєструватись</button>

                    </div>

                </section>

                <div className={"sign-redirect"}>

                    Уже є акаунт?
                    <Link to={"/sign-in"}>Ввійти</Link>

                </div>

            </section>
        </>
    );
}

export default SignUpPage;