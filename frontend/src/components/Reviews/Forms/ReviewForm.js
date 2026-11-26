import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import { Button, Card, Form } from 'react-bootstrap';

import ReviewService from "../../../services/ReviewService";

const ReviewForm = ({albumId, onReviewAdded}) => {
    const [errors, setErrors] = useState({
        title: false,
        text: false,
        type: false,
    })
    const [error, setError] = useState("");
    const reviewTypes = ['positive', 'negative', 'neutral'];
    const [reviewFormData, setReviewFormData] = useState({
        title: '',
        text: '',
        type: '',
        album: albumId,
    })

    const onSubmitClick = (e) => {
        e.preventDefault();
        if (!reviewFormData.title.trim()){
            setErrors({...errors, title: true})
            return
        }
        else if (reviewFormData.type === ''){
            setErrors({...errors, type: true})
            return
        }
        else if (!reviewFormData.text.trim()){
            setErrors({...errors, text: true})
            return 
        }
        else{
            ReviewService.createReview(reviewFormData)
            .then(
                (response) => {
                    setReviewFormData({
                        title: '',
                        type: '',
                        text: '',
                        album: albumId,
                    })
                    setErrors({
                        text: false,
                        title: false,
                        type: false,
                    })
                    if (onReviewAdded) onReviewAdded();
                }
            )
            .catch(
                (e) => setError(e.toString())
            )
        }
    }

    return (
        <Container>
            <Card className="mx-auto" style={{maxWidth: '500px'}}>
                <Card.Body>
                    <Card.Title data-testid="review-form-title" className="fs-3">
                        Написать рецензию
                    </Card.Title>
                    <Form onSubmit={onSubmitClick}>
                        <Form.Group>
                            <Form.Label data-testid="review-title">
                                Заголовок рецензии
                            </Form.Label>
                            <Form.Control
                                data-testid="review-title-control"
                                type="text"
                                value={reviewFormData.title}
                                onChange={(e) => {
                                    setReviewFormData({...reviewFormData, title: e.target.value})
                                    if (errors.title) setErrors({...errors, title: false})
                                }}
                                isInvalid={errors.title}
                            />
                            <Form.Control.Feedback type="invalid">
                                Поле не может быть пустым
                            </Form.Control.Feedback>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label data-testid="review-type">
                                Тип рецензии
                            </Form.Label>
                            <Form.Select
                                data-testid="review-type-control"
                                defaultValue={reviewFormData.type}
                                onChange={(e) => {
                                    setReviewFormData({...reviewFormData, type: e.target.value})
                                    if (errors.type) setErrors({...errors, type: false})
                                }}
                                isInvalid={errors.title}
                            >
                                <option value="">Выберите тип</option>
                                {reviewTypes.map(
                                    type => <option value={type}>{type}</option>
                                )}
                            </Form.Select>
                            <Form.Control.Feedback type="invalid">
                                Поле не может быть пустым
                            </Form.Control.Feedback>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label data-testid="review-text">
                                Текст рецензии
                            </Form.Label>
                            <Form.Control
                                data-testid="review-text-control"
                                as={"textarea"}
                                rows={6}
                                value={reviewFormData.text}
                                onChange={(e) => {
                                    setReviewFormData({...reviewFormData, text: e.target.value})
                                    if (errors.text) setErrors({...errors, text: false})
                                }}
                                isInvalid={errors.text}
                            />
                            <Form.Control.Feedback type="invalid">
                                Поле не может быть пустым
                            </Form.Control.Feedback>
                        </Form.Group>
                        <Button type="submit" data-testid="review-submit-btn">
                            Опубликовать рецензию
                        </Button>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    )
}

export default ReviewForm;