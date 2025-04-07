const apiEndpoints = {
    url: 'https://localhost:5001/',

    news: {
        getRecent: 'news/recent',
        getSport: 'news/',
        getArticle: 'news/article',
        getCurrentNews: '',
        likeArticle: 'like',
        getRecommendations: 'news/recommendation',
        getPaginated: 'news/search'
    },

    sports:{
        getAll: 'sports/all',
        getLeague: 'sports/league',
        getLeagueSearch: 'sports/league/search'
    },

    teams:{
        getTeamsSearch: 'teams/search',
        getTeamsAll: 'teams/league',
        getTeamsPlayers: 'teams/players',
    },

    players:{
        getPlayersAll: 'teams/players',
    },
    
    games:{
        getGames: 'games/search',
        getThisGame: 'games/this',
        getGame: 'games/today',
    },

    countries:{
        getAll: 'countries'
    },

    stream:{
        getStreamsSearch: 'streams/search'
    },

    localization:{
        userBaseLanguage: 'localization',
        setLanguage: 'set_language',
        ver: 'localization/version'
    },

    user: {
        signUp: 'user/sign-up',
        login: 'user/login',
        resetPasswordRequest: 'user/reset-password-request',
        resetPassword: 'user/reset-password',
        refresh: 'user/refresh'
    },

    preference:{
        getUserPreferences: 'preferences/get',
        changeUserPreferences: 'preferences/'
    },

    comment:{
        save: 'comments',
        update: (id) => `comments/${id}`,   
        delete: (id) => `comments/${id}`,
        getAll: 'comments'
    }
};

export default apiEndpoints;
