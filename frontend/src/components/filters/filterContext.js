import { createContext, useState } from "react";
import store from 'store';

export const FilterContext = createContext(null);

export const FilterProvider = ({ children }) => {
    const [countriesData, setCountriesData] = useState(() => {
        return store.get("countries") || null;
    });

    const [teamsData, setreamssData] = useState(() => {
        return store.get("teams") || null;
    });

    const countriesInput = (countriesData) => {
        store.set("countries", countriesData);
        setCountriesData(countriesData);
    };

    const teamsInput = (teamsData) => {
        store.set("teams", teamsData);
        setreamssData(teamsData);
    };


    return (
        <FilterContext.Provider value={{ countriesData, countriesInput, teamsData, teamsInput}}>
            {children}
        </FilterContext.Provider>
    );
};