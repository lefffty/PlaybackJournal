import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Card, Col, Row } from "react-bootstrap";
import Container from "react-bootstrap/Container";

import Review from "./Review";
import CommentForm from "./CommentForm";
import Comments from "./Comments";
import ReviewService from "../../services/ReviewService";


const ReviewDetail = (props) => {
    const [review, setReview] = useState(null);
    const [error, setError] = useState('');
    const params = useParams();
    const token = localStorage.getItem('auth_token');
    const albumId = params.albumId;
    const reviewId = params.reviewId;

    const fetchReview = () => {
        ReviewService.fetchReview(reviewId)
        .then(response => setReview(response.data))
        .catch(e => setError(e.toString()))
    }

    useEffect(
        () => {
            fetchReview();
        },
        [reviewId]
    )

    const handleCommentAdded = () => {
        fetchReview();
    }

    if (error){
        return (
            <div>
                Error: {error}
            </div>
        )
    }

    if (!review){
        return (
            <Container>
                Загрузка...
            </Container>
        )
    }

    return (
        <Container>
            <Review review={review}/>
            <Container className="d-flex justify-content-center">
                <Col md={8}>
                    <Row>
                        <Card
                            className="d-flex align-items-center mt-3 border-0"
                            style={{
                                backgroundColor: '#60b1e73a',
                                height: '30px',
                                alignContent: 'center',
                                alignItems: "start"
                            }}
                        >
                            <b>Комментарии ({review.comments.length})</b>
                        </Card>
                    </Row>
                    <Row>
                        <Comments comments={review.comments}/>
                    </Row>
                </Col>
            </Container>
            {token !== null || token !== ''
                ? (
                    <>
                        <CommentForm reviewId={reviewId} onCommentAdded={handleCommentAdded}/>
                    </>
                )
                : (
                    <>
                    </>
                )
            }
        </Container>
    )
}

export default ReviewDetail;