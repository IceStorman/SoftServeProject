import React, { Children, useState } from "react";

import NewsCard from "../cards/newsCard"
import NoItems from "../NoItems";


function Column({ children }) {
    return (
        <div >
            {React.Children.toArray(children).map((child, index, array) => (
                <div key={index}>
                    {child}
                    {index < array.length - 1 && <hr />}
                </div>
            ))}
            
        </div>
    );
}


export default Column;