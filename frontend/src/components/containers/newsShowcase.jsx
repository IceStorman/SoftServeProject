import React, { useState } from "react";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";
import NoItems from "../NoItems";
import NewsCard from "../cards/newsCard";
import ReactPaginate from "react-paginate";

import '../../scss/pagination.scss'

function NewsShowcase({ newsData }) {
    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);

    const postsPerPage = 1;
    const pageCount = Math.ceil(newsData.length / postsPerPage);
    // const element_height = 600;
    // const element_width = 500;

    const handlePageChange = ({ selected }) => {
        setCurrentPage(selected + 1);
    };


    return (
        <div className="newsbox">
            {newsData.length > 0 ? (
                <NewsCard
                    title={newsData[currentPage - 1]?.data?.title}
                    date={newsData[currentPage - 1]?.data?.timestamp}
                    img={newsData[currentPage - 1]?.data?.images[0] || null}
                    sport={newsData[currentPage - 1]?.data?.S_P_O_R_T}
                    content={newsData[currentPage - 1]?.data?.article?.section_1?.content}
                    id={newsData[currentPage - 1]?.blob_id}
                    article={newsData[currentPage - 1]?.data}
                    // height={element_height}//Нахуя?
                    // width={element_width}//Нахуя?
                    isFoil={true}
                />
            ) : !loading ? (
                <NoItems key={1} text={"No latest news were found"} />
            ) : null}

            <ReactPaginate
                breakLabel="..."
                nextLabel={currentPage === pageCount ? (<TfiLayoutLineSolid className="line" />) : (<SlArrowRight className="arrow" />)}
                previousLabel={currentPage === 1 ? (<TfiLayoutLineSolid className="line" />) : (<SlArrowLeft className="arrow" />)}
                onPageChange={handlePageChange}
                pageRangeDisplayed={1}
                marginPagesDisplayed={5}
                pageCount={pageCount}
                forcePage={currentPage - 1}
                renderOnZeroPageCount={null}
                activeClassName="activePaginationPane"
                containerClassName="dot-pagination"
                pageLinkClassName="page-dot"
                previousLinkClassName="arrow"
                nextLinkClassName="arrow"
                activeLinkClassName="active"
            />
        </div>
    );
}

export default NewsShowcase;