import React, {useState} from "react"
import useTranslations from "../../translationsContext";


const Filters = ({ setSelectedTeam, setSelectedDate, applyFilters, setInputValue }) => {
    const { t } = useTranslations();
    const [team, setTeam] = useState("");
    const [date, setDate] = useState("");

    const handleTeamChange = (event) => {
        const selectedTeam = event.target.value;
        setTeam(selectedTeam);
        setSelectedTeam(selectedTeam);
    };

    const handleDateChange = (event) => {
        const selectedDate = event.target.value;
        setDate(selectedDate);
        setSelectedDate(selectedDate);
    };

    const handleInputChange = (event) => {
        const value = event.target.value;
        setInputValue(value); // Оновлюємо значення input
    };

    const handleApplyFilters = () => {
        // Функція для застосування фільтрів, викликаємо передану функцію
        applyFilters();
    };

    return (
        <div className="filters">
            <h1>{t("filters")}</h1>
            <hr/>

            <div className="filter-option">
                <label htmlFor="team">{t("team")}</label>
                <select id="team" value={team} onChange={handleTeamChange}>
                    <option value="">{t("select_team")}</option>
                    <option value="team1">{t("team1")}</option>
                    <option value="team2">{t("team2")}</option>
                    {/* Додай більше команд за потребою */}
                </select>
            </div>

            <div className="filter-option">
                <label htmlFor="date">{t("date")}</label>
                <input
                    type="date"
                    id="date"
                    value={date}
                    onChange={handleDateChange}
                />
            </div>

            <div className="filter-option">
                <label>{t("other_filter")}</label>
                <p>{t("other_option_description")}</p>
                {/* Тут можна додати інші фільтри */}
            </div>

            <div className="filter-option">
                <label htmlFor="search">{t("search")}</label>
                <input
                    type="text"
                    id="search"
                    placeholder={t("search")}
                    onChange={handleInputChange}
                    className="input-field"
                />
            </div>

            <button onClick={handleApplyFilters}>
                {t("apply_filters")}
            </button>

        </div>
    );
}

export default Filters;
