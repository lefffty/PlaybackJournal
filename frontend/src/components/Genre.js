import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import { useParams, Link } from "react-router-dom";
import { Card, Row, Col } from "react-bootstrap";

import GenreService from "../services/GenreService";

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
                                <Card.Title>
                                    {genre.name}
                                </Card.Title>
                            </Col>
                        </Row>
                        <Card.Text>
                            {genre.description}
                        </Card.Text>
                        <Card.Header className="fs-6 mb-3">
                            <b>Artists</b>
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
                                                        width: '100px',
                                                        height: '100px',
                                                        objectFit: 'cover'
                                                    }}
                                                    />
                                            </Link>
                                            <Link to={`/artists/${artist.id}/`} className="text-decoration-none">
                                                <Col>
                                                    {artist.username}
                                                </Col>
                                            </Link>
                                        </Col>
                                    )
                                }
                            )}
                        </Row>
                        <Card.Header className="fs-6 mb-3">
                            <b>Albums</b>
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
                                                        borderRadius: '50%',
                                                        width: '100px',
                                                        height: '100px',
                                                        objectFit: 'cover'
                                                    }}
                                                    />
                                            </Link>
                                            <Link to={`/albums/${album.id}/`} className="text-decoration-none">
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
