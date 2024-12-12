import React, {useEffect, useState} from "react";
import Team from "../components/sportPage/team";
import ReactPaginate from "react-paginate";
import {useParams} from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import {toast} from "sonner";

function League(){
    const { leagueName  } = useParams();

    const [rangeScale ,setRangeScale]= useState(3)

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
        axios.get(`${apiEndpoints.url}${apiEndpoints.team.getAll}`)
            .then(res => {
                let returnedTeams = res.data;
                res.data.forEach((league) =>{
                    if(league?.sport === leagueName) {
                        returnedTeams = league?.team
                        setTeams(returnedTeams);
                    }
                })
            })
            .catch(error => {
                toast.error(`:( Troubles With Teams Loading: ${error}`);
            });
    }, []);

    return(
        <>
            <section className={"sportTeams"}>

                {currentTeams.map((item, index) => (
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
        </>
    );
}

export default League;