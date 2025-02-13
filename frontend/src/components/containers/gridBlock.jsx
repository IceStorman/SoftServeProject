import React, { useState } from 'react';
import { RiFunctionFill, RiGridFill, RiListCheck2 } from "react-icons/ri";
import { GoSortAsc, GoSortDesc } from "react-icons/go";
import ReactPaginate from "react-paginate";
import CustomSelect from './customSelect';
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";


const GridContainer = ({
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
    const [sortBy, setSortBy] = useState("popularity");
    const [sortOrder, setSortOrder] = useState("asc");
    const [selectedGrid, setSelectedGrid] = useState('large');
    const options = [
        { value: "short", label: "Date" },
        { value: "medium", label: "Popularity" },
        { value: "long", label: "This is a very long option" }
    ];

    return (
        <div className="grid-container">
            <div className="header">
                <h1>{title}</h1>

                <div className="sorting-controls">
                    <p>Sort by: </p>
                    <CustomSelect options={options} maxWidth={300} />

                    <button onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}>
                        {sortOrder === "asc" ? <GoSortAsc /> : <GoSortDesc />}
                    </button>
                </div>

                <div className="controls">
                    <button onClick={() => [onGridSizeChange('large'), setSelectedGrid('large')]} 
                        className={selectedGrid === 'large' ? 'selected' : ''}><RiFunctionFill /></button>
                    <button onClick={() => [onGridSizeChange('medium'), setSelectedGrid('medium')]}
                        className={selectedGrid === 'medium' ? 'selected' : ''}><RiGridFill /></button>
                    <button onClick={() => [onGridSizeChange('small'), setSelectedGrid('small')]}
                        className={selectedGrid === 'small' ? 'selected' : ''}><RiListCheck2 /></button>
                </div>
            </div>

            <hr />

            <div
                className="grid gap-4"
                style={{
                    gridTemplateColumns: `repeat(${gridSize.columns}, 1fr)`,
                    gridTemplateRows: `repeat(${gridSize.rows}, auto)`
                }}
            >
                {React.Children.map(children, (child) =>
                    React.cloneElement(child, { ...gridSize.cardSize })
                )}
            </div>
            <hr />
            <ReactPaginate
                breakLabel="..."
                nextLabel={currentPage === pageCount ? <TfiLayoutLineSolid className="line"/>  :  <SlArrowRight />}
                previousLabel={currentPage === 1 ? <TfiLayoutLineSolid className="line"/> : <SlArrowLeft />}
                onPageChange={onPageChange}
                pageRangeDisplayed={3}
                marginPagesDisplayed={1}
                pageCount={pageCount}
                renderOnZeroPageCount={null}
                activeClassName="activePaginationPane"
                containerClassName="pagination"
                pageLinkClassName="page-num"
                previousLinkClassName="page-prev"
                nextLinkClassName="page-next"
                activeLinkClassName="page-active"
                key={paginationKey}
            />
        </div>
    );
};


export default GridContainer;