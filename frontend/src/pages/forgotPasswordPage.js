import React from "react";
import {useState} from "react";


function ForgotPasswordPage(){

    return(
        <>
            <section className={"signPage"}>

                <section className={"signContainer"}>

                    <div className={"signBox"}>

                        <h1>Реєстрація</h1>

                        <div className={"inputBox"}>
                            <input id={"emailInputReset"} className={"emailInput"} type={"email"}
                                   placeholder={"Email"}/>
                            <h5 id={"emailError"} className={"signError"}></h5>
                            <input id={"codeInputReset"} className={"codeInput hidden"} type={"number"}
                                   placeholder={"Код з повідомлення"}/>
                            <h5 id={"codeError"} className={"signError"}></h5>
                            <input id={"passwordInputReset"} className={"passwordInput hidden"}
                                   placeholder={"Новий пароль"} type={"password"}/>
                            <input id={"passwordConfirmReset"} className={"passwordInput hidden"}
                                   placeholder={"Повторіть новий пароль"} type={"password"}/>
                            <h5 id={"passwordError"} className={"signError"}></h5>
                        </div>

                        <button id={"resetPassword"} className={"signBtn"} >Відновити акаунт</button>

                    </div>

                </section>

            </section>
        </>
    );
}

export default ForgotPasswordPage;