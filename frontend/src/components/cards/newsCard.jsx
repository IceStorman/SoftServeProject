import React from "react";
import { FaHeart } from "react-icons/fa";
import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import globalVariables from "../../globalVariables";


function NewsCard({ title, date, img, sport, id = 1, content, likes = 10, width, height, isFoil, article}) {
  const isVertical = height >= width;
  const isSmall = width < 301 || height < 301;
  const maxLines = isVertical ? 3 : 2;

  const newsData = {
    article,
    likes,
  };

  return (
      <NavLink
          to={`${globalVariables.routeLinks.newsPath}${id}`} state={{ newsData }}
          className="nav-link"
          activeClassName="active"
      >
        <div
            className={`news-card ${isVertical ? "vertical" : "horizontal"} ${isSmall ? "small" : "big"} ${isFoil ? "foil" : ""}`}
            style={{width: width, height: height}}
        >
          {img && (
              <div className={isVertical ? "image vertical" : "image horizontal"}>
                <img
                    src={img}
                    alt={title}
                    className="img-content"
                />
              </div>
          )}
          <div className={`content ${isVertical ? "vertical" : "horizontal"}`}>
            <div>
              <span className="tag">{sport}</span>
              <h2 className="title">{title}</h2>
              {!isSmall && (
                  <p className="subtitle" title={content} style={{WebkitLineClamp: maxLines}}>
                    {content}
                  </p>
              )}
            </div>
            <div className="details">
              <div className="date">{date}</div>
              <div className="like-vrapper">
                <div className="like-content">
                  <FaHeart className="like-icon"/> {likes}
                </div>
              </div>
            </div>
          </div>
        </div>
      </NavLink>
  );
}

export default NewsCard;
