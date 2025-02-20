import React, { useState } from 'react';
import { SlArrowDown, SlArrowUp } from "react-icons/sl";
import ReactPaginate from "react-paginate";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";

const GamesContainer = ({
    title,
    cardSizes,
    children,
    gridSize,
    postsPerPage,
    onGridSizeChange,
    pageCount,
    currentPage,
    onPageChange,
    loading,
    paginationKey,
}) => {
    const [isCollapsed, setIsCollapsed] = useState(false);
    return (
        <div className="game-container">

            <div className='title' onClick={() => setIsCollapsed(!isCollapsed)}>
                <button className='filled arrow'>
                    {isCollapsed ? <SlArrowDown /> : <SlArrowUp />}
                </button>
                <h1>{title}</h1>
            </div>

            {!isCollapsed && (
                <div className='games'>

                    {children}

                    <ReactPaginate
                        breakLabel="..."
                        nextLabel={currentPage === pageCount - 1 ? <TfiLayoutLineSolid className="line" /> : <SlArrowRight className="arrow" />}
                        previousLabel={currentPage === 0 ? <TfiLayoutLineSolid className="line" /> : <SlArrowLeft className="arrow" />}
                        onPageChange={onPageChange}
                        pageRangeDisplayed={3}
                        marginPagesDisplayed={1}
                        pageCount={3}
                        renderOnZeroPageCount={null}
                        activeClassName="activePaginationPane"
                        containerClassName="pagination-games"
                        pageLinkClassName="page-num"
                        previousLinkClassName="page-prev"
                        nextLinkClassName="page-next"
                        activeLinkClassName="page-active"
                        key={paginationKey}
                    />
                </div>)}
        </div>
    );
};


export default GamesContainer;