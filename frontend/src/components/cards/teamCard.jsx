import React, {useEffect} from "react";
import { useState } from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";


function TeamCard({ leagueName: teamName, img, id, size, sportId, sportName, leagueId, page}) {
    const [isFlipped, setIsFlipped] = useState(false);
    const hideText = size === "medium" || size === "large";
    const [players, setPlayers] = useState([]);

    const sportsArray = [
        'nfl',
        'mma',
        'football',
        'basketball',
    ];

    const isSportValid = (sportName) => sportsArray.includes(sportName);

    const handleFlip = () => {
        if (!isFlipped) {
            if (isSportValid(sportName)) {
                getPlayers()
            }
        }
        setIsFlipped(!isFlipped);
    };

    useEffect(() => {
        if (isFlipped) {
            setIsFlipped(!isFlipped);
        }
    }, [page])

    const getPlayers = async () => {
        try {
            const filtersData = [
                { 'filter_name': 'sport_id', 'filter_value': sportId },
                { 'filter_name': 'team_id', 'filter_value': id }
            ];

            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.players.getPlayersAll}`,
                {
                    sport_id: sportId,
                    league_id: leagueId,
                    team_id: id,

                    filters_data: {
                        filters: filtersData
                    }
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            if (!response.data.items) {
                if (response.data.results === 0) {
                    setPlayers([]);
                    return;
                }
                return getPlayers()
            }
            setPlayers(response.data.items);

        } catch (error) {
            toast.error(`Troubles With Leagues Loading: ${error}`);
        }
    };

    return (
        <div
            className={`team-card  horizontal ${size} ${isFlipped ? "flipped" : ""}`}
            onClick={handleFlip}
        >
            <div className="team-card-front">
                {img && (
                    <div className={`image horizontal ${size}`}>
                        <img src={img} alt={teamName} className="img-content"/>
                    </div>
                )}
                {!hideText && (
                    <div className={`content ${size}`}>
                        <h1>{teamName}</h1>
                    </div>
                )}
            </div>

            <div className="team-card-back">
                <h1>{teamName}</h1>
                {players && players.length > 0 ? (
                    <div className="players-list">
                        {players.map((player, index) => (
                            <div key={index} className="player-item">
                                <img className="player-photo" alt={player.name} src={player.logo} />
                                <p className="player-name">{player.name}</p>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p>No players available</p>
                )}
            </div>
        </div>
    );
}


export default TeamCard;