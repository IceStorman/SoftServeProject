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
import GamesPage from "../pages/games/gamesPage";
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
                    <Route path={globalVariables.routeLinks.defaultRoute} element={<MainPage />} />

                    <Route path={globalVariables.routeLinks.signInRoute} element={<SignInPage />} />

                    <Route path={globalVariables.routeLinks.signUpRoute} element={<SignUpPage />} />

                    <Route path={globalVariables.routeLinks.preferenceRoute} element={<PreferencesPage />} />

                    <Route path={globalVariables.routeLinks.accountRoute} element={<AccountPage />} />

                    <Route path={globalVariables.routeLinks.signInGoogleRoute} element={<GoogleAuthCallback />} />

                    <Route path={globalVariables.routeLinks.forgotPasswordRoute} element={<ForgotPasswordPage />} />

                    <Route path={globalVariables.routeLinks.resetPasswordTokenRoute} element={<ResetPasswordPage />} />

                    <Route path={globalVariables.routeLinks.checkEmailRoute} element={<CheckEmailPage />} />

                    <Route path={globalVariables.routeLinks.sportPageRoute} element={<SportPage />} />

                    <Route path={globalVariables.routeLinks.leaguePageRoute} element={<LeaguePage />} />

                    <Route path={globalVariables.routeLinks.teamPageRoute} element={<TeamPage />} />

                    <Route path={globalVariables.routeLinks.streamRoute} element={<GamesPage />} />

                    <Route path={globalVariables.routeLinks.streamPageRoute} element={<InsideStreamPage />} />

                    <Route path={globalVariables.routeLinks.newsPageRoute} element={<InsideNewsPage />} />

                    <Route path={globalVariables.routeLinks.nonExistingRoute} element={<NotExistingPage />} />

                    <Route path={globalVariables.routeLinks.FAQRoute} element={<FAQpage />} />

                    <Route path={globalVariables.routeLinks.aboutUsRoute} element={<AboutUsPage />} />

                    <Route path={globalVariables.routeLinks.nonExistingPath} element={<Navigate to={globalVariables.routeLinks.nonExistingRoute} replace />} />
                </Routes>

                {<Footer />}

            </Router>
        </>
    );
}

export default App;