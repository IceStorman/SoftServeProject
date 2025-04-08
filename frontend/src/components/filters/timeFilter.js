import React, { useState } from "react";

function TimeFilter({ onChange, label }) {
    const [selectedTime, setSelectedTime] = useState("");

    const handleChange = (e) => {
        const time = e.target.value;
        setSelectedTime(time);
        if (onChange) {
            onChange({ target: { value: time } });
        }
    };

    return (
        <div>
            <label className="timeHeading">{label}</label>
            <input
                type="time"
                value={selectedTime}
                onChange={handleChange}
                className="timeFilter"
                step="60"
            />
        </div>
    );
}

export default TimeFilter;