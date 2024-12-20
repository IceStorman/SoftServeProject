import React, {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import axios from "axios";
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
    const sports = location.state || {};

    const [readyToLoading, setReadyToLoading] = useState(false)

    const [rangeScale, setRangeScale] = useState(3)

    const [sportNews, setSportNews] = useState([]);
    const [leagues, setLeagues] = useState([]);

    const [currentLeagues, setCurrentLeagues] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const leaguesPerPage = 9;

    const [leaguesOffset, setLeaguesOffset] = useState(0);

    const [countryFilter, setCountryFilter] = useState("All");
    const [inputValue, setInputValue] = useState('');
    const [searchClicked, setSearchClicked] = useState();

    useEffect(() => {
        const endOffset = leaguesOffset + leaguesPerPage;
        setCurrentLeagues(leagues.slice(leaguesOffset, endOffset));
        setPageCount(Math.ceil(leagues.length / leaguesPerPage));
    }, [leaguesOffset, leagues]);

    const handlePageClick = (event) => {
        const newOffset = (event.selected * leaguesPerPage) % leagues.length;
        setLeaguesOffset(newOffset);
    };

    function handleSearchClick() {
        setSearchClicked((prev) => !prev);
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            handleSearchClick();
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
        axios.get(`${apiEndpoints.url}${apiEndpoints.team.getAll}`)
            .then(res => {
                let returnedTeams = res.data;
                res.data.forEach((sport) =>{
                    if(sport?.sport === sportName) {
                        returnedTeams = sport?.team
                        setLeagues(returnedTeams);
                    }
                })
            })
            .catch(error => {
                toast.error(`:( Troubles With Leagues Loading: ${error}`);
            });
    }, []);

    useEffect(() => {
        console.log(countryFilter);
        console.log(inputValue);
    }, [countryFilter, searchClicked]);

    return(
        <section className={"sportPage"}>

            <h1 className={"sportTitle"}>{ sportName }</h1>

            <section className={"news"}>

                {sportNews.map((item, index) => (

                    <SportNews
                        key={index}
                        title={item.data?.title}
                        text={item.data?.timestamp}
                        sport={sportName}
                        img={item.data?.images[0]}
                        side={index%2 === 0 ? "right" : "left"}
                        id={item.blob_id}
                    />

                ))}

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

                        <button onClick={handleSearchClick}>
                            <i className="fa-solid fa-magnifying-glass"></i>
                        </button>

                    </div>

                    <DropDown
                        setCountry={setCountryFilter}
                    />

                </section>

                <section className={"iconsBlock"}>

                    {
                        !(leagues.length === 0) ?
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