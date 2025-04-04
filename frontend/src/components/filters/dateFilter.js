import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import {format} from "date-fns";

function DateFilter({ onChange, label }) {
    const [selectedDate, setSelectedDate] = useState(null);

    const handleChange = (date) => {
        setSelectedDate(date);
        if (onChange) {
            onChange({ target: { value: date ? format(date, "yyyy-MM-dd") : null } });
        }
    };

    return (
        <>
            <div>
                <label className="dateHeading">{label}</label>
                <DatePicker
                    selected={selectedDate}
                    onChange={handleChange}
                    dateFormat="yyyy-MM-dd"
                    className="dateFilter"
                />
            </div>
        </>
    );
}

export default DateFilter;
