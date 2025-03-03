import React from 'react';

const GridRecommendationBlock = ({
   title,
   children,
   gridSize
}) => {
    return (
        <div className="grid-container">
            <div className="header">
                <h1>{title}</h1>
            </div>

            <hr />

            <div
                className="grid gap-4"
                style={{
                    gridTemplateColumns: `repeat(${gridSize.columns}, 1fr)`,
                    gridTemplateRows: `repeat(${gridSize.rows}, auto)`
                }}
            >
                {React.Children.map(children, (child) =>
                    React.cloneElement(child, { ...gridSize.cardSize })
                )}
            </div>
        </div>
    );
};


export default GridRecommendationBlock;