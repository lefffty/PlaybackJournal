import React, { useState } from "react";
import {FaStar} from "react-icons/fa";
import Container from "react-bootstrap/Container";

const ScaleRating = ({initialValue, onRatingChange, totalStars = 10}) => {
    const [rating, setRating] = useState(initialValue);
    const [hover, setHover] = useState(0);

    const handleClick = (index) => {
        setRating(index);
        if (onRatingChange) onRatingChange(index);
    }

    return (
        <div style={{ display: 'flex', gap: '4px' }}>
            {
                [...Array(totalStars)].map(
                    (_, index) => {
                        const starValue = index + 1;
                        return (
                            <FaStar
                                
                                key={index}
                                size={30}
                                color={starValue <= (hover || rating) ? '#ffc107' : '#e4e5e9'}
                                onClick={() => handleClick(starValue)}
                                onMouseEnter={() => setHover(starValue)}
                                onMouseLeave={() => setHover(0)}
                            />
                        )
                    }
                )
            }
        </div>
    )
};

export default ScaleRating;