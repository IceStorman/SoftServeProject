import React from "react";

function NoItems({text}){

    return (
        <div className={"noItems"}>
            <h1>{text} :(</h1>
        </div>
    );
}

export default NoItems;