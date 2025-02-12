import React, { useState, useEffect } from "react";
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

function App() {


    return (
        <>

            <Router
                future={{
                    v7_startTransition: true,
                    v7_relativeSplatPath: true,
                }}
            >



                <Header />
                <NavBar />

                <Routes>

                    <Route exact path="/" element={<MainPage />} />

                    <Route path="/sign-in" element={<SignInPage />} />

                    <Route path="/sign-up" element={<SignUpPage />} />

                    <Route path="/sign-in/reset-password" element={<ForgotPasswordPage />} />

                    <Route path="/sport" element={<SportPage />} />

                    <Route path="/sport/:sportName" element={<LeaguePage />} />

                    <Route path="/sport/:sportName/league/:leagueName" element={<TeamPage />} />

                    <Route path="/stream" element={<GamesPage />} />

                    <Route path="/stream/:gameId" element={<InsideStreamPage />} />

                    <Route path="/streamq" element={<InsideStreamPage />} />

                    <Route path="/news/:articleId" element={<InsideNewsPage />} />

                    <Route path="/not-existing" element={<NotExistingPage />} />

                    <Route path="*" element={<Navigate to="/not-existing" replace />} />

                    <Route exact path="/FAQ" element={<FAQpage />} />

                    <Route exact path="/AboutUs" element={<AboutUsPage />} />

                    <Route exact path="/SearchPageTamplate" element={<AboutUsPage/>}/>

                </Routes>

                {<Footer />}

            </Router>

        </>
    );
}

export default App;