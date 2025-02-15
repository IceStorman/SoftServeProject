import React from "react";

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