import React, {useContext, useEffect} from "react";
import { useState } from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import {AuthContext} from "../../pages/registration/AuthContext";


function TeamCard({
        leagueName: teamName,
        img,
        id,
        size,
        sportId,
        sportName,
        leagueId,
        page,
        favoriteTeams,
        handleApplyFavoriteTeams
    }) {
    const [isFlipped, setIsFlipped] = useState(false);
    const [isFavorite, setIsFavorite] = useState(false);
    const isSportValid = (sportName) => sportsArray.includes(sportName);
    const hideText = size === "medium" || size === "large";
    const [players, setPlayers] = useState([]);
    const {user} = useContext(AuthContext);

    useEffect(() => {
        for (let i = 0; i < favoriteTeams?.length; i++) {
            if (favoriteTeams[i] == id) {
                setIsFavorite(true);
                break;
            }
        }
    }, [favoriteTeams, id]);

    const sportsArray = [
        'nfl',
        'mma',
        'football',
        'basketball',
    ];

    const handleFlip = () => {
        if (!isFlipped && isSportValid(sportName)) {
            getPlayers();
        }
        setIsFlipped(!isFlipped);
    };

    useEffect(() => {
        if (isFlipped) {
            setIsFlipped(!isFlipped);
        }
    }, [page])


    const toggleFavorite = async (e) => {
        e.stopPropagation();
        setIsFavorite((prev) => !prev);

        try {
            if (!isFavorite) {
                await axios.post(
                    `${apiEndpoints.url}${apiEndpoints.preference.changeUserPreferences}`,
                    {
                        preferences: [...favoriteTeams, id],
                        user_id: user?.user_id,
                        type: 'team',
                    },
                    {
                        headers: { 'Content-Type': 'application/json' },
                    }
                );
            } else {
                await axios.delete(
                    `${apiEndpoints.url}${apiEndpoints.preference.changeUserPreferences}`,
                    {
                        data: {
                            preferences: [id],
                            user_id: user?.user_id,
                            type: 'team',
                        },
                        headers: { 'Content-Type': 'application/json' },
                    }
                );
            }
            handleApplyFavoriteTeams()
        } catch (error) {
            handleApplyFavoriteTeams()
            // toast.error(`Error updating favorites: ${error}`);
        }
    };

    const getPlayers = async (retryCount = 0) => {
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

                if (retryCount < 2) {
                    return getPlayers(retryCount + 1);
                } else {
                    setPlayers([]);
                    return;
                }
            }

            setPlayers(response.data.items);

        } catch (error) {
            if (retryCount < 2) {
                return getPlayers(retryCount + 1);
            } else {
                toast.error(`:( Troubles With Leagues Loading: ${error}`);
            }
        }
    };

    return (
        <div
            className={`team-card  horizontal ${size} ${isFlipped ? "flipped" : ""}`}
            onClick={handleFlip}
        >
            <div className="team-card-front">
                {img &&
                    <div className={`image horizontal ${size}`}>
                        <img src={img} alt={teamName} className="img-content"/>
                    </div>
                }
                {!hideText &&
                    <div className={`content ${size}`}>
                        <h1>{teamName}</h1>
                    </div>
                }
                {user &&
                    <button className={`favorite-btn ${isFavorite ? "active" : ""}`}
                            onClick={toggleFavorite}
                            aria-label="Add to favorites">
                        <div className="star"></div>
                    </button>
                }


            </div>

            <div className="team-card-back">
                <h1>{teamName}</h1>
                {players && players?.length > 0 ? (
                    <div className="players-list">
                        {players.map((player) => (
                            <div key={player.id} className="player-item">
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