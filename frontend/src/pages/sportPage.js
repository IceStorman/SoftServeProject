import React from "react";
import {useParams} from "react-router-dom";

function SportPage(){
    const { sportName  } = useParams();


    return(
        <>
            <section className={"sportPage"}>

                <h1 className={"sportTitle"}>{ sportName }</h1>

                <section className={"sportNews"}>

                </section>

                <section className={"sportTeams"}>

                </section>

            </section>

        </>
    );
}

export default SportPage;