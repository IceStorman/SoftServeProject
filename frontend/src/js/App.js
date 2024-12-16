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

import Header from "../components/header";
import Footer from "../components/footer";

import SignUpPage from "../pages/signUpPage";
import SignInPage from "../pages/signInPage";
import MainPage from "../pages/mainPage";
import ForgotPasswordPage from "../pages/forgotPasswordPage";
import SportPage from "../pages/sportPage";
import LeaguePage from "../pages/leaguePage";

function App(){

    return (
        <>

            <Router
                future={{
                v7_startTransition: true,
                v7_relativeSplatPath: true,
                }}
            >

                {<Header />}

                <Routes>

                    <Route exact path="/" element={<MainPage />} />

                    <Route path="/sign-in" element={<SignInPage />} />

                    <Route path="/sign-up" element={<SignUpPage />} />

                    <Route path="/reset-password" element={<ForgotPasswordPage />} />

                    <Route path="/sport/:sportName" element={<SportPage />} />

                    <Route path="/league/:leagueName" element={<LeaguePage />} />

                    <Route path="*" element={<Navigate to="/" />} />

                </Routes>

                {<Footer />}

            </Router>

        </>
    );
}

export default App;