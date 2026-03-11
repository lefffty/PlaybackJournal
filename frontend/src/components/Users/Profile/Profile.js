import React, { useEffect, useState } from "react";
import moment from 'moment';
import { Card, Row, Col } from 'react-bootstrap';
import Alert from 'react-bootstrap/Alert';
import {FaUser, FaAt, FaCalendarAlt, FaEnvelope, FaAngleRight} from 'react-icons/fa';
import Container from 'react-bootstrap/Container';
import { Link } from "react-router-dom";
import Button from "react-bootstrap/Button";

import ProfileListLink from './ProfileListLink';
import UserService from "../../../services/UserService";

const Profile = (props) => {
    const [profile, setProfile] = useState('');
    const token = localStorage.getItem('auth_token');

    useEffect(
        () => {
            retrieveProfile();
        }, [token]
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
                    You are not logged in. Please <Link to={"/login/"}>login</Link>.
                </Alert>
            ) : (
                <>
                    <Card className="mx-auto mb-3" style={{ maxWidth: '900px'}}>
                        <Row className="g-0">
                            <Col md={4}>
                                <Card.Img
                                    src={`http://localhost:8000/${profile.avatar}`}
                                    style={{ width: '100%', height: 'auto', objectFit: 'cover' }}
                                    />
                            </Col>
                            <Col md={8}>
                                <Card.Body>
                                    <Card.Title className="fs-2">
                                        <FaUser className="me-2 fs-1"/> {profile.first_name} {profile.last_name}
                                    </Card.Title>
                                    <Card.Text className="fs-4">
                                        <FaAt className="me-2 fs-1"/> {profile.username}
                                    </Card.Text>
                                    <Card.Text className="fs-4">
                                        <FaEnvelope className="me-2 fs-1"/> {profile.email}
                                    </Card.Text>
                                    <Card.Text className="fs-4">
                                        <FaCalendarAlt className="me-2 fs-1"/> {moment(profile.registration_date).format('Do MMMM YYYY')}
                                    </Card.Text>
                                    <Row className="mt-4">
                                        <Col xs={6} className="d-flex justify-content-center">
                                            <Link to={"/profile/password/"}>
                                                <Button variant="primary">
                                                    Change password
                                                </Button>
                                            </Link>
                                        </Col>
                                        <Col xs={6} className="d-flex justify-content-center">
                                            <Link to={"/profile/avatar/"}>
                                                <Button variant="secondary">
                                                    Change avatar
                                                </Button>
                                            </Link>
                                        </Col>
                                    </Row>
                                </Card.Body>
                            </Col>
                        </Row>
                    </Card>
                    <Card className="mx-auto" style={{ maxWidth: '900px'}}>
                        <Row className="g-0">
                            <Card.Header>
                                Альбомы
                            </Card.Header>
                            <ProfileListLink cardText={"Любимые"} link={"/profile/favourite/albums"} md={4}/>
                            <ProfileListLink cardText={"Оценки"} link={"/profile/rated/albums"} md={3}/>
                            <ProfileListLink cardText={"Прослушанные"} link={"/profile/listened/albums"} md={5}/>
                        </Row>
                        <Row className="g-0 mb-3">
                            <Card.Header>
                                Плейлисты
                            </Card.Header>
                            <ProfileListLink cardText={"Любимые"} link={"/profile/favourite/playlists"} md={4}/>
                            <ProfileListLink cardText={"Оценки"} link={"/profile/rated/playlists"} md={5}/>
                        </Row>
                    </Card>
                </>
            )}
        </Container>
    );
}

export default Profile;