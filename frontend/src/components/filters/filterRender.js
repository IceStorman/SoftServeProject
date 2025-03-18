import React, {useState} from "react";
import { filtersImports} from "./filterImport";

const FiltersRenderer = ({ model, onFilterChange, sportId }) => {
    const selectedFilters = filtersImports[model] || {};
    const [filters, setFilters] = useState([]);

    const handleChange = (key, value, order, field) => {
        const updatedFilters = filters.filter(f => f.filter_name !== key);
        if (value !== "") {
            let newFilter = {
                filter_name: key,
                filter_value: value,
                // order_type:  order ? order : "",
                // order_field: field ? field : ""
            };

            updatedFilters.push(newFilter);
        }
        setFilters(updatedFilters);
        onFilterChange(updatedFilters);
    };

    // const handleOrder = () => {
    //     if (filters) {
    //         filters[0].order_type = filters.order_type;
    //         filters[0].order_field = filters.order_field;
    //     }
    // }

    return (
        <div>
            <h3>Filters for {model}:</h3>
            {Object.entries(selectedFilters).map(([key, Component]) => (
                <div key={key}>
                    <Component onChange={(e) => handleChange(key, e.target.value)} sportId={sportId}/>
                </div>
            ))}
            {/*<button onClick={onFilterChange}>Filter</button>*/}

        </div>
    );
};

export default FiltersRenderer;
