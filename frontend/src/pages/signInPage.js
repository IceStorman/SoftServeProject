import React from "react";
import {Link, Route, Router, Routes} from "react-router-dom";

function SignUpPage(){

    return(
        <>

            <section className={"sign-page"}>

                <section className={"sign-container"}>

                    <div className={"sign-box"}>

                        <h1>Вхід</h1>

                        <div className={"input-box"}>
                            <input id={"email-input"} type={"email text"} placeholder={"Email / Нік нейм"}/>
                            <input id={"password-input"} placeholder={"Пароль"}/>
                        </div>

                        <Link to={""}>Забули пароль?</Link>

                        <button id={"sign-btn"}>Ввійти</button>

                    </div>

                </section>

                <div className={"sign-redirect"}>

                    Ще немає акаунта?
                    <Link to={"/sign-up"}>Створити</Link>

                </div>

            </section>

        </>
    );
}

export default SignUpPage;