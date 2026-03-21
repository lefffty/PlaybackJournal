import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import { Button, Card, Form } from 'react-bootstrap';

import ReviewService from "../../services/ReviewService";
import { useNavigate, useParams } from "react-router-dom";

const CommentForm = ({reviewId, albumId}) => {
    const params = useParams();
    const navigate = useNavigate();
    const [error, setError] = useState('');
    const [commentData, setCommentData] = useState({
        review: reviewId,
        text: '',
    })

    const onSubmitClick = () => {
        ReviewService.createComment(commentData)
        .catch(
            (e) => setError(e.toString())
        )
    }

    return (
        <Container>
            <Card className="border-0 mx-auto" style={{maxWidth: '500px'}}>
                <Card.Body>
                    <Form>
                        <Form.Group>
                            <Form.Label className="mb-2">
                                Текст комментария
                            </Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={2}
                                onChange={(e) => setCommentData({...commentData, text: e.target.value})}
                                className="mb-2"
                            />
                        </Form.Group>
                        <Button
                            type="submit"
                            onClick={onSubmitClick}
                            variant="light"
                        >
                            Отправить
                        </Button>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    )
}

export default CommentForm;