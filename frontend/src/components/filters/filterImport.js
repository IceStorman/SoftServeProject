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
        date_from: (props) => <DateFilter {...props} />
    },
    news: {
        title_contains: (props) => <NameFilter {...props} />,
        sport_id: (props) => <SportFilter {...props} />,
        date_from: (props) => <DateFilter {...props} />,
        date_to: (props) => <DateFilter {...props} />,
    },
    games: {
        team_home: (props) => <NameFilter {...props} />,
        sport_id: (props) => <SportFilter {...props} />,
        date_from: (props) => <DateFilter {...props} />,
        date_to: (props) => <DateFilter {...props} />,
        country_id: (props) => <CountryFilter {...props} />,
    }
};
