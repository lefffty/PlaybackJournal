import React, { useEffect, useState } from "react";
import {Row, Col} from 'react-bootstrap';
import './ReviewReaction.css';
import {FaThumbsUp, FaThumbsDown} from 'react-icons/fa';

import ReviewService from "../../../services/ReviewService";

const ReviewReaction = ({initialState = '', reviewId = null}) => {
    const [reaction, setReaction] = useState(initialState);
    const [error, setError] = useState('');

    useEffect(
        () => {
            console.log(reaction)
        },
        [reaction]
    )

    const handleLikeClick = () => {
        const newReaction = reaction === 'useful' ? '' : 'useful';
        setReaction(newReaction);
        const data = {
            reaction: newReaction,
        }
        if (reaction === 'useful'){
            data.reaction = 'useful';
        }
        ReviewService.reactionReview(reviewId, data)
        .catch(e => setError(e.toString()));
    }

    const handleDislikeClick = () => {
        const newReaction = reaction === 'not_useful' ? '' : 'not_useful';
        setReaction(newReaction);
        const data = {
            reaction: newReaction,
        }
        if (reaction === 'not_useful'){
            data.reaction = 'not_useful';
        }
        ReviewService.reactionReview(reviewId, data)
        .catch(e => setError(e.toString()));
    }

    const likeColor = reaction === 'useful' ? 'green' : 'gray';
    const dislikeColor = reaction === 'not_useful' ? 'red' : 'gray';

    return (
        <Row>
            <Col
                xs="auto"
                style={{
                    backgroundColor: 'white',
                    borderRadius: '50px',
                    height: '40px',
                    width: '130px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'flex-start',
                    gap: '20px',
                    padding: '0 12px',
                }}
                onClick={handleLikeClick}
                className="review-reaction"
            >
                <FaThumbsUp size={22} color={likeColor}/>
                <span style={{ fontSize: '14px', color: '#555', textAlign: "center" }}><b>Полезно</b></span>
            </Col>
            <Col
                xs="auto"
                style={{
                    marginLeft: '30px',
                    backgroundColor: 'white',
                    borderRadius: '50px',
                    height: '40px',
                    width: '130px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'start',
                    gap: '30px',
                    padding: '0 12px',
                }}
                onClick={handleDislikeClick}
                className="review-reaction"
            >
                <FaThumbsDown size={22} color={dislikeColor}/>
                <span style={{ fontSize: '14px', color: '#555', textAlign: "center" }}><b>Нет</b></span>
            </Col>
        </Row>
    )
}

export default ReviewReaction;