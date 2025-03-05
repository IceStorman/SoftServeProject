import React, { useContext, useEffect, useState } from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";
import { Check, Plus } from "lucide-react";
import { AuthContext } from "./AuthContext";


function PreferencesPage() {
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();
    const [choices, setChoices] = useState([]);
    const [userPref, setUserPref] = useState([]);
    const [isActive, setIsActive] = useState({});

    const { user } = authContext;

    const loadUserPreferences = async () => {
        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.preference.getUserPreferences}`,
                {
                    user_id: user?.id, //поки для перевірок заміняємо на потрібний, після тараса пр, можна не хардкодити
                    type: 'sport',
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );
            setUserPref(response.data);
        } catch (err) {
            toast.error("Error with user preferences!");
        }
    };

    const changeUserPreferences = async (preferences) => {
        try {
            if (preferences.length > 0){
                await axios.post(
                    `${apiEndpoints.url}${apiEndpoints.preference.changeUserPreferences}`,
                    {
                        preferences: preferences,
                        user_id: user?.id,
                        type: 'sport',
                    },
                    {
                        headers: { 'Content-Type': 'application/json' },
                    }
                );
            }else {
                await axios.delete(
                    `${apiEndpoints.url}${apiEndpoints.preference.changeUserPreferences}`,
                    {
                        data: {
                            preferences: [],
                            user_id: user?.id,
                            type: 'sport',
                        },
                        headers: { 'Content-Type': 'application/json' },
                    }
                );
            }

            toast.success('Your preferences have been updated!');
            navigate('/');
        } catch (err) {
            toast.error("Error with changing user preferences!");
        }
    };

    useEffect(() => {
        axios
            .get(`${apiEndpoints.url}${apiEndpoints.sports.getAll}`)
            .then((res) => {
                const returnedSports = res.data;
                setChoices(returnedSports);
            })
            .catch((error) => {
                toast.error(`Troubles With Choices Loading: ${error}`);
            });
    }, []);

    useEffect(() => {
        loadUserPreferences();
    }, []);

    useEffect(() => {
        const activeItems = {};
        if (choices && userPref) {
            choices.forEach((choice) => {
                const isActiveItem = userPref.some(
                    (pref) => pref?.sports_id === choice?.id.toString()
                );
                if (isActiveItem) {
                    activeItems[choice.id] = true;
                }
            });
            setIsActive(activeItems);
        }
    }, [choices, userPref]);

    const toggleChoice = (id) => {
        setIsActive((prevState) => ({
            ...prevState,
            [id]: !prevState[id],
        }));
    };

    function handleSubmit() {
        const activeItems = Object.keys(isActive).filter((id) => isActive[id]);
        changeUserPreferences(activeItems);
    }

    return (
        <section className={"preferences registration"}>
            <div className={"preferencesHeading"}>
                <h1>What are you interested in?</h1>
                <h3>Choose your favourite sports:</h3>
            </div>

            <section className={"preferencesChoices"}>
                {choices.map((choice) => (
                    <button
                        className={"choice filled"}
                        key={choice?.id}
                        onClick={() => toggleChoice(choice?.id)}
                    >
                        {choice?.sport}
                        {isActive[choice?.id] ? <Check size={24} /> : <Plus size={24} />}
                    </button>
                ))}
            </section>

            <div className={"controlBtnBox"}>
                <h3 onClick={() => navigate('/')}>Skip ></h3>
                <button className={"filled"} onClick={handleSubmit}>Confirm?</button>
            </div>
        </section>
    );
}

export default PreferencesPage;
