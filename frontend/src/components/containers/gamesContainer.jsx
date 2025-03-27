import React, { useState } from 'react';
import { SlArrowDown, SlArrowUp } from "react-icons/sl";
import ReactPaginate from "react-paginate";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";
import StreamCard from "../cards/streamCard";

const GamesContainer = ({
    streams
}) => {

    return (
        <div className="game-container">

            <div className='games'>

                {streams?.length > 0 ? streams.map((item) => (
                    <StreamCard
                        key={item?.id}
                        stream={item}
                    />
                )) : <p>No streams available</p>}

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
                        pageCount={pageCount}
                        forcePage={currentPage}
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