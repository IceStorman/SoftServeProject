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
    const sportId = stateData.sportId;


    const [sports, setSport] = useState([]);

    const [rangeScale, setRangeScale] = useState(3)

    const [sportNews, setSportNews] = useState([]);

    const [currentLeagues, setCurrentLeagues] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [paginationKey, setPaginationKey] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const leaguesPerPage = 9;

    const [loading, setLoading] = useState(false);

    const [countryFilter, setCountryFilter] = useState(0);
    const [inputValue, setInputValue] = useState('');

    const [prevCountryFilter, setPrevCountryFilter] = useState();
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

        setPrevCountryFilter(countryFilter);
        setPrevInputValue(inputValue);

        try {
            setLoading(true);

            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.sports.getLeagueSearch}`,
                {
                    sport_id: sportId,
                    country_id: parseInt(countryFilter),
                    letter: inputValue ? inputValue : ' ',
                    page: page + 1,
                    per_page: leaguesPerPage
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            setCurrentLeagues(response.data);
            const totalPosts = response.data[0].count;
            setPageCount(Math.ceil(totalPosts / leaguesPerPage));
        } catch (error) {
            setPageCount(0);
            toast.error(`:( Troubles With Leagues Loading: ${error}`);
        }
    };

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
            handlePageClick({selected: 0});
            setPaginationKey((prevKey) => prevKey + 1);
        }
    }, [countryFilter, searchClicked]);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.sports.getAll}`)
        .then(res => {
            const returnedSports = res.data;

            if (returnedSports.length > 0) {

                if ((returnedSports.find(item => item.sport === sportName) === undefined) || returnedSports.find(item => item.sport === sportName).sport !== sportName) {
                    navigate("/not-existing");
                }

            } else {
                navigate("/not-existing");
            }

            setSport(returnedSports);
        })
        .catch(error => {
            toast.error(`:( Troubles With Sports Loading: ${error}`);
        });

    }, [sportName]);

    useEffect(() => {
        (loading === false) ? setLoading(false) :
        (
            (sportNews.length > 0 || currentLeagues.length > 0) ? setLoading(false)
                : setTimeout(() => {
                    setLoading(false);
                }, 2000)
        )
    }, [sportNews.length, currentLeagues.length, loading]);

    return(
        <>

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
                            : (loading === false) ?
                                (
                                    <div className={"noItems"}>
                                        <h1>no {sportName} news were found :(</h1>
                                    </div>
                                ) : null
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
                        key={paginationKey}
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

            {loading === true ?
                (
                    <>
                        <div className={"loader-background"}></div>
                        <div className="loader"></div>
                    </>
                ) : null
            }
        </>
    );
}

export default SportPage;