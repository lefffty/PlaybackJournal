import React, { useState } from "react";
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from "react-router-dom";


const SignUp = props => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const signup = () => {
        props.signup({
            email: email,
            first_name: firstName,
            last_name: lastName,
            username: username,
            password: password
        });
        navigate('/login');
    }

    const onEmailChange = e => {
        const email = e.target.value;
        setEmail(email)
    }

    const onUsernameChange = e => {
        const username = e.target.value;
        setUsername(username);
    }

    const onPasswordChange = e => {
        const password = e.target.value;
        setPassword(password);
    }

    const onFirstNameChange = e => {
        const firstName = e.target.value;
        setFirstName(firstName);
    }

    const onLastNameChange = e => {
        const lastName = e.target.value;
        setLastName(lastName);
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
                        value={email}
                        placeholder="Enter email"
                        onChange={onEmailChange}
                    />
                </Form.Group>
                <Form.Group>
                    <Form.Label>
                        First name
                    </Form.Label>
                    <Form.Control
                        type="text"
                        value={firstName}
                        placeholder="Enter first name"
                        onChange={onFirstNameChange}
                    />
                </Form.Group>
                <Form.Group>
                    <Form.Label>
                        Last name
                    </Form.Label>
                    <Form.Control
                        type="text"
                        value={lastName}
                        placeholder="Enter last name"
                        onChange={onLastNameChange}
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>
                        Username
                    </Form.Label>
                    <Form.Control
                        type="text"
                        value={username}
                        placeholder="Enter username"
                        onChange={onUsernameChange}
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>
                        Password
                    </Form.Label>
                    <Form.Control
                        type="password"
                        value={password}
                        placeholder="Enter password"
                        onChange={onPasswordChange}
                    />
                </Form.Group>
            </Form>
            <Button variant="primary" onClick={signup}>
                Sign up
            </Button>
        </Container>
    );
};

export default SignUp;