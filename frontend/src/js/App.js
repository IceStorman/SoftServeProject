import React, {useState, useEffect, useContext} from "react";
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
import { toast } from "sonner";
import axios from 'axios';

import apiEndpoints from "../apiEndpoints";
import NavBar from "../components/basic/nav";
import InsideNewsPage from "../pages/news/insideNewsPage";
import AboutUsPage from "../pages/misc/aboutAs";
import GoogleAuthCallback from "../pages/registration/googleCallBack";

function App() {

    return (
        <>
            <Toaster
                position="bottom-right"
                richColors
                expand={true}
                duration={5000}
                visibleToasts={3}
                closeButton
            />

            <Router
                future={{
                    v7_startTransition: true,
                    v7_relativeSplatPath: true,
                }}>

                <Header />
                <NavBar />

                <Routes>
                    <Route path="/" element={<MainPage />} />

                    <Route path="/sign-in" element={<SignInPage />} />

                    <Route path="/sign-up" element={<SignUpPage />} />

                    <Route path="/sign-in/google" element={<GoogleAuthCallback />} />

                    <Route path="/sign-in/reset-password" element={<ForgotPasswordPage />} />

                    <Route path="/sport" element={<SportPage />} />

                    <Route path="/sport/:sportName" element={<LeaguePage />} />

                    <Route path="/sport/:sportName/league/:leagueName" element={<TeamPage />} />

                    <Route path="/stream" element={<GamesPage />} />

                    <Route path="/stream/:gameId" element={<InsideStreamPage />} />

                    <Route path="/news/:articleId" element={<InsideNewsPage />} />

                    <Route path="/not-existing" element={<NotExistingPage />} />

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