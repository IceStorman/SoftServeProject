import React from 'react';
import ReactDOM from 'react-dom/client';
import './scss/index.scss';
import App from './js/App';
import {AuthProvider} from "./pages/registration/AuthContext";
import {FilterProvider} from "./components/filters/filterContext";
import {TranslationsProvider} from "./translationsContext";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <TranslationsProvider>
        <FilterProvider>
            <AuthProvider>
                <App />
            </AuthProvider>
        </FilterProvider>
    </TranslationsProvider>
);