import React, { useState, useEffect } from "react";
import axios from 'axios';

import { toast } from "sonner";
import NoItems from "../NoItems";
import NewsCard from "../cards/newsCard";
import DotPagination from "./dotPagination";

import '../../scss/pagination.scss'

function NewsBox({ testNews }) {
    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [postsPerPage, setPostsPerPage] = useState(1);

    const lastPostIndex = currentPage * postsPerPage;
    const firstPostIndex = lastPostIndex - postsPerPage;
    const currentPosts = testNews.slice(firstPostIndex, lastPostIndex);

    const element_height = 600
    const element_width = 500
    return (
        <div className="newsbox">
            {
                !(currentPosts.lenght === 0) ?
                    currentPosts.map((item, index) => (
                        <NewsCard
                            title={item.title}
                            date={item.date}
                            img={item.img}
                            sport={item.sport}
                            content={item.content}
                            height={element_height}
                            width={element_width}
                            isFoil={true}
                        />
                    ))
                    : (loading === false) ?
                        (
                            <NoItems
                                key={1}
                                text={"No latest news were found"}
                            />
                        ) : null
            }
            <DotPagination
                totalPosts={5}
                postsPerPage={postsPerPage}
                setCurrentPage={setCurrentPage}
                currentPage={currentPage}
            ></DotPagination>
        </div>
    );
}

export default NewsBox;