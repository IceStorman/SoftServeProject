import React from 'react';
import ReactDOM from 'react-dom/client';
import './scss/index.scss';
import App from './js/App';
import {AuthProvider} from "./pages/registration/AuthContext";
import {FilterProvider} from "./components/filters/filterContext";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <FilterProvider>
        <AuthProvider>
            <App />
        </AuthProvider>
    </FilterProvider>
);