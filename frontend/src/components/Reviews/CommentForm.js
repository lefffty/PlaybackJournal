import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import { Button, Card, Form } from 'react-bootstrap';

import ReviewService from "../../services/ReviewService";

const CommentForm = ({reviewId, onCommentAdded}) => {
    const [error, setError] = useState(false);
    const [commentData, setCommentData] = useState({
        review: reviewId,
        text: '',
    })

    const onSubmitClick = (e) => {
        e.preventDefault();
        if (!commentData.text.trim()){
            setError(true);
        }
        else{
            ReviewService.createComment(commentData)
            .then(
                () => {
                    setCommentData({review: reviewId, text: ''})
                    setError(false);
                    if (onCommentAdded) onCommentAdded();
                }
            )
            .catch(
                (e) => setError(e.toString())
            )
        }
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
                                value={commentData.text}
                                onChange={(e) => {
                                    setCommentData({...commentData, text: e.target.value})
                                    if (error) setError(false)
                                }}
                                className="mb-2"
                                isInvalid={error}
                            />
                            <Form.Control.Feedback type="invalid">
                                Поле не может быть пустым
                            </Form.Control.Feedback>
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