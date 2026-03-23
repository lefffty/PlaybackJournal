import React from "react";
import { useState } from "react";
import {Row, Col} from 'react-bootstrap';
import { FaPlus, FaMinus } from "react-icons/fa";

import './Reaction.css';
import ReviewService from "../../../../services/ReviewService";

const CommentReaction = ({
    initialState = '',
    commentId = null,
    plusCount = 0,
    minusCount = 0
}) => {
    const [plusCounter, setPlusCounter] = useState(plusCount);
    const [minusCounter, setMinusCounter] = useState(minusCount);
    const [reaction, setReaction] = useState(initialState);
    const [error, setError] = useState('');

    const handleLikeClick = () => {
        const newReaction = reaction === 'plus' ? '' : 'plus';
        const action = reaction === 'plus' ? -1 : 1;
        setPlusCounter(plusCounter + action);
        setReaction(newReaction);
        if (reaction === 'minus'){
            setMinusCounter(minusCounter - 1);
        }
        const data = {
            reaction: newReaction,
        }
        if (reaction === 'plus'){
            data.reaction = 'plus';
        }
        ReviewService.reactionComment(commentId, data)
        .catch(e => setError(e.toString()))
    }

    const handleDislikeClick = () => {
        const newReaction = reaction === 'minus' ? '' : 'minus';
        const action = reaction === 'minus' ? -1 : 1;
        setMinusCounter(minusCounter + action);
        if (reaction === 'plus'){
            setPlusCounter(plusCounter - 1);
        }
        setReaction(newReaction);
        const data = {
            reaction: newReaction,
        }
        if (reaction === 'minus'){
            data.reaction = 'minus';
        }
        ReviewService.reactionComment(commentId, data)
        .catch(e => setError(e.toString()))
    }

    const plusColor = reaction === 'plus' ? 'green' : 'gray';
    const minusColor = reaction === 'minus' ? 'red' : 'gray';

    return (
        <Row style={{ justifyContent: 'end' }}>
            <Col xs="auto" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <div
                style={{
                    backgroundColor: 'white',
                    borderRadius: '50px',
                    height: '40px',
                    width: '40px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    cursor: 'pointer',
                }}
                onClick={handleLikeClick}
                className="review-reaction"
                >
                <FaPlus size={16} color={plusColor} />
                </div>
                <span style={{ marginTop: '4px', fontSize: '12px', fontWeight: 'bold' }}>
                {plusCounter}
                </span>
            </Col>
            <Col xs="auto" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <div
                style={{
                    backgroundColor: 'white',
                    borderRadius: '50px',
                    height: '40px',
                    width: '40px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    cursor: 'pointer',
                }}
                onClick={handleDislikeClick}
                className="review-reaction"
                >
                    <FaMinus size={16} color={minusColor} />
                </div>
                    <span style={{ marginTop: '4px', fontSize: '12px', fontWeight: 'bold' }}>
                        {minusCounter}
                    </span>
            </Col>
        </Row>
    )
}

export default CommentReaction;
