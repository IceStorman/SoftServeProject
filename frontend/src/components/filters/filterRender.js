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
            };

            updatedFilters.push(newFilter);
        }
        setFilters(updatedFilters);
        onFilterChange(updatedFilters);
    };

    return (
        <div className="filters">
            <h3>Filters for {model}:</h3>
            {Object.entries(selectedFilters).map(([key, Component]) => (
                <Component onChange={(e) => handleChange(key, e.target.value)} sportId={sportId}/>
            ))}
        </div>
    );
};

export default FiltersRenderer;
