import React from "react";

function TeamsBtn({name, logo}){

    return (
        <div className={"iconsBlockElement"} >

            <img src={logo} alt={name}/>

        </div>
    );
}

export default TeamsBtn;