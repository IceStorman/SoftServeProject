import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import SportNews from "../components/sportPage/sportNews";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import Team from "../components/sportPage/team";
import ReactPaginate from 'react-paginate';

function SportPage(){
    const { sportName  } = useParams();

    const [sportNews, setSportNews] = useState([]);
    const [teams, setTeams] = useState([]);

    const [currentTeams, setCurrentTeams] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const teemsPerPage = 9;

    const [teamOffset, setTeamOffset] = useState(0);

    useEffect(() => {
        const endOffset = teamOffset + teemsPerPage;
        setCurrentTeams(teams.slice(teamOffset, endOffset));
        setPageCount(Math.ceil(teams.length / teemsPerPage));
    }, [teamOffset, teams]);

    const handlePageClick = (event) => {
        const newOffset = (event.selected * teemsPerPage) % teams.length;
        setTeamOffset(newOffset);
    };


    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.news.getSport}${sportName}`)
            .then(res => {
                const returnedNews = res.data;
                setSportNews(returnedNews);
            })
            .catch(error => {
                console.error('There was an error getting news:', error);
            });
    }, []);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.team.getAll}`)
            .then(res => {
                let returnedTeams = res.data;
                res.data.forEach((sport) =>{
                    if(sport?.sport === sportName) {
                        returnedTeams = sport?.team
                        setTeams(returnedTeams);
                    }
                })
            })
            .catch(error => {
                console.error('There was an error getting teams:', error);
            });
    }, []);

    return(
        <section className={"sportPage"}>

            <h1 className={"sportTitle"}>{ sportName }</h1>

            <section className={"sportNews"}>

                {sportNews.map((item, index) => (

                    <SportNews
                        key={index}
                        title={item.data?.title}
                        text={item.data?.timestamp}
                        sport={sportName}
                        img={item.data?.images[0]}
                        side={index%2 === 0 ? "right" : "left"}
                    />

                ))}

            </section>

            <section className={"sportTeams"}>

                {currentTeams.map((item, index) =>(
                    <Team
                        key={index}
                        name={item?.name}
                        logo={item?.team?.logo || item?.logo}
                    />
                ))}

            </section>

            <ReactPaginate
                breakLabel="..."
                nextLabel="→"
                onPageChange={handlePageClick}
                pageRangeDisplayed={3}
                pageCount={pageCount}
                previousLabel="←"
                renderOnZeroPageCount={null}
                activeClassName="activePaginationPane"
                containerClassName="pagination"
            />

        </section>
    );
}

export default SportPage;