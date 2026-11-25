import React from "react";
import { Card, Row, Col } from "react-bootstrap";

import Review from "../Reviews/Review";
import Reviews from "../Statistics/Reviews/Reviews";

const AlbumReviews = ({ id, isStatistics, reviewsStatistics, reviews }) => {
    if (!isStatistics) {
        return null;
    }

    return (
        <>
            <Card.Title className="mb-3 fs-3">
                Рецензии слушателей
            </Card.Title>
            <Row className="g-0">
                <Col md={8} className="pe-3">
                    {reviews.map((review) => (
                        <Review
                            key={review.id}
                            review={review}
                            albumId={id}
                        />
                    ))}
                </Col>
                <Col md={4} className="statistics-block" style={{ top: "20px" }}>
                    <Reviews stats={reviewsStatistics} />
                </Col>
            </Row>
        </>
    );
};

export default AlbumReviews;