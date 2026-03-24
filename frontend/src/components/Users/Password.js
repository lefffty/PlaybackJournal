import React, { useState } from "react";
import { Button, Container, Form } from "react-bootstrap";
import { Card } from "react-bootstrap";
import { useNavigate, Link } from "react-router-dom";
import Alert from "react-bootstrap/Alert";

import UserService from "../../services/UserService";


const Password = (props) => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        current_password: '',
        new_password: '',
    });
    const [error, setError] = useState({
        current_password: '',
        new_password: '',
    });
    const token = localStorage.getItem('auth_token');
    const isAuthenticated = token && token !== '';

    const validate = () => {
        const newErrors = {};

        if (!formData.current_password){
            newErrors.current_password = 'Enter current_password';
        }
        if (!formData.new_password){
            newErrors.new_password = 'Enter new_password'
        }

        return newErrors;
    }

    const setPassword = () => {
        const validationErrors = validate();
        setError(validationErrors);

        if (Object.keys(validationErrors).length > 0){
            return;
        }

        UserService.setPassword(formData)
        .then(
            (response) => {
                navigate(-1);
            }
        )
        .catch(
            (e) => {
                console.log(e.toString());
            }
        )
    }

    return (
        <Container>
            {!isAuthenticated ?
            (
                <Alert variant="warning">
                    You are not logged in. Please <Link to={"/login/"}>login</Link>.
                </Alert>
            ) : (
                <Card>
                    <Card.Header><b>Set new password</b></Card.Header>
                    <Card.Body>                
                        <Form>
                            <Form.Group className="mb-3">
                                <Form.Label>Current password</Form.Label>
                                <Form.Control
                                    type="password"
                                    onChange={(e) => setFormData({...formData, current_password: e.target.value})}
                                    value={formData.current_password}
                                    required
                                    onError={!!error.current_password}
                                    />
                                <Form.Control.Feedback type="invalid">
                                    {error.current_password}
                                </Form.Control.Feedback>
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>New password</Form.Label>
                                <Form.Control
                                    type="password"
                                    onChange={(e) => setFormData({...formData, new_password: e.target.value})}
                                    value={formData.new_password}
                                    required
                                    onError={!!error.new_password}
                                    />
                                <Form.Control.Feedback type="invalid">
                                    {error.new_password}
                                </Form.Control.Feedback>
                            </Form.Group>
                            <Button type="submit" onClick={setPassword}>
                                Submit
                            </Button>
                        </Form>
                    </Card.Body>
                </Card>
            )
        }
        </Container>
    );
};

export default Password;