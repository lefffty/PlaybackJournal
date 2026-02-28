import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Card, Col, Row, Container } from "react-bootstrap";
import { FaAngleRight } from "react-icons/fa";

import './Album.css';
import ArtistService from '../services/ArtistService';

const Artist = (props) => {
    const [artist, setArtist] = useState(null);
    const params = useParams();
    const id = params.id;
    const [error, setError] = useState('');

    useEffect(
        () => {
            setArtist(null);
            ArtistService.readArtist(id)
            .then(
                (response) => {
                    setArtist(response.data);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        },
        [id]
    );

    if (!artist){
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
                <Card className="mb-3">
                    <Row className="g-0">
                        <Col md={4}>
                            <Card.Img
                                src={artist.avatar}
                            />
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Card.Title className="fs-1">
                                    {artist.username}
                                </Card.Title>
                                <Card.Text>
                                    {artist.description}
                                </Card.Text>
                                <Card.Text className="fs-4">
                                    <span><b>Жанры</b>: </span>
                                    <span>
                                        {artist.genres.map(
                                            (genre, index) => (
                                                <React.Fragment>
                                                    <Link to={`/genres/${genre.id}/`} className="text-decoration-none">
                                                        {genre.name}
                                                    </Link>
                                                    {index < artist.genres.length - 1 && ', '}
                                                </React.Fragment>
                                            )
                                        )}
                                    </span>
                                </Card.Text>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
                <Card className="mb-3">
                    <Card.Body>
                        <Card.Header className="fs-3 mb-3">
                            <div className="d-flex align-items-end" style={{height: '50px'}}>
                                <Link
                                    to={"#"}
                                    className="text-decoration-none"
                                    style={{
                                        color: "black"
                                    }}
                                >
                                    <Card.Text className="mb-0 me-2">
                                        <b>Альбомы</b>
                                    </Card.Text>
                                </Link>
                                <Link
                                    to={"#"}
                                    style={{
                                        color: "black"
                                    }}
                                >
                                    <FaAngleRight
                                        className="hover-shift"
                                    />
                                </Link>
                            </div>
                        </Card.Header>
                        <Row className="g-0">
                            {artist.albums.map(
                                (album) => {
                                    return (
                                        <Col style={{textAlign: "center"}}>
                                            <Link
                                                to={`/albums/${album.id}`}
                                            >
                                                <Card.Img
                                                    src={album.cover}
                                                    style={{
                                                        borderRadius: '75%',
                                                        width: '240px',
                                                        height: '240px',
                                                        objectFit: 'cover'
                                                    }}
                                                />
                                            </Link>
                                            <Link
                                                to={`/albums/${album.id}`}
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
                <Card className="mb-3">
                    <Card.Body>
                        <Card.Header  className="fs-3 mb-3">
                            <div className="d-flex align-items-end">
                                <Link
                                    to={"#"}
                                    className="text-decoration-none"
                                    style={{
                                        color: "black"
                                    }}
                                >
                                    <Card.Text className="mb-0 me-2">
                                        <b>Похожие исполнители</b>
                                    </Card.Text>
                                </Link>
                                <Link
                                    to={"#"}
                                    style={{
                                        color: "black"
                                    }}
                                >
                                    <FaAngleRight
                                        className="hover-shift"
                                    />
                                </Link>
                            </div>
                        </Card.Header>
                        <Row className="g-0">
                            {artist.similar.map(
                                (art) => {
                                    return (
                                        <Col style={{textAlign: "center"}}>
                                            <Link
                                                to={`/artists/${art.id}/`}
                                            >
                                                <Card.Img
                                                    src={art.avatar}
                                                    style={{
                                                        borderRadius: '75%',
                                                        width: '240px',
                                                        height: '240px',
                                                        objectFit: 'cover'
                                                    }}
                                                />
                                            </Link>
                                            <Link
                                                to={`/artists/${art.id}/`}
                                                className="text-decoration-none fs-5"
                                                style={{color: "black"}}
                                            >
                                                <Col>
                                                    {art.username}
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
};

export default Artist;