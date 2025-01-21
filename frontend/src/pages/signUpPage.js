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

                            <div className={"inputBoxField"}>

                                <input
                                    id={"nameInputSignUo"}
                                    className={"nameInput"}
                                    type={"text"}
                                    placeholder={" "}
                                />
                                <label>Нік нейм</label>

                            </div>
                            <div className={"inputBoxField"}>

                                <input
                                    id={"emailInputSignUp"}
                                    className={"emailInput"}
                                    type={"email"}
                                    placeholder={" "}
                                />
                                <label>Email</label>

                            </div>
                            <div className={"inputBoxField"}>

                                <input
                                    id={"passwordInputSignUp"}
                                    className={"passwordInput"}
                                    type={"password"}
                                    placeholder={" "}
                                />
                                <label>Пароль</label>

                            </div>
                            <div className={"inputBoxField"}>

                                <input
                                    id={"passwordConfirmSignUp"}
                                    className={"passwordInput"}
                                    type={"password"}
                                    placeholder={" "}
                                />
                                <label>Повторити пароль</label>

                            </div>


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