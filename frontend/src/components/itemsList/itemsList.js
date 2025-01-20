import React from "react";
import ReactPaginate from "react-paginate";
import NoItems from "../NoItems";

const ItemList = ({
      items,
      renderItem,
      noItemsText,
      pageCount,
      onPageChange,
      rangeScale,
      loading,
      paginationKey,
  }) => {

    return (
        <section className="iconsBlock">
            {
                (items && items.length !== 0) ? (
                    items.map((item, index) => renderItem(item, index))
                ) : (!loading) ? (
                    <NoItems
                        key={1}
                        text={noItemsText}
                    />
                ) : null
            }
            {pageCount > 1 && (
                <ReactPaginate
                    key={paginationKey}
                    breakLabel="..."
                    nextLabel="→"
                    onPageChange={onPageChange}
                    pageRangeDisplayed={rangeScale}
                    pageCount={pageCount}
                    previousLabel="←"
                    renderOnZeroPageCount={null}
                    activeClassName="activePaginationPane"
                    containerClassName="pagination"
                />
            )}
        </section>
    );
};

export default ItemList;
