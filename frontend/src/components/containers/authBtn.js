import React from "react";
import globalVariables from "../../globalVariables";

function AuthBtn() {

    function handleGoogleLogin() {
        const clientId = globalVariables.googleAuth.clientId;
        const redirectUri = globalVariables.googleAuth.redirectUri;
        const scope = globalVariables.googleAuth.scope;
        const responseType = globalVariables.googleAuth.responseType;

        const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}`;
        window.location.href = authUrl;
    }

    return (
        <div className="authBtn">
            <button className="google-login" onClick={handleGoogleLogin}>
                <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google logo" />
            </button>
        </div>
    );
}

export default AuthBtn;