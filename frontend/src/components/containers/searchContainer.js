import React, { useEffect, useRef, useState } from "react";
import ReactPaginate from "react-paginate";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";
import FiltersRenderer from "../filters/filterRender";
import useTranslations from "../../translationsContext";
import NoItems from "../NoItems";
import {FaFilter, FaTimes} from "react-icons/fa";
import useBurgerMenuState from "../../customHooks/useBurgerMenuState";


const SearchContainer = ({
                         children,
                         gridSize,
                         pageCount,
                         currentPage,
                         onPageChange,
                         paginationKey,
                         burgerMenu,
                         selectedModel,
                         handleFiltersChange,
                         sportId,
                         handleApplyFilters,
                         count
                     }) => {
    const { t } = useTranslations();
    const filterRef = useRef(null);

    const { menuIsOpen, menuIcon, handleOpenMenu, handleCloseMenu } = useBurgerMenuState({
        initialIcon: <FaFilter size={28} />,
        closeIcon: <FaTimes size={28} color="black" />,
        menuSelector: ".burger-filter",
        buttonSelector: ".menu-btn"
    });

    return (
        <div className="search-container">
            <section className="header">
                {burgerMenu  && (
                    <div className="filter-wrapper" ref={filterRef}>
                        <button className="menu-btn" onClick={handleOpenMenu}>
                            {menuIcon}
                        </button>
                        { menuIsOpen && (
                            <div className={` burger-filter ${menuIsOpen ? "show" : ""}`}>
                                <div className="filters-container">
                                    <FiltersRenderer model={selectedModel} onFilterChange={handleFiltersChange}
                                                     sportId={sportId}/>
                                    <button onClick={() => { handleApplyFilters(); handleCloseMenu(); }}>
                                        {t("apply_filters")}
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </section>

            <hr/>

            { !(count === 0) ?
                <>
                    <div
                        className="grid gap-4"
                        style={{
                            gridTemplateColumns: `repeat(${gridSize.columns}, 1fr)`,
                            gridTemplateRows: `repeat(${gridSize.rows}, auto)`
                        }}
                    >
                        {React.Children.map(children, (child) =>
                            React.cloneElement(child, {...gridSize.cardSize})
                        )}
                    </div>
                    <hr/>
                    <ReactPaginate
                        breakLabel="..."
                        nextLabel={currentPage === pageCount - 1 ? <TfiLayoutLineSolid className="line"/> :
                            <SlArrowRight className="arrow"/>}
                        previousLabel={currentPage === 0 ? <TfiLayoutLineSolid className="line"/> :
                            <SlArrowLeft className="arrow"/>}
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
                </>
                : <NoItems text={`No ${selectedModel} were found`}/>
            }
        </div>
    );
}

export default SearchContainer;