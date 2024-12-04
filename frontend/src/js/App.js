import {
    useEffect,
    useState
} from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Navigate,
    Link
} from "react-router-dom";
import axios from "axios";

import header from "../components/header";
import footer from "../components/footer";

// import Home component
import homePage from "../pages/mainPage";
import SignUpPage from "../pages/signUpPage";
import SignInPage from "../pages/signInPage";
import MainPage from "../pages/mainPage";
import ForgotPasswordPage from "../pages/forgotPasswordPage";

function App(){

    return (
        <>

            <Router
                future={{
                v7_startTransition: true,
                v7_relativeSplatPath: true,
                }}
            >

                {header()}

                <Routes>

                    <Route exact path="/" element={<MainPage />} />

                    <Route path="/sign-in" element={<SignInPage />} />

                    <Route path="/sign-up" element={<SignUpPage />} />

                    <Route path="/reset-password" element={<ForgotPasswordPage />} />

                    <Route path="*" element={<Navigate to="/" />} />

                </Routes>

                {footer()}

            </Router>

        </>
    );
}

export default App;