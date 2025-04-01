import React, { useState, useEffect } from "react";
import FiltersRenderer from "../../components/filters/filterRender";
import useTranslations from "../../translationsContext";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import { toast } from "sonner";
import useBurgerMenu from "../../customHooks/useBurgerMenu";
import globalVariables from "../../globalVariables";
import { FaFilter, FaTimes } from "react-icons/fa";
import useBurgerMenuState from "../../customHooks/useBurgerMenuState";
import SearchBlock from "../../components/containers/searchBlock";
import StreamCard from "../../components/cards/streamCard";
import LeagueCard from "../../components/cards/leagueCard";
import TeamCard from "../../components/cards/teamCard";
import NewsCard from "../../components/cards/newsCard";
import GameCard from "../../components/cards/gameCard";

function SearchPage() {
    const { t } = useTranslations();
    const [selectedModel, setSelectedModel] = useState("leagues");
    const [filters, setFilters] = useState([]);
    const [currentItems, setCurrentItems] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const burgerMenu = useBurgerMenu(globalVariables.windowSizeForBurger.streams);
    const [sportId, setSportId] = useState(null);
    const [leagueId, setLeagueId] = useState(null);
    const [inputValue, setInputValue] = useState(""); 
    const [prevInputValue, setPrevInputValue] = useState("");
    const [openFilterModel, setOpenFilterModel] = useState(null);

    const { menuIsOpen, menuIcon, handleOpenMenu, handleCloseMenu } = useBurgerMenuState({
        menuSelector: ".filters-container",
        buttonSelector: ".menu-btn",
        initialIcon: <FaFilter size={28} />, 
        closeIcon: <FaTimes size={28} color="black" />,
    });

    const componentMap = (type, item) => {
        const componentsCard = {
            streams: <StreamCard key={`${type}-${item.id}`} stream={item}/>,

            leagues: <LeagueCard
                    key={`${type}-${item.id}`}
                    leagueName={item.name}
                    img={item.logo}
                    id={item.id}
                    sportId={sportId}
                    />,

            teams:  <TeamCard
                    key={`${type}-${item.id}`}
                    leagueName={item.team_name}
                    img={item.logo}
                    sportId={item.sport_id}
                    id={item.id}
                    />,

            news:   <NewsCard
                    key={`${type}-${item.id}`}
                    title={item?.data?.title}
                    date={item?.data?.timestamp}
                    img={item?.data?.images || null}
                    content={item?.data?.article?.section_1?.content}
                    id={item?.blob_id}
                    article={item?.data?.article}
                    />,

            games: <GameCard
                    key={`${type}-${item.id}`}
                    nameHome={item.home_team_name}
                    nameAway={item.away_team_name}
                    logoHome={item.home_team_logo}
                    logoAway={item.away_team_logo}
                    scoreHome={item.home_score}
                    scoreAway={item.away_score}
                    time={item.time}
                    isVertical={true}
        />
        }
        
        return componentsCard[type] || null;
    };

    const fetchData = async (model, page = 0) => {
        setCurrentItems([]);
        setPrevInputValue(inputValue);
    
        let filtersData = [...filters];
    
        if (sportId) {
            filtersData.push({ filter_name: "sport_id", filter_value: sportId });
        }
        if (leagueId) {
            filtersData.push({ filter_name: "league_id", filter_value: leagueId });
        }
    
        try {
            const endpointMap = {
                streams: apiEndpoints.stream.getStreamsSearch,
                leagues: apiEndpoints.sports.getLeagueSearch,
                teams: apiEndpoints.teams.getTeamsAll,
                news: apiEndpoints.news.getPaginated,
                games: apiEndpoints.games.getGames
            };
    
            if (!endpointMap[model]) {
                throw new Error(`Unknown model: ${model}`);
            }
    
            const response = await axios.post(
                `${apiEndpoints.url}${endpointMap[model]}`,
                {
                    pagination: { page: page + 1, per_page: 8 },
                    filters: filtersData,
                },
                { headers: { "Content-Type": "application/json" } }
            );
    
            setCurrentItems(response.data.items || []);
            setPageCount(Math.ceil(response.data.count / 8));
            console.log(response.data.items)
        } catch (error) {
            setPageCount(0);
            toast.error(`Error loading ${model}: ${error.message}`);
        }
    };    

    useEffect(() => {
        setCurrentItems([]);
        fetchData(selectedModel, 0);
    }, [selectedModel, filters]);

    const calculateColumns = (width, layout) => {
        if (width > globalVariables.windowsSizesForCards.desktopLarge) return layout.baseColumns;
        if (width > globalVariables.windowsSizesForCards.desktopMid) return Math.max(layout.baseColumns - 1, layout.minColumns);
        if (width > globalVariables.windowsSizesForCards.tablet) return Math.max(layout.baseColumns - 2, layout.minColumns);
        if (width > globalVariables.windowsSizesForCards.mobileLarge) {
            return layout.baseColumns === 4
                ? Math.max(layout.baseColumns - 2, layout.minColumns)
                : Math.max(layout.baseColumns - 3, layout.minColumns);
        }
        if (width < globalVariables.windowsSizesForCards.mobileSmall) {
            if (layout.baseColumns === 2) {
                return layout.minColumns - 1;
            }
        }
        return layout.minColumns;
    };

    const [gridSize, setGridSize] = useState({
        ...globalVariables.cardLayouts.large,
        columns: calculateColumns(window.innerWidth, globalVariables.cardLayouts.large)
    });

    const calculateLeaguesPerPage = (layout) => {
        if (layout.minColumns === 1) return layout.alwaysColumns * 2;
        return gridSize.baseRows * gridSize.alwaysColumns
    }

    const [leaguesPerPage, setLeaguesPerPage] = useState(calculateLeaguesPerPage(globalVariables.cardLayouts.large));

    useEffect(() => {
        setLeaguesPerPage(gridSize.baseRows * gridSize.columns);
    }, [gridSize]);

    const handleGridSizeChange = (size) => {
        if (globalVariables.cardLayouts[size]) {
            setGridSize({
                ...globalVariables.cardLayouts[size],
                columns: calculateColumns(window.innerWidth, globalVariables.cardLayouts[size])
            });
        }
    };

    const toggleFilters = (model) => {
        setOpenFilterModel((prevModel) => {
            const newModel = prevModel === model ? null : model;
            console.log("openFilterModel:", newModel); 
            return newModel;
        });
    };
    

    return (
        <div className="streams-page">
            <div className="model-selection">
                {["streams", "leagues", "teams", "news", "games"].map((model) => (
                    <div className="menu">
                        <button
                        key={model}
                        className={selectedModel === model ? "active" : "menu-button"}
                        onClick={() => {
                            setSelectedModel(model);
                            toggleFilters(model); 
                        }}
                        >
                        {model.charAt(0).toUpperCase() + model.slice(1)}
                        </button>

                        {openFilterModel === model && (
                        <div className="filter-wrapper">
                            <div className={`filters-container ${openFilterModel === selectedModel ? "show" : ""}`}>
                                <FiltersRenderer model={selectedModel} onFilterChange={setFilters} />
                                <button onClick={() => fetchData(selectedModel, 0)}>{t("apply_filters")}</button>
                                <button onClick={() => setOpenFilterModel(null)}>{t("close_filters")}</button>
                             </div>
                        </div>
                        )}
                    </div>
                ))}
            </div>


            <SearchBlock
                key={selectedModel}
                gridSize={gridSize}
                onGridSizeChange={handleGridSizeChange}
                postsPerPage={10}
                pageCount={pageCount}
                currentPage={currentPage}
                onPageChange={(event) => {
                    setCurrentPage(event.selected);
                    fetchData(selectedModel, event.selected);
                }}
                paginationKey={selectedModel}
                count={currentItems.length}
            
                children={currentItems.length > 0 ? (
                    currentItems.map((item) => {
                        return componentMap(selectedModel, item);
                    })
                ) : (
                    <div>{t("no_results_found")}</div>
                )}
            >
            </SearchBlock>
        </div>
    );
}

export default SearchPage;
