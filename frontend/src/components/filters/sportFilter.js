import React, {useEffect, useState} from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";


export const SportFilter = ({ onChange }) => {
    const [sports, setSports] = useState([]);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.sports.getAll}`)
            .then(res => {
                const returnedSports = res.data;
                setSports(returnedSports);
            })
            .catch(error => {
                toast.error(`Troubles With Sports Loading: ${error}`);
            });
    }, []);


    return (
        <>
            <div className="sportFilter">
                <select onChange={onChange} className="sportInput">
                    <option value="">Choose sport:</option>
                    {sports.map((sport) => (
                        <option key={sport.id} value={sport.id}>
                            {sport.sport}
                        </option>
                    ))}
                </select>
            </div>
        </>

    );
};