import React from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Navigate
} from "react-router-dom";
import { Toaster } from "sonner";

import Header from "../components/basic/header";
import Footer from "../components/basic/footer";

import SignUpPage from "../pages/registration/signUpPage";
import SignInPage from "../pages/registration/logInPage";
import MainPage from "../pages/mainPage";
import ForgotPasswordPage from "../pages/registration/forgotPasswordPage";
import SportPage from "../pages/sport items/sportPage";
import LeaguePage from "../pages/sport items/leaguePage";
import TeamPage from "../pages/sport items/teamPage";
import StreamsPage from "../pages/games/streamsPage";
import FAQpage from "../pages/misc/FAQ";
import NotExistingPage from "../pages/notExistingPage";
import InsideStreamPage from "../pages/games/insideStreamPage";
import NavBar from "../components/basic/nav";
import InsideNewsPage from "../pages/news/insideNewsPage";
import AboutUsPage from "../pages/misc/aboutAs";
import ResetPasswordPage from "../components/passwordReset/resetPasswordPage";
import CheckEmailPage from "../components/passwordReset/checkEmailPage";
import GoogleAuthCallback from "../pages/registration/googleCallBack";
import PreferencesPage from "../pages/registration/PreferencesPage";
import AccountPage from "../pages/registration/accountPage";
import globalVariables from "../globalVariables";

function App() {


    return (
        <>
            <Router
                future={{
                    v7_startTransition: true,
                    v7_relativeSplatPath: true,
                }}>

                <Toaster
                    position="bottom-right"
                    richColors
                    expand={true}
                    duration={5000}
                    visibleToasts={globalVariables.windowsSizes.find(ws => window.innerWidth <= ws.maxWidth).limit || 0}
                    closeButton
                />

                <Header />
                <NavBar />


                <Routes>
                    <Route path="/" element={<MainPage />} />

                    <Route path="/sign-in" element={<SignInPage />} />

                    <Route path="/sign-up" element={<SignUpPage />} />

                    <Route path="/user/preferences" element={<PreferencesPage />} />

                    <Route path="/user/account" element={<AccountPage />} />

                    <Route path="/sign-in/google" element={<GoogleAuthCallback />} />

                    <Route path="/sign-in/reset-password" element={<ForgotPasswordPage />} />

                    <Route path="/sign-in/reset-password/:token" element={<ResetPasswordPage />} />

                    <Route path="/check-email" element={<CheckEmailPage />} />

                    <Route path="/sport" element={<SportPage />} />

                    <Route path="/sport/:sportName" element={<LeaguePage />} />

                    <Route path="/sport/:sportName/league/:leagueName" element={<TeamPage />} />

                    <Route path="/stream" element={<StreamsPage />} />

                    <Route path="/stream/:streamId" element={<InsideStreamPage />} />

                    <Route path="/news/:articleId" element={<InsideNewsPage />} />

                    <Route path="/not-existing" element={<NotExistingPage />} />

                    <Route path="*" element={<Navigate to="/not-existing" replace />} />

                    <Route path="/FAQ" element={<FAQpage />} />

                    <Route path="/AboutUs" element={<AboutUsPage />} />

                    <Route path="*" element={<Navigate to="/not-existing" replace />} />
                </Routes>

                {<Footer />}

            </Router>
        </>
    );
}

export default App;