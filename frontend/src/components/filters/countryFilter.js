import React, {useContext, useEffect, useState} from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {FilterContext} from "./filterContext";


export const CountryFilter= ({ onChange }) => {
    const {countriesData, countriesInput } = useContext(FilterContext);
    const [countries, setCountries] = useState([])

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

    return (

        <select onChange={onChange}>
            <option value="">Choose country: </option>
            {countries.map((country) => (
                <option key={country.id} value={country.id}>
                    {country.name}
                </option>
            ))}
        </select>
    );
};