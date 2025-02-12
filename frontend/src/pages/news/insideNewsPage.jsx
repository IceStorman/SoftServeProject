import React from "react";
import img1 from '../imgs/1.jpg'
import { FaRegHeart } from "react-icons/fa";
import { FaHeart } from "react-icons/fa";


export default function InsideNewsPage() {


    const title = 'Metallum Nostrum'
    const sport = 'Football'
    const date = '2025-01-23'
    const likes = 10
    const content = 'Howling winds keep screaming around And the rain comes pouring down Doors are locked and bolted now As the thing crawls into town Straight out of hell One of a kind Stalking his victim Don t look behind you Night crawler Beware the beast in black Night crawler You know he s coming back Night crawler'

    return (
        <section className="news-block">

            <h1>{title}</h1>

            <div className="tags">
                <p>Tags:</p>
                <span className="tag">{sport}</span>
            </div>

            <img src={img1} alt={title} />

            <section className="content">
                {content}
            </section>

            <div className="details">
                <div className="date">{date}</div>
                <button className="like-vrapper">
                    <div className="like-content">
                    <FaRegHeart /> {likes}
                    </div>
                </button>
            </div>

            <section className="comments">
            
                <hr />
               
            </section>

        </section>
    );
}