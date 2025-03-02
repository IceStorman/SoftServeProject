import React from "react";
import { useLocation } from 'react-router-dom';
import { FaRegHeart } from "react-icons/fa";
import useTranslations from "../../translationsContext";


export default function InsideNewsPage() {
    const { t } = useTranslations();
    const location = useLocation();
    const newsData = location.state?.newsData;
    if (!newsData) {

        //    ТУТ АНДРІЙ ТИ В ТЕОРІЇ СВІЙ ЗАПИТ ПИСАТИ БУДЕШ

        return <div>{t("newsNotFound")}</div>;
    }
    const { article, id, likes} = newsData;

    const sections = Object.values(article?.article)
    console.log(article)

    return (
        <section className="news-block">

            <h1>{article?.title}</h1>

            <div className="tags">
                <p>{t("tags")}</p>
                <span className="tag">{article?.S_P_O_R_T}</span>
            </div>

            {article?.images[0] ? <img src={article?.images[0]}/> : null}

            <section className="content">
                {sections.map((item, index) => (
                    <React.Fragment key={index}>
                        {index > 0 && article?.images[index] ? <img src={article?.images[index]}/> : null}
                        <h3>{item?.subheadings[index] || null}</h3>
                        <p>{item?.content}</p>
                        <br/>
                    </React.Fragment>
                ))
                }
            </section>

            <div className="details">
            <div className="date">{article?.timestamp}</div>
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