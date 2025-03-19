import React from "react";

export const NameFilter = ({ onChange }) => (
    <div className="filter-search">
        <input type="text" placeholder="Search..." onChange={onChange}/>
    </div>
);