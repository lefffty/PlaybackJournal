import React, { useEffect, useState } from "react";
import { Card, Col, Container, Row } from "react-bootstrap";
import { Link } from "react-router-dom";

import UserService from "../../../services/UserService";
import './AlbumsList.css';


const FavouritePlaylists = (props) => {
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');

    useEffect(
        () => {
            UserService.fetchFavouritePlaylists()
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
                        Любимые плейлисты
                    </Card.Title>
                    <Card.Body>
                        <Row className="g-0">
                            {data.map(
                                (item) => {
                                    return (
                                        <Col style={{width: '240px'}}>
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

export default FavouritePlaylists;