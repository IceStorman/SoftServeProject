import React, {useEffect, useState} from "react";
import ReactPaginate from "react-paginate";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import {toast} from "sonner";
import LeagueBtn from "../components/sportPage/leagueBtn";
import NoItems from "../components/NoItems";
import TeamsBtn from "../components/LeaguePage/teamsBtn";

function LeaguePage(){
    const { leagueName  } = useParams();

    const location = useLocation();
    const navigate = useNavigate();

    const [rangeScale ,setRangeScale]= useState(3)
    const stateData = location.state || {};
    const leagueId = stateData.leagueId;
    const sportId = stateData.sportId;

    const [currentTeams, setCurrentTeams] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [paginationKey, setPaginationKey] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const teamsPerPage = 9;


    const [loading, setLoading] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const [prevInputValue, setPrevInputValue] = useState('');
    const [searchClicked, setSearchClicked] = useState(false);


    const handlePageClick = (event) => {
        const selectedPage = event.selected;
        setCurrentPage(selectedPage);
        getTeams(selectedPage);
    };

    function handleSearchClick() {
        setSearchClicked((prev) => !prev);
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            handleSearchClick();
        }
    };
    const getTeams = async (page) => {

        setPrevInputValue(inputValue);

        try {
            setLoading(true);

            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.teams.getAll}`,
                {
                    teams__sport_id: sportId,
                    leagues__api_id: leagueId,
                    letter: inputValue,
                    page: page + 1,
                    per_page: teamsPerPage
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            setCurrentTeams(response.data.teams);
            console.log(response.data.teams);
            const totalPosts = response.data.count;
            setPageCount(Math.ceil(totalPosts / teamsPerPage));
        } catch (error) {
            setPageCount(0);
            toast.error(`:( Troubles With Leagues Loading: ${error}`);
        }
    };

    useEffect(() => {
        console.log("Sport ID:", sportId);
        console.log("League ID:", leagueId);
        if (!sportId || !leagueId) {
            toast.error("Missing sport or league ID.");
            navigate("/not-existing");
            return;
        }
        getTeams(0);
    }, [sportId, leagueName]);

    useEffect(() => {
        if(prevInputValue !== inputValue){
            handlePageClick({selected: 0});
            setPaginationKey((prevKey) => prevKey + 1);
        }
    }, [searchClicked]);

    useEffect(() => {
        (loading === false) ? setLoading(false) :
            (
                (currentTeams.length > 0) ? setLoading(false)
                    : setTimeout(() => {
                        setLoading(false);
                    }, 2000)
            )
    }, [loading]);



    return(
        <>
            <section className={"leaguePage"}>

                <h1 className={"sportTitle"}>{leagueName}</h1>

                <section className={"itemsPaginationBlock"}>

                    <section className={"filter"}>

                        <div className={"itemSearch"}>
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


                    </section>

                    <section className={"iconsBlock"}>

                        {
                            (currentTeams && currentTeams.length !== 0) ?
                                currentTeams.map((item, index) => (
                                    <TeamsBtn
                                        key={index}
                                        team_name={item?.team_name}
                                        logo={item?.logo}
                                        sportId={sportId}
                                    />))
                                : (loading === false) ?
                                    (<NoItems
                                        key={1}
                                        text={`No ${leagueName} teams were found`}
                                    />) : null
                        }

                    </section>

                    {pageCount > 1 && (
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
                    />)}

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

export default LeaguePage;