import React, {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import axios from "axios";
import ReactPaginate from 'react-paginate';
import {toast} from "sonner";

import apiEndpoints from "../apiEndpoints";

import SportNews from "../components/sportPage/sportNews";
import LeagueBtn from "../components/sportPage/leagueBtn";
import DropDown from "../components/dropDown/dropDown";
import ItemList from "../components/itemsList/itemsList";
import NoItems from "../components/NoItems";
import SearchWithFilter from "../components/searchFilter/searchFilterBtn";


function SportPage() {
    const {sportName} = useParams();
    const navigate = useNavigate();

    const location = useLocation();
    const stateData = location.state || {};
    const sportId = stateData.sportId;

    const [rangeScale, setRangeScale] = useState(3)

    const [sportNews, setSportNews] = useState([]);

    const [currentLeagues, setCurrentLeagues] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [paginationKey, setPaginationKey] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const leaguesPerPage = 9;

    const [loading, setLoading] = useState(false);

    const [countryFilter, setCountryFilter] = useState();
    const [inputValue, setInputValue] = useState('');

    const [prevCountryFilter, setPrevCountryFilter] = useState(0);
    const [prevInputValue, setPrevInputValue] = useState('');

    const [searchClicked, setSearchClicked] = useState(false);


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
                    leagues__sport_id: sportId,
                    countries__country_id: parseInt(countryFilter),
                    letter: inputValue,
                    page: page + 1,
                    per_page: leaguesPerPage
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            setCurrentLeagues(response.data.leagues);
            const totalPosts = response.data.count;
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
        })
        .catch(error => {
            toast.error(`:( Troubles With Sports Loading: ${error}`);
        });

    }, [sportName]);

    useEffect(() => {
        if(prevInputValue !== inputValue || prevCountryFilter !== countryFilter){
            handlePageClick({selected: 0});
            setPaginationKey((prevKey) => prevKey + 1);
        }
    }, [countryFilter, searchClicked]);

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

                <h1 className={"sportTitle"}>{sportName}</h1>

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
                                    side={index % 2 === 0 ? "right" : "left"}
                                    id={item.blob_id}
                                />
                            ))
                            : (loading === false) ?
                                (
                                    <NoItems
                                        key={1}
                                        text={`No ${sportName} news were found`}
                                    />
                                ) : null
                    }

                </section>

                <section className={"itemsPaginationBlock"}>

                    <SearchWithFilter
                        setInputValue={setInputValue}
                        loading={loading}
                        placeholder={"Search league"}
                        additionalComponent={
                            <DropDown setCountry={setCountryFilter} />
                        }
                    />

                    <ItemList
                        items={currentLeagues}
                        renderItem={(item, index) => (
                            <LeagueBtn
                                key={index}
                                leagueName={item?.name}
                                leagueId={item?.id}
                                sportId={item?.sport}
                                logo={item?.logo}
                            />
                        )}
                        noItemsText={`No ${sportName} leagues were found`}
                        pageCount={pageCount}
                        onPageChange={handlePageClick}
                        rangeScale={rangeScale}
                        loading={loading}
                        paginationKey={paginationKey}
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