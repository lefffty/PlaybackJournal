import React from "react";
import { useState } from "react";
import {Row, Col} from 'react-bootstrap';
import { FaPlus, FaMinus } from "react-icons/fa";

import './Reaction.css';
import ReviewService from "../../../../services/ReviewService";

const CommentReaction = ({initialState = '', commentId = null}) => {
    const [reaction, setReaction] = useState(initialState);
    const [error, setError] = useState('');

    const handleLikeClick = () => {
        const newReaction = reaction === 'plus' ? '' : 'plus';
        setReaction(newReaction);
        const data = {
            reaction: newReaction,
        }
        if (reaction === 'plus'){
            data.reaction = 'plus';
        }
        ReviewService.reactionComment(commentId, data)
        .catch(e => setError(e.toString))
    }

    const handleDislikeClick = () => {
        const newReaction = reaction === 'minus' ? '' : 'minus';
        setReaction(newReaction);
        const data = {
            reaction: newReaction,
        }
        if (reaction === 'minus'){
            data.reaction = 'minus';
        }
        ReviewService.reactionComment(commentId, data)
        .catch(e => setError(e.toString))
    }

    const plusColor = reaction === 'plus' ? 'green' : 'gray';
    const minusColor = reaction === 'minus' ? 'red' : 'gray';

    return (
        <Row
            style={{
                justifyContent: 'end'
            }}
        >
            <Col
                xs="auto"
                style={{
                    backgroundColor: 'white',
                    borderRadius: '50px',
                    height: '40px',
                    width: '40px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
                onClick={handleLikeClick}
                className="review-reaction"
            >
                <FaPlus size={16} color={plusColor}/>
            </Col>
            <Col
                xs="auto"
                style={{
                    backgroundColor: 'white',
                    borderRadius: '50px',
                    height: '40px',
                    width: '40px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
                onClick={handleDislikeClick}
                className="review-reaction"
            >
                <FaMinus size={16} color={minusColor}/>
            </Col>
        </Row>
    )
}

export default CommentReaction;
