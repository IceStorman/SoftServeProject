import React, {useEffect, useState} from "react";
import ReactPaginate from "react-paginate";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import {toast} from "sonner";
import LeagueBtn from "../components/sportPage/leagueBtn";
import ItemList from "../components/itemsList/itemsList";
import TeamsBtn from "../components/LeaguePage/teamsBtn";
import SearchWithFilter from "../components/searchFilter/searchFilterBtn";
import Slider from "../components/games/slider.js";

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

    const [games, setGames] = useState([]);

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
        const requestData = { 
            games__league_id: leagueId,
        };

        axios.post(`${apiEndpoints.url}${apiEndpoints.games.getGames}`, requestData)
            .then(res => {
                const returnedGames = res.data;
                setGames(returnedGames);
            })
            .catch(error => {
                toast.error(`:( Troubles With Games Loading: ${error}`);
            });
    }, []);


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

            <Slider games={games}/>

                <h1 className={"sportTitle"}>{leagueName}</h1>

                <section className={"itemsPaginationBlock"}>

                    <SearchWithFilter
                        setInputValue={setInputValue}
                        loading={loading}
                        placeholder="Search teams"
                    />

                    <ItemList
                        items={currentTeams}
                        renderItem={(item, index) => (
                            <TeamsBtn
                                key={index}
                                team_name={item?.team_name}
                                logo={item?.logo}
                                sportId={sportId}
                            />
                        )}
                        noItemsText={`No ${leagueName} teams were found`}
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

export default LeaguePage;