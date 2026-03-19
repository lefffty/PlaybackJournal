import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Card, Col, Row } from "react-bootstrap";
import Container from "react-bootstrap/Container";

import Review from "./Review";
import Comments from "./Comments";
import ReviewService from "../../services/ReviewService";


const ReviewDetail = (props) => {
    const [review, setReview] = useState(null);
    const [error, setError] = useState('');
    const params = useParams();
    const reviewId = params.reviewId;

    useEffect(
        () => {
            ReviewService.fetchReview(reviewId)
            .then(
                (response) => {
                    setReview(response.data);
                }
            )
            .catch(
                e => setError(e.toString())
            )
        },
        []
    )

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
        </Container>
    )
}

export default ReviewDetail;