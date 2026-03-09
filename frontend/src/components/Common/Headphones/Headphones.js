import React, { useState } from "react";
import {FaHeadphones} from "react-icons/fa";

import './Headphones.css';

function Headphones({initialValue, onClick}){
    const [listened, setListened] = useState(initialValue);

    const onListenedClick = () => {
        setListened(!listened);
        if (onClick) onClick(!listened);
    }

    return (
        <div
            style={{
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
            }}
        >
            <FaHeadphones
                color={listened ? "blue" : "gray"}
                size={30}
                onClick={onListenedClick}
                className="headphones"
            />
        </div>
    )
}

export default Headphones;