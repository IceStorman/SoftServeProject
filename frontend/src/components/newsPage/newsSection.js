import React from "react";

function NewsSection({text, img, subheading}){

    return(
        <section className={"newsSection"}>

            {!(subheading.length === 0) ? <h2>{subheading}</h2> : null}

            <div className={"sectionContent"}>

                <div className={"imgContainer"}>
                    <img src={img}/>
                </div>

                <p>{text}</p>

            </div>

        </section>
    );
}

export default NewsSection;