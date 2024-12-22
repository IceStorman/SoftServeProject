import React, {useEffect, useRef, useState} from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";

function DropDown({setCountry}){
    const [countries, setCountries] = useState([])
    const [isActive, setIsActive] = useState(false);
    const dropdownRef = useRef(null);


    function handleClick(e){
        setCountry(e.target.id);
        setIsActive(false);
    }

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.countries.getAll}`)
            .then(res => {
                const returnedCountries = res.data;
                setCountries(returnedCountries);
            })
            .catch(error => {
                toast.error(`:( Troubles With Country Loading: ${error}`);
            });
    }, []);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsActive(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    function handleMenu(){
        isActive ? setIsActive(false) : setIsActive(true)
    }

    return(
        <div className={"leaguesCountry"} ref={dropdownRef}>
            <button className={`dropButton ${isActive ? "" : "inActiveDrop"}`} onClick={handleMenu}>Country</button>

            <div className={`dropMenu ${isActive ? "" : "hidden"}`}>

                <h1 key={-1} id={-1} onClick={handleClick}>All</h1>

                {countries.map((item, index) => {
                    return <h1 key={index} id={item.id} onClick={handleClick}>{item.name}</h1>
                })}

            </div>
        </div>
    );
}

export default DropDown;