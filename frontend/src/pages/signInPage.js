import React from "react";
import {Link, Route, Router, Routes} from "react-router-dom";

function SignUpPage(){

    return(
        <>

            <section className={"signPage"}>

                <section className={"signContainer"}>

                    <div className={"signBox"}>

                        <h1>Вхід</h1>

                        <div className={"inputBox"}>
                            <input id={"emailInputSignIn"} className={"emailInput"} type={"email text"} placeholder={"Email / Нік нейм"}/>
                            <input id={"passwordInputSignIn"} className={"passwordInput"} placeholder={"Пароль"} type={"password"}/>
                            <input id={"passwordConfirmSignIn"} className={"passwordInput hidden"} placeholder={"Повторіть новий пароль"} type={"password"}/>
                        </div>

                        <Link to={"/recover-password"}>Забули пароль?</Link>

                        <button id={"sign-in-btn"} className={"signBtn"}>Ввійти</button>

                    </div>

                </section>

                <div className={"signRedirect"}>

                    Ще немає акаунта?
                    <Link to={"/sign-up"}>Створити</Link>

                </div>

            </section>

        </>
    );
}

export default SignUpPage;