import React, {useContext, useEffect, useState} from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {FilterContext} from "./filterContext";
import useTranslations from "../../translationsContext";


export const TeamFilter= ({ onChange }) => {
    const {countriesData, countriesInput } = useState();
    const [countries, setCountries] = useState([])

    const [selected, setSelected] = useState(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [filteredCountries, setFilteredCountries] = useState([]);
    const [isActiveAll, setIsActiveAll] = useState(false);

    const { t } = useTranslations();

    useEffect(() => {

        axios.post(`${apiEndpoints.url}${apiEndpoints.teams.getTeamsSearch}`,  {
    
                filters: [{filter_name: "a"}]
            },
            {
                headers: { 'Content-Type': 'application/json' },
            })
            .then(res => {

                const returnedCountries = res.data.items;
                console.log(returnedCountries)
                setCountries(returnedCountries);
                setFilteredCountries(returnedCountries);
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
        if (isActiveAll) {
            setIsActiveAll(!isActiveAll);
        }

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

    const handleReset = () => {
        setIsActiveAll(!isActiveAll);
        setSelected(null);
        setSearchQuery("");
        setFilteredCountries(countries);
        onChange({ target: { value: "" } });
    };


    return (
        <div className="scrollContainer">
            <div className="filterSearch">
                <input
                    type="text"
                    placeholder={t("select_country")}
                    value={searchQuery}
                    onChange={handleSearch}
                />
                <button onClick={handleReset} className={`buttonAll ${isActiveAll ? "active" : ""}`}> {t("all")} </button>
            </div>

            <div className="list">
                {filteredCountries.map((team) => (
                    <div
                        key={team.id}
                        id={team.id}
                        className={`listItem ${selected == team.id ? "active" : ""}`}
                        onClick={handleClick}
                    >
                        {team.team_name}
                    </div>
                ))}
            </div>
        </div>
    );
};