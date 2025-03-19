import React from "react";

export const NameFilter = ({ onChange }) => (
    <div className="filterSearch">
        <input type="text" placeholder="Search by name..." onChange={onChange}/>
    </div>
);