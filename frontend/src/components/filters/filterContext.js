import { createContext, useState, useEffect } from "react";
import Cookies from "js-cookie";

export const FilterContext = createContext(null);

export const FilterProvider = ({ children }) => {
    const [countriesData, setCountriesData] = useState(() => {
        const storedFiltersData = Cookies.get("countries");
        return storedFiltersData ? JSON.parse(storedFiltersData) : null;
    });

    const countriesInput = (countriesData) => {
        console.log("vvvvvv",countriesData);
        Cookies.set("countries", JSON.stringify(countriesData), { expires: 30});
        setCountriesData(countriesData);
    };

    useEffect(() => {
        console.log("llll",countriesData);
    }, [countriesData]);

    return (
        <FilterContext.Provider value={{ countriesData, countriesInput }}>
            {children}
        </FilterContext.Provider>
    );
};