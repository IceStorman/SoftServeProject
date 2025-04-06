import React, {useContext, useEffect, useState} from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {FilterContext} from "./filterContext";
import useTranslations from "../../translationsContext";


export const TeamFilter = ({ onChange, placeholder}) => {
    const {teamsData, teamsInput } = useContext(FilterContext);
    const [teams, setTeams] = useState([])

    const [selected, setSelected] = useState(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [filteredTeams, setFilteredTeams] = useState([]);
    const [isActiveAll, setIsActiveAll] = useState(false);

    const { t } = useTranslations();

    useEffect(() => {

        if (teamsData) {
            setFilteredTeams(teamsData);
            setTeams(teamsData)
            return;
        }

        axios.post(`${apiEndpoints.url}${apiEndpoints.teams.getTeamsSearch}`,  {
    
                filters: [{filter_name: "a"}]
            },
            {
                headers: { 'Content-Type': 'application/json' },
            })
            .then(res => {

                const returnedTeams = res.data.items;
               
                setTeams(returnedTeams);
                setFilteredTeams(returnedTeams);
                teamsInput(returnedTeams)
            })
            .catch(error => {
                toast.error(`Troubles With Country Loading: ${error}`);
            });

    }, [teamsData, teamsInput]);

    const handleClick = (e) => {
        const teamId = e.target.id;
        setSelected(teamId);
        setSearchQuery("");
        if (isActiveAll) {
            setIsActiveAll(!isActiveAll);
        }

        onChange({ target: { value: teamId } });
    };

    const handleSearch = (event) => {
        const query = event.target.value.toLowerCase();
        setSearchQuery(query);

        const filtered = teams.filter((team) =>
            team?.team_name.toLowerCase().includes(query)
        );
        setFilteredTeams(filtered);
    };

    const handleReset = () => {
        setIsActiveAll(!isActiveAll);
        setSelected(null);
        setSearchQuery("");
        setFilteredTeams(teams);
        onChange({ target: { value: "" } });
    };


    return (
        <div className="scrollContainer">
            <div className="filterSearch">
                <input
                    type="text"
                    placeholder={placeholder}
                    value={searchQuery}
                    onChange={handleSearch}
                />
                <button onClick={handleReset} className={`buttonAll ${isActiveAll ? "active" : ""}`}> {t("all")} </button>
            </div>

            <div className="list">
                {filteredTeams.map((team, index) => (
                    <div
                        key={`${team.id}-${index}`}
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