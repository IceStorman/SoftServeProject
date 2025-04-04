import React, {useEffect, useState} from 'react';
import { RiFunctionFill, RiGridFill, RiListCheck2 } from "react-icons/ri";
import { GoSortAsc, GoSortDesc } from "react-icons/go";
import ReactPaginate from "react-paginate";
import CustomSelect from './customSelect';
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";
import useTranslations from "../../translationsContext";
import useBurgerMenu from '../../customHooks/useBurgerMenu';
import globalVariables from '../../globalVariables';


const GridContainer = ({
    title,
    children,
    gridSize,
    onGridSizeChange,
    pageCount,
    currentPage,
    onPageChange,
    setSortValue
}) => {
    const noThirdButton = useBurgerMenu(1024);
    const noSecondButton = useBurgerMenu(768);
    const { t } = useTranslations();
    const [sortBy, setSortBy] = useState("popularity");
    const [sortOrder, setSortOrder] = useState("desc");
    const [selectedGrid, setSelectedGrid] = useState('large');
    const options = [
        { value: "short", label: "Date" }
    ];

    useEffect(() => {
        setSortValue(sortOrder)
    }, [sortOrder]);

    return (
        <div className="grid-container">
            <div className="header">
                <h1>{title}</h1>

                <div className="sorting-controls">
                    <p>{t("sort")}</p>
                    <CustomSelect options={options} maxWidth={300} />

                    <button onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}>
                        {sortOrder === "asc" ? <GoSortAsc /> : <GoSortDesc />}
                    </button>
                </div>

                <div className="controls">
                    <button onClick={() => [onGridSizeChange('large'), setSelectedGrid('large')]} 
                        className={selectedGrid === 'large' ? 'selected' : ''}><RiFunctionFill /></button>
                    {!noSecondButton && (
                    <button onClick={() => [onGridSizeChange('medium'), setSelectedGrid('medium')]}
                        className={selectedGrid === 'medium' ? 'selected' : ''}><RiGridFill /></button>
                    )}
                    {!noThirdButton && (
                        <button onClick={() => [onGridSizeChange('small'), setSelectedGrid('small')]}
                            className={selectedGrid === 'small' ? 'selected' : ''}>
                            <RiListCheck2 />
                        </button>
                    )}
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
                forcePage={currentPage}
                breakLabel="..."
                nextLabel={currentPage + 1 >= pageCount ? <TfiLayoutLineSolid className="line"/> : <SlArrowRight />}
                previousLabel={currentPage === 0 ? <TfiLayoutLineSolid className="line"/> : <SlArrowLeft />}
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
            />
        </div>
    );
};


export default GridContainer;