import React, {useContext, useEffect, useState} from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {FilterContext} from "./filterContext";


export const CountryFilter= ({ onChange }) => {
    const {countriesData, countriesInput } = useContext(FilterContext);
    const [countries, setCountries] = useState([])

    const [selected, setSelected] = useState(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [filteredCountries, setFilteredCountries] = useState(countriesData);


    useEffect(() => {

        if (countriesData) {
            setCountries(countriesData);
            return;
        }

        axios.get(`${apiEndpoints.url}${apiEndpoints.countries.getAll}`)
            .then(res => {
                const returnedCountries = res.data;
                setCountries(returnedCountries);
                countriesInput(returnedCountries)
            })
            .catch(error => {
                toast.error(`Troubles With Country Loading: ${error}`);
            });
    }, [countriesData, countriesInput]);

    const handleClick = (e) => {
        const countryId = e.target.id;
        setSelected(countryId);
        setSearchQuery("");
        onChange({ target: { value: countryId } });
    };

    const handleSearch = (event) => {
        const query = event.target.value.toLowerCase();
        setSearchQuery(query);

        const filtered = countries.filter((country) =>
            country.name.toLowerCase().includes(query)
        );
        setFilteredCountries(filtered);
    };


    return (
        <div className="scrollContainer">
            <div className="filterSearch">
                <input
                    type="text"
                    placeholder="Select a country..."
                    value={searchQuery}
                    onChange={handleSearch}
                />
            </div>

            <div className="list">
                {filteredCountries.map((country) => (
                    <div
                        key={country.id}
                        id={country.id}
                        className={`listItem ${selected == country.id ? "active" : ""}`}
                        onClick={handleClick}
                    >
                        {country.name}
                    </div>
                ))}
            </div>
        </div>
    );
};