import React, { useEffect, useState } from "react";
import UserService from "../services/UserService";

import moment from 'moment';
import { Card, Row, Col } from 'react-bootstrap';
import Alert from 'react-bootstrap/Alert';
import {FaUser, FaAt, FaCalendarAlt, FaEnvelope} from 'react-icons/fa';
import Container from 'react-bootstrap/Container';
import { Link, useLocation } from "react-router-dom";
import Button from "react-bootstrap/Button";


const Profile = props => {
    const [profile, setProfile] = useState('');
    const location = useLocation()
    const token = localStorage.getItem('auth_token');

    useEffect(
        () => {
            retrieveProfile();
        }, [token]
    );

    useEffect(
        () => {
            console.log('Profile updated: ', profile);
        },
        [profile]
    );

    const retrieveProfile = () => {
        UserService.profile(token)
        .then(
            (response) => {
                setProfile(response.data);
            }
        ).catch(
            e => {
                console.log(e.toString());
            }
        )
    };

    return (
        <Container>
            {token == null || token === "" ? (
                <Alert variant="warning">
                    You are not logged in. Please <Link to={"/login"}>login</Link>.
                </Alert>
            ) : (
                <Card>
                <Row className="g-0">
                    <Col md={4}>
                    <Card.Img
                        src={`http://localhost:8000/${profile.avatar}`}
                        style={{ width: '100%', height: 'auto', objectFit: 'cover' }}
                    />
                    </Col>
                    <Col md={8}>
                    <Card.Body>
                        <Card.Title>
                            <FaUser className="me-2 fs-1"/> {profile.first_name} {profile.last_name}
                        </Card.Title>
                        <Card.Text>
                            <FaAt className="me-2 fs-1"/> {profile.username}
                        </Card.Text>
                        <Card.Text>
                            <FaEnvelope className="me-2 fs-1"/> {profile.email}
                        </Card.Text>
                        <Card.Text>
                            <FaCalendarAlt className="me-2 fs-1"/> {moment(profile.registration_date).format('Do MMMM YYYY')}
                        </Card.Text>
                    </Card.Body>
                    </Col>
                </Row>
                </Card>
            )}
        </Container>
    );
}

export default Profile;