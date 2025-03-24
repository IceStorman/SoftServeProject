import React, {useEffect, useRef, useState} from "react";
import { RiFunctionFill, RiGridFill, RiListCheck2 } from "react-icons/ri";
import ReactPaginate from "react-paginate";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";
import FiltersRenderer from "../filters/filterRender";
import useTranslations from "../../translationsContext";
import NoItems from "../NoItems";
import {FaFilter} from "react-icons/fa";


const SearchBlock = ({
    children,
    gridSize,
    postsPerPage,
    onGridSizeChange,
    pageCount,
    currentPage,
    onPageChange,
    paginationKey,
    handleOpenMenu,
    menuIcon,
    setMenuIcon,
    burgerMenu,
    menuIsOpen,
    selectedModel,
    handleFiltersChange,
    sportId,
    handleApplyFilters,
    count,
    setMenuIsOpen
}) => {

    const initialIcon = <FaFilter size={28} />

    const [selectedGrid, setSelectedGrid] = useState('large');
    const { t } = useTranslations();
    const filterRef = useRef(null);

    const handleClickOutside = (event) => {
        if (filterRef.current && !filterRef.current.contains(event.target)) {
            setMenuIsOpen(false);
            setMenuIcon(initialIcon);
        }
    };

    useEffect(() => {
        if (menuIsOpen) {
            document.addEventListener("mousedown", handleClickOutside);
        } else {
            document.removeEventListener("mousedown", handleClickOutside);
        }

        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [menuIsOpen]);

    return (
        <div className="search-container">
            <header className="header">
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
                                    <button onClick={handleApplyFilters}>{t("apply_filters")}</button>
                                </div>
                            </div>
                        )}
                    </div>
                )}

                <div className="controls">
                    <button onClick={() => [onGridSizeChange('large'), setSelectedGrid('large')]}
                            className={selectedGrid === 'large' ? 'selected' : ''}><RiFunctionFill/></button>
                    <button onClick={() => [onGridSizeChange('medium'), setSelectedGrid('medium')]}
                            className={selectedGrid === 'medium' ? 'selected' : ''}><RiGridFill/></button>
                    <button onClick={() => [onGridSizeChange('small'), setSelectedGrid('small')]}
                            className={selectedGrid === 'small' ? 'selected' : ''}><RiListCheck2/></button>
                </div>
            </header>

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
                : <NoItems text='No leagues were found'/>
            }
        </div>
    );
}

export default SearchBlock;