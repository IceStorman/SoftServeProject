import React from "react";

function SearchWithFilter({
      setSearchClicked,
      inputValue,
      setInputValue,
      loading,
      placeholder = " ",
      additionalComponent = null
  })
{

    function handleSearchClick() {
        setSearchClicked((prev) => !prev);
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            handleSearchClick();
        }
    };


    return (

        <section className={"filter"}>
            <div className={"itemSearch"}>
                <input
                    type={"search"}
                    placeholder={" "}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                />
                <label>{placeholder}</label>

                <button onClick={handleSearchClick} disabled={loading}>
                    <i className="fa-solid fa-magnifying-glass"></i>
                </button>
            </div>

            {additionalComponent && additionalComponent}
        </section>
    );
}

export default SearchWithFilter;
