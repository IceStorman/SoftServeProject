const globalVariables= {
    authStrategies:{
        simpleStrategy: "simple",
        googleStrategy: "google"
    },

    googleAuth:{
        clientId: "829213951149-inaonf6rlebslvuv2eihissm0dmmvj66.apps.googleusercontent.com",
        redirectUri: "http://localhost:3000/sign-in/google",
        scope: "openid email",
        responseType: "code"
    }
}

export default globalVariables;