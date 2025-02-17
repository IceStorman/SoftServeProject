const apiEndpoints = {
    url: 'http://127.0.0.1:5001/',

    news: {
        getRecent: 'news/recent',
        getSport: 'news/',
        getArticle: 'news/article',
        getCurrentNews: '',
        likeArticle: 'like',
    },

    sports:{
        getAll: 'sports/all',
        getLeague: 'sports/league',
        getLeagueSearch: 'sports/league/search'
    },

    teams:{
        getAll: 'teams/league',
    },
    
    games:{
        getGames: 'games/specific',
        getThisGame: 'games/this',
        getGame: 'games/today',
    },

    countries:{
        getAll: 'countries'
    },

    stream:{
        getAll: 'streams/all',
        getInfo: 'streams/info'
    },

    localization:{
        userBaseLanguage: 'localization',
        setLanguage: 'set_language',
    },

    user:{
        resetPasswordRequest: 'login/reset-password-request',
        resetPassword: 'login/reset-password',
    }
};

export default apiEndpoints;
