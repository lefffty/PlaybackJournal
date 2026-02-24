import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const Login = props => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const onEmailChange = e => {
        const email = e.target.value;
        setEmail(email);
    }

    const onPasswordChange = e => {
        const password = e.target.value;
        setPassword(password);
    }

    const login = () => {
        props.login({email: email, password: password});
        navigate("/albums");
    }

    return (
        <Container>
            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>
                        Email
                    </Form.Label>
                    <Form.Control
                    type="email"
                    placeholder="Enter email"
                    value={email}
                    onChange={onEmailChange}
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>
                        Password
                    </Form.Label>
                    <Form.Control
                    type="text"
                    placeholder="Enter password"
                    value={password}
                    onChange={onPasswordChange}
                    />
                </Form.Group>
            </Form>
            <Button variant="primary" onClick={login}>
                Login
            </Button>
        </Container>
    );
}

export default Login;