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
                            <input id={"nameInputSignUo"} className={"nameInput"} type={"text"} placeholder={"Нік нейм"}/>
                            <input id={"emailInputSignUp"} className={"emailInput"} type={"email"} placeholder={"Email"}/>
                            <input id={"passwordInputSignUp"} className={"passwordInput"} placeholder={"Пароль"} type={"password"}/>
                            <input id={"passwordConfirmSignUp"} className={"passwordInput"} placeholder={"Повторити пароль"} type={"password"}/>
                        </div>

                        <Link to={"/reset-password"}>Забули пароль?</Link>

                        <button id={"signUpBtn"} className={"signBtn"}>Зареєструватись</button>

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