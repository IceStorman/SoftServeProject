import React, { useState } from "react";
import { RiFunctionFill, RiGridFill, RiListCheck2 } from "react-icons/ri";
import ReactPaginate from "react-paginate";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";


const SearchBlock = ({
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
    const [inputValue, setInputValue] = useState('');

    const handleChange = (event) => {
        setInputValue(event.target.value);
    };

    const [selectedGrid, setSelectedGrid] = useState('large');
    return (
        <div className="search-container">
            <div className="header">
                <input
                    type="text"
                    value={inputValue}
                    onChange={handleChange}
                    placeholder="Search..."
                    className="input-field"
                ></input>

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
                nextLabel={currentPage === pageCount-1 ? <TfiLayoutLineSolid className="line"/>  :  <SlArrowRight className="arrow" />}
                previousLabel={currentPage === 0 ? <TfiLayoutLineSolid className="line"/> : <SlArrowLeft className="arrow"/>}
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
}

export default SearchBlock;