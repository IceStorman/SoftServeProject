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

// import Home component
import homePage from "../pages/mainPage";
// import About component
import SignUpPage from "../pages/signUpPage";
import MainPage from "../pages/mainPage";

function App(){
    const [tab, setTab] = useState('about');

    return (
        <>

            <Router>

                <header>
                    <Link className="title" to={"/"}>
                        <span className="red">КУЙ</span>Sport
                    </Link>

                    <div className="nav-menu">

                        <Link to={"/"}>Трансляції</Link>
                        <Link to={"/"}>Розклад подій</Link>
                        <Link className="sign" to={"/sign-up"}>Вхід</Link>

                    </div>

                </header>

                <Routes>

                    <Route exact path="/" element={<MainPage />} />

                    <Route path="/sign-up" element={<SignUpPage />} />

                    <Route path="*" element={<Navigate to="/" />} />

                </Routes>

                <footer>

                    <h1>Some silly text to style the footer</h1>

                </footer>

            </Router>

        </>
    );
}

export default App;