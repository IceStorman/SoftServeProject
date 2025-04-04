import React, {useMemo} from "react"
import {SportFilter} from "./sportFilter";
import {NameFilter} from "./nameFilter";
import {CountryFilter} from "./countryFilter";
import DateFilter from "./dateFilter";
import {TeamFilter} from "./teamFIlter";


export const filtersImports = {
    leagues: {
        name: (props) => <NameFilter {...props} />,
        sport_id: (props) => {
            if (props.sportId) return null;
            return <SportFilter {...props} />;
        },
        country_id: (props) => <CountryFilter {...props} />,
    },
    teams: {
        name: (props) => <NameFilter {...props} />,
        sport_id: (props) => {
            if (props.sportId) return null;
            return <SportFilter {...props} />;
        }
    },
    streams: {
        name: (props) => <NameFilter {...props} />,
        sport_id: (props) => <SportFilter {...props} />,
        date_from: (props) => <DateFilter {...props} label="Select date of beginning" />
    },
    news: {
        title_contains: (props) => <NameFilter {...props} />,
        sport_id: (props) => <SportFilter {...props} />,
        date_from: (props) => <DateFilter {...props} label="Show news from:"/>,
        date_to: (props) => <DateFilter {...props} label="Show news to:"/>,
    },
    games: {
        sport_id: (props) => <SportFilter {...props} />,
        date_from: (props) => <DateFilter {...props} label="Show games from:"/>,
        date_to: (props) => <DateFilter {...props} label="Show games to:"/>,
        country_id: (props) => <CountryFilter {...props} />,
       // team_away: (props) => <TeamFilter {...props} />,
    }
};
