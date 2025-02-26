const globalVariables= {
    authStrategies:{
        simpleStrategy: "simple",
        googleStrategy: "google"
    },

    googleAuth:{
        clientId: process.env.REACT_APP_GOOGLE_CLIENT_ID,
        redirectUri: process.env.REACT_APP_GOOGLE_REDIRECT_URI,
        scope: "openid email",
        responseType: "code"
    },

    authMessages:{
        successLogIn: "You have successfully signed up",
        passwordMessage: "Password must contain at least 8 symbols, where: 1 uppercase letter, 1 lowercase letter and 1 number",
        UsernameError: "Username is empty or contains invalid characters",
        EmailError: "Email is empty or contains invalid characters",
        EmailMessage: "email: example@email.com",
        UsernameOrEmailError: "Email or Username are empty or contains invalid characters"
    }
}

export default globalVariables;