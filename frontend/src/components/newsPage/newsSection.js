import React from "react";

function NewsSection({text, img, subheading}){

    return(
        <section className={"newsSection"}>

            {subheading ? <h2>{subheading}</h2> : null}

            <div className={"sectionContent"}>
                <p>{text}</p>

                <img src={img}/>
            </div>

        </section>
    );
}

export default NewsSection;