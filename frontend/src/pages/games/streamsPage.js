import React, { useState, useEffect } from "react";
import img1 from "../imgs/1.jpg";
import img2 from "../imgs/2.jpg";
import FiltersRenderer from "../../components/filters/filterRender";
import GamesContainer from "../../components/containers/gamesContainer";
import StreamCard from "../../components/cards/streamCard";
import useTranslations from "../../translationsContext";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import { toast } from "sonner";
import { TfiLayoutLineSolid } from "react-icons/tfi";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import ReactPaginate from "react-paginate";
import useBurgerMenu from "../../customHooks/useBurgerMenu";
import globalVariables from "../../globalVariables";
import {FaFilter, FaTimes} from "react-icons/fa";
import useBurgerMenuState from "../../customHooks/useBurgerMenuState";


function StreamsPage() {
    const { t } = useTranslations();
    const [selectedModel, setSelectedModel] = useState("streams");
    const [filters, setFilters] = useState([]);
    const [currentStreams, setCurrentStreams] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const [inputValue, setInputValue] = useState('');
    const [prevInputValue, setPrevInputValue] = useState('');
    const burgerMenu = useBurgerMenu(`${globalVariables.windowSizeForBurger.streams}`);
    const initialIcon = <FaFilter size={28} />;
    const closeIcon = <FaTimes size={28} color="black" />;

    const { menuIsOpen, menuIcon, handleOpenMenu, handleCloseMenu } = useBurgerMenuState({
        menuSelector: ".filters-container",
        initialIcon: initialIcon,
        closeIcon: closeIcon,
    });

    const getStreams = async (page = 0) => {
        setPrevInputValue(inputValue);

        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.stream.getStreamsSearch}`,
                {
                    pagination: {
                        page: page + 1,
                        per_page: 10,
                    },
                    filters: filters
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            setCurrentStreams(response.data.items);
            setPageCount(Math.ceil(response.data.count / 10));
        } catch (error) {
            setPageCount(0);
            toast.error(`Troubles With Leagues Loading: ${error}`);
        }
    };

    useEffect(() => {
        getStreams(0);
    }, []);

    const handlePageClick = (event) => {
        const selectedPage = event.selected;
        setCurrentPage(selectedPage);
        getStreams(selectedPage);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    const handleFiltersChange = (newFilters) => {
        setFilters(newFilters);
    };

    const handleApplyFilters = () => {
        setCurrentPage(0);
        getStreams(0);
    };

    const filtersBlock = (
        <div className={`filters-container ${menuIsOpen ? "show" : ""}`}>
            <FiltersRenderer model={selectedModel} onFilterChange={handleFiltersChange} />
            <button onClick={handleApplyFilters}>{t("apply_filters")}</button>
        </div>
    )

    return (
        <div className="streams-page">
            {!burgerMenu ? filtersBlock : null}

            <div className="content">

                {burgerMenu  && (
                    <div className="filter-wrapper">
                        <button className={"menu-btn"} onClick={handleOpenMenu}>{menuIcon}</button>
                        {menuIsOpen && filtersBlock }
                    </div>
                )}

                {
                    currentStreams ?
                        <GamesContainer
                            streams={currentStreams}
                        /> : null
                }

                {pageCount > 1 && (
                    <ReactPaginate
                        breakLabel="..."
                        nextLabel={currentPage === pageCount - 1 ? <TfiLayoutLineSolid className="line"/> :
                            <SlArrowRight className="arrow"/>}
                        previousLabel={currentPage === 0 ? <TfiLayoutLineSolid className="line"/> :
                            <SlArrowLeft className="arrow"/>}
                        onPageChange={handlePageClick}
                        pageRangeDisplayed={3}
                        marginPagesDisplayed={1}
                        pageCount={pageCount}
                        renderOnZeroPageCount={null}
                        activeClassName="activePaginationPane"
                        containerClassName="pagination-games"
                        pageLinkClassName="page-num"
                        previousLinkClassName="page-prev"
                        nextLinkClassName="page-next"
                        activeLinkClassName="page-active"
                    />
                )}
            </div>
        </div>
    );
}

export default StreamsPage;
