import React from "react";
import { RiArrowLeftWideLine, RiArrowRightWideLine } from "react-icons/ri";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";

const DotPagination = ({
    totalPosts,
    postsPerPage,
    setCurrentPage,
    currentPage,
}) => {
    let pages = [];

    for (let i = 1; i <= Math.ceil(totalPosts / postsPerPage); i++) {
        pages.push(i);
    }
    
    return (
        <div className="dot-pagination">
            <button 
                onClick={() => setCurrentPage(currentPage - 1)} 
                disabled={currentPage === 1} 
                className="arrow"
            >
                {currentPage === 1 ? <TfiLayoutLineSolid className="line"/> : <SlArrowLeft />}
                
            </button>

            {pages.map((page, index) => (
                <button
                    key={index}
                    onClick={() => setCurrentPage(page)}
                    className={`page-dot ${page === currentPage ? "active" : ""}`}
                >
                </button>
            ))}

            <button 
                onClick={() => setCurrentPage(currentPage + 1)} 
                disabled={currentPage === pages.length} 
                className="arrow"
            >
                {currentPage === totalPosts ? <TfiLayoutLineSolid className="line"/>  :  <SlArrowRight />}
               
            </button>
        </div>
    );
};

export default DotPagination;