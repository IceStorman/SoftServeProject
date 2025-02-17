import React from "react";
import GoogleButton from "react-google-button";
import globalVariables from "../../globalVariables";

function AuthBtn() {
    function handleGoogleLogin() {
        const { clientId, redirectUri, scope, responseType } = globalVariables.googleAuth;
        const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}`;
        window.location.href = authUrl;
    }

    return (
        <div className="authBtn">
            <GoogleButton onClick={handleGoogleLogin} />
        </div>
    );
}

export default AuthBtn;
