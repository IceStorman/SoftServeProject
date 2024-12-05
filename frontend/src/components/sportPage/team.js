import React from "react";

function Team({name, logo}){

    return (
        <div className={"team"}>

            <img src={logo} alt={name}/>

        </div>
    );
}

export default Team;