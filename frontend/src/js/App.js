import React from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Navigate
} from "react-router-dom";
import {Toaster} from "sonner";

import Header from "../components/header";
import Footer from "../components/footer";

import SignUpPage from "../pages/signUpPage";
import SignInPage from "../pages/signInPage";
import MainPage from "../pages/mainPage";
import ForgotPasswordPage from "../pages/forgotPasswordPage";
import SportPage from "../pages/sportPage";
import LeaguePage from "../pages/leaguePage";
import StreamPage from "../pages/streamPage";
import NewsPage from "../pages/newsPage";
import NotExistingPage from "../pages/notExistingPage";
import ScrollToTop from "../components/scrollToTop";

function App(){

    return (
        <>

            <Router
                future={{
                v7_startTransition: true,
                v7_relativeSplatPath: true,
                }}
            >
                <ScrollToTop />

                <Toaster  position="top-center" expand={true} richColors  />

                {<Header />}

                <Routes>

                    <Route exact path="/" element={<MainPage />} />

                    <Route path="/sign-in" element={<SignInPage />} />

                    <Route path="/sign-up" element={<SignUpPage />} />

                    <Route path="/reset-password" element={<ForgotPasswordPage />} />

                    <Route path="/sport/:sportName" element={<SportPage />} />

                    <Route path="/sport/:sportName/league/:leagueName" element={<LeaguePage />} />

                    <Route path="/sport/:sportName/news/:id" element={<NewsPage />} />

                    <Route path="/stream" element={<StreamPage />} />

                    <Route path="/news/:id" element={<NewsPage />} />


                    <Route path="/not-existing" element={<NotExistingPage />} />

                    <Route path="*" element={<Navigate to="/not-existing" replace />} />

                </Routes>

                {<Footer />}

            </Router>

        </>
    );
}

export default App;