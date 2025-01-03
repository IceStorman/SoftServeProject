import React from "react";

function NewsSection({text, teams, img, subheading}){
    
    const highlightText = (text) => {
        return teams.reduce((item, team) => {
            const regex = new RegExp(` (${team}) `, 'gi');
            return item.replace(regex, ` <span class="highlighted">${team}</span> `);
        }, text);
    };

    const highlightedText = highlightText(text.join(' '));

    return(
        <section className={"newsSection"}>

            {!(subheading.length === 0) ? <h2>{subheading}</h2> : null}

            <div className={"sectionContent"}>

                {img ?
                    <div className={"imgContainer"}>
                        <img src={img} alt={subheading}/>
                    </div>
                : null
                }

                <p dangerouslySetInnerHTML={{__html: highlightedText}}></p>

            </div>

        </section>
    );
}

export default NewsSection;