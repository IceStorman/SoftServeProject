import React from "react";

function scrollTop(){
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function Footer(){

    return (
        <footer>

            <button className={"scrollBtn"} onClick={scrollTop}>
                <i className="fa fa-solid fa-arrow-up fa-10x"></i>
            </button>

            <div className={"footerInfo"}>
                <h1>Vlad help: +380 97 584 22 34</h1>
                <h1>Vlad home: Коломийська 19, кв 20, 5 поверх, 1 під'їзд</h1>
            </div>


        </footer>
    );
}

export default Footer;