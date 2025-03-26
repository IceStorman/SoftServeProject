import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import {format} from "date-fns";

function DateFilter({ onChange }) {
    const [selectedDate, setSelectedDate] = useState(null);

    const handleChange = (date) => {
        setSelectedDate(date);
        if (onChange) {
            onChange({ target: { value: date ? format(date, "yyyy-MM-dd") : null } });
        }
    };

    return (
        <>
            <label>Select date of beginning</label>
            <DatePicker
                selected={selectedDate}
                onChange={handleChange}
                dateFormat="yyyy-MM-dd"
            />
        </>
    );
}

export default DateFilter;
