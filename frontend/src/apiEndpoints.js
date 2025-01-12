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
        getGames: 'games/',
        getThisGame: 'games/this'
    },

    countries:{
        getAll: 'countries'
    },

    stream:{
        getAll: 'streams/all',
        getInfo: 'streams/info'
    }
};

export default apiEndpoints;
