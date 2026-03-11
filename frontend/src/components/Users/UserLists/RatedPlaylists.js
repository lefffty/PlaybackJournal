import React, { useEffect, useState } from "react";
import { Card, Col, Container, Row } from "react-bootstrap";
import { Link } from "react-router-dom";

import UserService from "../../../services/UserService";
import './UserList.css';

const RatedPlaylists = (props) => {
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');

    useEffect(
        () => {
            UserService.fetchRatedPlaylists()
            .then(
                (response) => {
                    setData(response.data);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        },
        [token]
    )

    if (error){
        return (
            <div>
                <h1>
                    Error: {error}
                </h1>
            </div>
        )
    }

    return (
        <div>
            <Container>
                <Card>
                    <Card.Title className="fs-1 ms-3 mt-3">
                        Оценки
                    </Card.Title>
                    <Card.Body>
                        <Row className="g-0 flex-nowrap" style={{flexWrap: "nowrap", gap: '10px'}}>
                            {data.map(
                                (item) => {
                                    return (
                                        <Col className="p-0 flex-shrink-0" key={item.playlist.id}>
                                            <div style={{position: "relative", width: '240px', height: '240px'}}>
                                                <Link to={`/playlists/${item.playlist.id}/`}>
                                                    <Card.Img
                                                        src={"http://localhost:8000" + item.playlist.cover}
                                                        style={{
                                                            borderRadius: '5%',
                                                            width: '240px',
                                                            height: '240px',
                                                            objectFit: 'cover'
                                                        }}
                                                        className="album-cover"
                                                    />
                                                </Link>
                                                <div
                                                    style={{
                                                        position: 'absolute',
                                                        top: '10px',
                                                        right: '10px',
                                                        width: '40px',
                                                        height: '40px',
                                                        borderRadius: '50%',
                                                        backgroundColor: '#f5efe0',
                                                        color: '#000',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                        fontWeight: 'bold',
                                                        fontSize: '1.2rem',
                                                        boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
                                                        zIndex: 10
                                                    }}
                                                >
                                                    {item.rating}
                                                </div>
                                            </div>
                                            <Link
                                                to={`/playlists/${item.playlist.id}/`}
                                                className="text-decoration-none fs-4 d-block"
                                                style={{color: "black", width: "240px"}}
                                            >
                                                <Card.Text
                                                    className="album-title"
                                                >
                                                    {item.playlist.name}
                                                </Card.Text>
                                            </Link>
                                        </Col>
                                    )
                                }
                            )}
                        </Row>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
};

export default RatedPlaylists;