import React, {useEffect, useState} from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";


export const CountryFilter= ({ onChange }) => {
    const [countries, setCountries] = useState([]);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.countries.getAll}`)
            .then(res => {
                console.log(res.data);
                const returnedSports = res.data;
                setCountries(returnedSports);
            })
            .catch(error => {
                toast.error(`Troubles With Country Loading: ${error}`);
            });
    }, []);

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