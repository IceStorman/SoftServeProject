import React, { createContext, useContext, useEffect, useState } from 'react';
import apiEndpoints from "./apiEndpoints";
import axios from 'axios';
import {toast} from "sonner";

const InteractionContext = createContext();

export const InteractionProvider = ({ children }) => {
    const [interactionTypes, setInteractionTypes] = useState(() => {
        return JSON.parse(localStorage.getItem('interactionTypes')) || {};
    });

    useEffect(() => {
        const getInteractionTypes = async () => {
            try {
                const response = await axios.get(`${apiEndpoints.url}${apiEndpoints.interactions.getInteractionTypes}`);
                const types = response.data;
                localStorage.setItem('interactionTypes', JSON.stringify(types));
                setInteractionTypes(types);
            } catch (error) {
                toast.error("Error fetching interaction types:", error);
            }
        };

        if (Object.keys(interactionTypes).length === 0) {
            getInteractionTypes();
        }
    }, []);

    return (
        <InteractionContext.Provider value={interactionTypes}>
            {children}
        </InteractionContext.Provider>
    );
};

export const useInteractionTypes = () => {
    return useContext(InteractionContext);
};
