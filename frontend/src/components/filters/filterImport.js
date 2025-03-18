import React, {useMemo} from "react"
import {SportFilter} from "./sportFilter";
import {NameFilter} from "./nameFilter";
import {CountryFilter} from "./countryFilter";

//
// function FilterImport({ modelName }) {
//
//     const filtersImports = {
//         leagues: {
//             title: "text",
//             sport_id: "",
//             country_id: "",
//         },
//     };
//
//     const checkModel = (name) => {
//         return filtersImports[name] || null;
//     };
//
//     const currentFilters = checkModel(modelName);
//
//     return (
//         <div className="filters">
//
//         </div>
//     );
// }
//
// export default FilterImport;
const a = true

export const filtersImports = {
    leagues: {
        name: (props) => <NameFilter {...props} />,
        sport_id: (props) => {
            if (props.sportId) return null;
            return <SportFilter {...props} />;
        },
        country_id: (props) => <CountryFilter {...props} />,
    }
};
