import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import { useParams, Link } from "react-router-dom";
import { Card, Row, Col } from "react-bootstrap";
import {FaAngleRight} from 'react-icons/fa';

import GenreService from "../../services/GenreService";
import './Genre.css';

const Genre = (props) => {
    const params = useParams(null);
    const id = params.id;
    const token = localStorage.getItem('auth_token');
    const [genre, setGenre] = useState(null);
    const [error, setError] = useState('');

    useEffect(
        () => {
            GenreService.readGenre(id)
            .then(
                (response) => {
                    setGenre(response.data);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        },
        []
    )

    if (!genre){
        return (
            <div>
                Loading...
            </div>
        )
    }

    if (error){
        return (
            <div>
                Error: {error}
            </div>
        )
    }

    return (
        <div>
            <Container>
                <Card>
                    <Card.Body>
                        <Row md={2}>
                            <Col>
                                <Card.Title className="fs-2">
                                    {genre.name}
                                </Card.Title>
                            </Col>
                        </Row>
                        <Card.Text className="fs-4">
                            {genre.description}
                        </Card.Text>
                        <Card.Header className="fs-3 mb-3">
                            <div className="d-flex align-items-end" style={{height: '50px'}}>
                                <Link to={`/genre/${genre.id}/artists/`} style={{color: "black"}} className="text-decoration-none">
                                    <Card.Text className="mb-0 me-2">
                                        <b>Исполнители</b>
                                    </Card.Text>
                                </Link>
                                <Link to={`/genre/${genre.id}/artists/`} style={{color: "black"}}>
                                    <FaAngleRight className="hover-shift"/>
                                </Link>
                            </div>
                        </Card.Header>
                        <Row className="g-0">
                            {genre.artists.map(
                                (artist) => {
                                    return (
                                        <Col style={{textAlign: "center"}}>
                                            <Link to={`/artists/${artist.id}/`}>
                                                <Card.Img
                                                    src={`http://localhost:8000/${artist.avatar}`}
                                                    style={{
                                                        borderRadius: '50%',
                                                        width: '240px',
                                                        height: '240px',
                                                        objectFit: 'cover'
                                                    }}
                                                    />
                                            </Link>
                                            <Link
                                                to={`/artists/${artist.id}/`}
                                                className="text-decoration-none fs-5"
                                                style={{color: "black"}}
                                            >
                                                <Col>
                                                    {artist.username}
                                                </Col>
                                            </Link>
                                        </Col>
                                    )
                                }
                            )}
                        </Row>
                        <Card.Header className="fs-3 mb-3">
                            <div className="d-flex align-items-end" style={{height: '50px'}}>
                                <Link to={`/genre/${genre.id}/albums/`} style={{color: "black"}} className="text-decoration-none">
                                    <Card.Text className="mb-0 me-2">
                                        <b>Альбомы</b>
                                    </Card.Text>
                                </Link>
                                <Link to={`/genre/${genre.id}/albums/`} style={{color: "black"}} className="text-decoration-none">
                                    <FaAngleRight className="hover-shift"/>
                                </Link>
                            </div>
                        </Card.Header>
                        <Row className="g-0">
                            {genre.albums.map(
                                (album) => {
                                    return (
                                        <Col style={{textAlign: "center"}}>
                                            <Link to={`/albums/${album.id}/`}>
                                                <Card.Img
                                                    src={`http://localhost:8000/${album.cover}`}
                                                    style={{
                                                        borderRadius: '75%',
                                                        width: '240px',
                                                        height: '240px',
                                                        objectFit: 'cover'
                                                    }}
                                                    />
                                            </Link>
                                            <Link
                                                to={`/albums/${album.id}/`}
                                                className="text-decoration-none fs-5"
                                                style={{color: "black"}}
                                            >
                                                <Col>
                                                    {album.name}
                                                </Col>
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
}

export default Genre;
