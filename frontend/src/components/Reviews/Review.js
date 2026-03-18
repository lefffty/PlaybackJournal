import React from "react";
import {Card, Row, Col} from "react-bootstrap";
import moment from "moment";


const Review = ({review}) => {
    const typeToColor = {
        negative: '#ff72722f',
        positive: '#bcffa66c',
        neutral: '#c6d7cf84',
    }

    const reviewColor = typeToColor[review.type];
    console.log(reviewColor)

    return (
        <Col md={12}>
            <Card
                className="mb-3"
                style={{
                    backgroundColor: reviewColor
                }}
            >
                <Row className="align-items-center mt-3 ms-1">
                    <Col md={2} className="d-flex justify-content-center">
                        <Card.Img
                            style={{
                                width: '75px',
                                height: '75px',
                                borderRadius: '90px'
                            }}
                            src={`http://localhost:8000/${review.author.avatar}`}
                            >
                        </Card.Img>
                    </Col>
                    <Col md={6}>
                        <span className="fs-3">
                            <b>{review.author.username}</b>
                        </span>
                    </Col>
                    <Col md={4}>
                        <span>
                            {moment(review.updated_at).format('D MMMM YYYY [г.] HH:mm')}
                        </span>
                    </Col>
                </Row>
                <hr></hr>
                <Card.Body
                    style={{
                        textAlign: "left",
                    }}
                    className="pt-0"
                >
                    <Card.Title className="fs-3">
                        {review.title}
                    </Card.Title>
                    <Card.Text>
                        {review.text}
                    </Card.Text>
                </Card.Body>
            </Card>
        </Col>
    )
}

export default Review;