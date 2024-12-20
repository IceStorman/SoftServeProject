import React, {useEffect, useRef, useState} from "react";

function DropDown({setCountry}){
    const [choice, setChoice] = useState(['Ukraine', 'USA', 'Germany', 'Poland', 'France'])
    const [isActive, setIsActive] = useState(false);
    const dropdownRef = useRef(null);

    function handleClick(e){
        setCountry(e.target.textContent);
        setIsActive(false);
    }

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

                <h1 key={-1} onClick={handleClick}>All</h1>
                <h1 key={0} onClick={handleClick}>{choice[0]}</h1>
                <h1 key={1} onClick={handleClick}>{choice[1]}</h1>
                <h1 key={2} onClick={handleClick}>{choice[2]}</h1>
                <h1 key={3} onClick={handleClick}>{choice[3]}</h1>
                <h1 key={4} onClick={handleClick}>{choice[4]}</h1>
                <h1 key={5} onClick={handleClick}>{choice[0]}</h1>
                <h1 key={6} onClick={handleClick}>{choice[1]}</h1>
                <h1 key={7} onClick={handleClick}>{choice[2]}</h1>
                <h1 key={8} onClick={handleClick}>{choice[3]}</h1>
                <h1 key={9} onClick={handleClick}>{choice[4]}</h1>
                <h1 key={10} onClick={handleClick}>{choice[0]}</h1>
                <h1 key={11} onClick={handleClick}>{choice[1]}</h1>
                <h1 key={12} onClick={handleClick}>{choice[2]}</h1>
                <h1 key={13} onClick={handleClick}>{choice[3]}</h1>
                <h1 key={14} onClick={handleClick}>{choice[4]}</h1>
                <h1 key={15} onClick={handleClick}>{choice[0]}</h1>
                <h1 key={16} onClick={handleClick}>{choice[1]}</h1>
                <h1 key={17} onClick={handleClick}>{choice[2]}</h1>

                {choice.map((item, index) => {
                    <h1 key={index} onClick={handleClick}>{item}</h1>
                })
                }

            </div>
        </div>
    );
}

export default DropDown;