const apiEndpoints = {
    url: 'http://127.0.0.1:5001/',

    news: {
        getRecent: 'news/recent',
        getSport: 'news/',
        getCurrentNews: ''
    },

    sports:{
        getAll: 'sports/all',
        getLeague: 'sports/league',
        getLeagueSearch: 'sports/league/search'
    },

    team:{
        getAll: 'team/'
    },
    
    games:{
        getGames: 'games/'
    },

    countries:{
        getAll: 'countries'
    }
};

export default apiEndpoints;
