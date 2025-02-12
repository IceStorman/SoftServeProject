import React, { useState, useRef, useEffect } from "react";
import { FaChevronDown } from "react-icons/fa";
import { SlArrowDown } from "react-icons/sl";

const CustomSelect = ({ options, maxWidth = 300 }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [selected, setSelected] = useState(options[0]);
    const dropdownRef = useRef(null);

    const handleSelect = (option) => {
        setSelected(option);
        setIsOpen(false);
    };
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);
    return (
        <div className="custom-dropdown">
            <div className="dropdown-header" onClick={() => setIsOpen(!isOpen)}>
                <span>{selected.label}</span>
                <SlArrowDown className={`dropdown-icon ${isOpen ? "open" : ""}`} />
            </div>
            {isOpen && (
                <ul className="dropdown-list" ref={dropdownRef}>
                    {options.map((option) => (
                        <li
                            key={option.value}
                            onClick={() => handleSelect(option)}
                            className="dropdown-item"
                        >
                            {option.label}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CustomSelect;
