const globalVariables= {
    authStrategies:{
        simpleStrategy: "simple",
        googleStrategy: "google"
    },

    googleAuth:{
        defaultLink: "https://accounts.google.com/o/oauth2/v2/auth?",
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
    },

    windowsSizes: [
        { maxWidth: 480, limit: 0 },
        { maxWidth: 1024, limit: 1 },
        { maxWidth: Infinity, limit: 3 }
    ],

    screenSizes: {
        large: 1024,
        medium: 768,
        small: 480,
    },

    windowsSizesForCards: {
        desktopLarge: 1400,
        desktopMid: 1200,
        tablet: 1000,
        mobileLarge: 450,
        mobileSmall: 600,
    },

    cardLayouts: {
        large: { baseRows: 4, baseColumns: 4, minColumns: 1, alwaysColumns: 4},
        medium: { baseRows: 5, baseColumns: 5, minColumns: 2, alwaysColumns: 4},
        small: { baseRows: 8, baseColumns: 2, minColumns: 2, alwaysColumns: 2}
    },

    newsLayouts: {
        large: { baseRows: 4, baseColumns: 4, minColumns: 1, alwaysColumns: 4},
        medium: { baseRows: 5, baseColumns: 5, minColumns: 2, alwaysColumns: 4},
        small: { baseRows: 8, baseColumns: 2, minColumns: 2, alwaysColumns: 2}
    },

    windowSizeForBurger: {
        filters: 1050,
        streams: 1000,
        navBar: 600,
        latestNews: 1220,
        latestGames: 1024
    },

    routeLinks: {
        defaultRoute: "/",
        nonExistingRoute: "/not-existing",
        nonExistingPath: "*",
        signInRoute: "/sign-in",
        signInGoogleRoute: "/sign-in/google",
        signUpRoute: "/sign-up",
        preferenceRoute: "/user/preferences",
        accountRoute: "/user/account",
        forgotPasswordRoute: "/sign-in/reset-password",
        resetPasswordTokenRoute: "/sign-in/reset-password/:token",
        checkEmailRoute: "/check-email",
        sportPageRoute: "/sport",
        sportPagePath: "/sport/",
        leaguePageRoute: "/sport/:sportName",
        leaguePath: "/league/",
        teamPageRoute: "/sport/:sportName/league/:leagueName",
        streamRoute: "/stream",
        streamPageRoute: "/stream/:streamId",
        streamPagePath: "/stream/",
        newsPageRoute: "/news/:articleId",
        newsPath: "/news/",
        FAQRoute: "/FAQ",
        aboutUsRoute: "/AboutUs",
        searchPageRoute: "/search" 
    }
}

export default globalVariables;