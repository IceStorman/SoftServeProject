import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import SportNews from "../components/sportPage/sportNews";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import Team from "../components/sportPage/team";
import ReactPaginate from 'react-paginate';
import {toast, Toaster} from "sonner";
import {Link} from "react-router-dom";


function SportPage(){
    const { sportName  } = useParams();

    const [rangeScale ,setRangeScale]= useState(3)

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
                        setTeams(returnedTeams);
                    }
                })
            })
            .catch(error => {
                toast.error(`:( Troubles With Teams Loading: ${error}`);
            });
    }, []);

    return(
        <section className={"sportPage"}>

            <Toaster  position="top-center" expand={true} richColors  />

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
                pageRangeDisplayed={rangeScale}
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