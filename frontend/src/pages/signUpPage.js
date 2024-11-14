import React from "react";
import {Link} from "react-router-dom";

function SignUpPage(){

    return(
        <>
            <section className={"signPage"}>

                <section className={"signContainer"}>

                    <div className={"signBox"}>

                        <h1>Реєстрація</h1>

                        <div className={"inputBox"}>
                            <input id={"name-input-sign-up"} className={"name-input"} type={"text"} placeholder={"Нік нейм"}/>
                            <input id={"email-input-sign-up"} className={"emailInput"} type={"email"} placeholder={"Email"}/>
                            <input id={"password-input-sign-up"} className={"passwordInput"} placeholder={"Пароль"} type={"password"}/>
                        </div>

                        <Link to={"/recover-password"}>Забули пароль?</Link>

                        <button id={"sign-up-btn"} className={"signBtn"}>Зареєструватись</button>

                    </div>

                </section>

                <div className={"signRedirect"}>

                    Уже є акаунт?
                    <Link to={"/sign-in"}>Ввійти</Link>

                </div>

            </section>
        </>
    );
}

export default SignUpPage;