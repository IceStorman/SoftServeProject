import React from 'react';
import ReactDOM from 'react-dom/client';
import './scss/index.scss';
import App from './js/App';
import {AuthProvider} from "./pages/registration/AuthContext";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <AuthProvider>
        <App />
    </AuthProvider>
);