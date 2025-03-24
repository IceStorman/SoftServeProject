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

function StreamsPage() {
    const { t } = useTranslations();
    const [selectedModel, setSelectedModel] = useState("streams");
    const [filters, setFilters] = useState([]);
    const [currentStreams, setCurrentStreams] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const [inputValue, setInputValue] = useState('');
    const [prevInputValue, setPrevInputValue] = useState('');

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

    return (
        <div className="streams-page">
            <div className="filters-container">
                <FiltersRenderer model={selectedModel} onFilterChange={handleFiltersChange} />
                <button onClick={handleApplyFilters}>{t("apply_filters")}</button>
            </div>

            <div className="content">

                {
                    currentStreams ?
                    <GamesContainer
                        streams={currentStreams}
                    /> : null
                }

                {pageCount > 1 && (
                    <ReactPaginate
                        breakLabel="..."
                        nextLabel={currentPage === pageCount - 1 ? <TfiLayoutLineSolid className="line" /> : <SlArrowRight className="arrow" />}
                        previousLabel={currentPage === 0 ? <TfiLayoutLineSolid className="line" /> : <SlArrowLeft className="arrow" />}
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
