import React, {useMemo} from "react"
import {SportFilter} from "./sportFilter";
import {NameFilter} from "./nameFilter";
import {CountryFilter} from "./countryFilter";
import TimeFilter from "./timeFilter";


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
        date_from: (props) => <TimeFilter {...props} />
    }
};
