import React, {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import axios, {spread} from "axios";
import ReactPaginate from 'react-paginate';
import {toast} from "sonner";

import apiEndpoints from "../apiEndpoints";

import SportNews from "../components/sportPage/sportNews";
import LeagueBtn from "../components/sportPage/leagueBtn";
import DropDown from "../components/dropDown/dropDown";

function SportPage() {
    const {sportName} = useParams();
    const navigate = useNavigate();

    const location = useLocation();
    const stateData = location.state || {};
    const sports = stateData.sports;
    const sportId = stateData.sportId;

    const [readyToLoading, setReadyToLoading] = useState(false)

    const [rangeScale, setRangeScale] = useState(3)

    const [sportNews, setSportNews] = useState([]);

    const [currentLeagues, setCurrentLeagues] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const leaguesPerPage = 9;

    const [loading, setLoading] = useState(false);

    const [countryFilter, setCountryFilter] = useState('0');
    const [inputValue, setInputValue] = useState(' ');

    const [prevCountryFilter, setPrevCountryFilter] = useState('');
    const [prevInputValue, setPrevInputValue] = useState('');

    const [searchClicked, setSearchClicked] = useState();


    const handlePageClick = (event) => {
        const selectedPage = event.selected;
        setCurrentPage(selectedPage);
        getLeagues(selectedPage);
    };

    function handleSearchClick() {
        setSearchClicked((prev) => !prev);
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            handleSearchClick();
        }
    };

    const getLeagues = async (page) => {
        try {
            setLoading(true);

            console.log(sportId);
            console.log(inputValue);
            console.log(page);

            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.sports.getLeagueSearch}`,
                {
                    sport_id: sportId,
                    letter: inputValue,
                    page: page + 1,
                    per_page: leaguesPerPage
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            setCurrentLeagues(response.data);

            console.log(response.data)

            const totalPosts = response.data[0].count;

            console.log(response.data[0].count)
            setPageCount(Math.ceil(totalPosts / leaguesPerPage));

            setPrevCountryFilter(countryFilter);
            setPrevInputValue(inputValue);
        } catch (error) {
            setPrevCountryFilter('0');
            setPrevInputValue(' ');
            toast.error(`:( Troubles With Leagues Loading: ${error}`);
        }finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (Array.isArray(sports) && sports.length > 0) {

            if (!sports.find(item => item.sport === sportName)) {
                navigate("/not-existing");
            }

            setReadyToLoading(true);

        } else {
            navigate("/not-existing");
        }
    }, [sports, sportName]);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.news.getSport}${sportName}`)
            .then(res => {
                const returnedNews = res.data;
                setSportNews(returnedNews);
            })
            .catch(error => {
                toast.error(`:( Troubles With News Loading: ${error}`);
            });
    }, []);

    useEffect(() => {
        if(prevInputValue !== inputValue || prevCountryFilter !== countryFilter){
            getLeagues(currentPage);

        }
    }, [countryFilter, searchClicked]);

    return(
        <section className={"sportPage"}>

            <h1 className={"sportTitle"}>{ sportName }</h1>

            <section className={"news"}>

                {
                !(sportNews.length === 0) ?
                    sportNews.map((item, index) => (
                        <SportNews
                            key={index}
                            title={item.data?.title}
                            text={item.data?.timestamp}
                            sport={sportName}
                            img={item.data?.images[0]}
                            side={index%2 === 0 ? "right" : "left"}
                            id={item.blob_id}
                        />
                    ))
                    :
                    <div className={"noItems"}>
                        <h1>no {sportName} news were found :(</h1>
                    </div>
                }

            </section>

            <section className={"leaguesBlock"}>

                <section className={"leaguesFilter"}>

                    <div className={"leaguesSearch"}>

                        <input
                            type={"search"}
                            placeholder={" "}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyDown={handleKeyDown}
                        ></input>

                        <label>Search league</label>

                        <button onClick={handleSearchClick} disabled={loading}>
                            <i className="fa-solid fa-magnifying-glass"></i>
                        </button>

                    </div>

                    <DropDown
                        setCountry={setCountryFilter}
                    />

                </section>

                <section className={"iconsBlock"}>

                    {
                        !(currentLeagues.length === 0) ?
                        currentLeagues.map((item, index) => (
                        <LeagueBtn
                            key={index}
                            name={item?.name}
                            logo={item?.team?.logo || item?.logo}
                        /> ))
                        :
                        <div className={"noItems"}>
                            <h1>no leagues were found :(</h1>
                        </div>
                    }

                </section>

                <ReactPaginate
                    breakLabel="..."
                    nextLabel="→"
                    onPageChange={handlePageClick}
                    pageRangeDisplayed={rangeScale}
                    pageCount={pageCount}
                    previousLabel="←"
                    renderOnZeroPageCount={null}
                    activeClassName="activePaginationPane"
                    containerClassName="pagination"
                />

            </section>

        </section>
    );
}

export default SportPage;