import React from "react";
import GoogleButton from "react-google-button";
import globalVariables from "../../globalVariables";

function AuthBtn() {
    function handleGoogleLogin() {
        const { clientId, redirectUri, scope, responseType } = globalVariables.googleAuth;
        window.location.href = `${globalVariables.googleAuth.defaultLink}client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}`;
    }

    return (
        <div className="authBtn">
            <GoogleButton onClick={handleGoogleLogin} />
        </div>
    );
}

export default AuthBtn;
