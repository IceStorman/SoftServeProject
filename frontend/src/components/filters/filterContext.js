import { createContext, useState } from "react";
import store from 'store';

export const FilterContext = createContext(null);

export const FilterProvider = ({ children }) => {
    const [countriesData, setCountriesData] = useState(() => {
        return store.get("countries") || null;
    });

    const countriesInput = (countriesData) => {
        store.set("countries", countriesData);
        setCountriesData(countriesData);
    };


    return (
        <FilterContext.Provider value={{ countriesData, countriesInput }}>
            {children}
        </FilterContext.Provider>
    );
};