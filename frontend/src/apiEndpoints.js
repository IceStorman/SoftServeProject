const apiEndpoints = {
    url: 'http://127.0.0.1:5001/',

    news: {
        getRecent: 'news/recent',
        getSport: 'news/'
    },

    sports:{
        getAll: 'sports/all',
    },

    team:{
        getAll: 'team/'
    },
    
    games:{
        getGames: 'games/'
    }
};

export default apiEndpoints;
