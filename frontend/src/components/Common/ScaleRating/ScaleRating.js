import React, { useState } from "react";
import { FaStar, FaTrash } from "react-icons/fa";

import './ScaleRating.css';

const ScaleRating = ({initialValue, onRatingChange, totalStars = 10, frozen = false}) => {
    const [rating, setRating] = useState(initialValue);
    const [hover, setHover] = useState(0);

    const handleClick = (index) => {
        if (frozen) return;
        setRating(index);
        if (onRatingChange) onRatingChange(index);
    }

    const handleReset = () => {
        if (frozen) return;
        setRating(0);
        if (onRatingChange) onRatingChange(0)
    }

    return (
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ display: 'flex', gap: '4px' }}>
                {
                    [...Array(totalStars)].map(
                        (_, index) => {
                            const starValue = index + 1;
                            return (
                                <FaStar
                                    key={index}
                                    size={30}
                                    color={starValue <= (hover || rating) ? '#ad8611' : '#e4e5e9'}
                                    onClick={frozen === false ? () => handleClick(starValue) : null}
                                    onMouseEnter={frozen === false ? () => setHover(starValue) : null}
                                    onMouseLeave={frozen === false ? () => setHover(0) : null}
                                    className="scale-rating"
                                />
                            )
                        }
                    )
                }
            </div>
            {!frozen && (
                <FaTrash
                    size={24}
                    color="#888"
                    onClick={handleReset}
                    style={{ cursor: 'pointer' }}
                    title="Сбросить оценку"
                />
            )}
        </div>
    )
};

export default ScaleRating;