import React, { useEffect, useState } from "react";
import { NavLink, Link } from "react-router-dom";
import axios from "axios";
import { toast } from "sonner";

import apiEndpoints from "../../apiEndpoints";

import NoItems from "../../components/NoItems";

function SportPage() {
    const [loading, setLoading] = useState(false);
    const [sports, setSport] = useState([]);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.sports.getAll}`)
            .then(res => {
                const returnedSports = res.data;
                setSport(returnedSports);
            })
            .catch(error => {
                toast.error(`Troubles With Sports Loading: ${error}`);
            });
    }, []);

    const amountOfColumns = 4
    const overflow = sports.length % amountOfColumns

    return (
        <>
            {
                !(sports.length === 0) ?
                    <section className={"sportPage"}>

                        <h1>Select sport</h1>
                        <div className={`sport-selection-grid overflow-${overflow}`}>
                            {
                                sports.map((item) => (
                                    <Link className="button-link" to={`${item.sport}`} key={item.sport} state={{ sportId: item.id }}>
                                        <button>{item.sport}</button>
                                    </Link>
                                ))
                            }
                        </div>
                    </section> : <NoItems text='No sports were found' />
            }
        </>
    );
}

export default SportPage;