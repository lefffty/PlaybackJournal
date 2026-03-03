import React, { useEffect, useState } from "react";
import Container from 'react-bootstrap/Container';
import {Card, Col, Row} from 'react-bootstrap';
import { useSearchParams } from "react-router-dom";
import { Link } from "react-router-dom";

import SearchService from './../../services/SearchService';

const SearchResults = () => {
    const [searchParams] = useSearchParams();
    const searchQuery = searchParams.get('q') || '';
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(
        () => {
            if (!searchQuery) return;
            setLoading(true);
            const params = {
                query: searchQuery
            }
            SearchService.search(params)
            .then(
                (response) => {
                    setData(response.data);
                    setError('');
                }
            )
            .catch(
                (e) => console.log(e.toString())
            )
            .finally(
                () => setLoading(false)
            )
        },
        [searchQuery]
    );

    if (loading){
        return (
            <Container>
                Loading...
            </Container>
        )
    }

    if (error){
        return (
            <Container>
                Error: {error}
            </Container>
        )
    }

    return (
        <Container>
            <h1>
                Результаты поиска для "{searchQuery}":
            </h1>
            <h3>
                Исполнители
            </h3>
            {data.artists?.length > 0 && ( data.artists.map(
                (artist) => {
                    return (
                        <Card className="mb-3 w-50">
                            <Row className="g-0">
                                <Col md={4} className="d-flex">
                                    <Card.Img
                                        src={artist.avatar}
                                    />
                                </Col>
                                <Col md={8}>
                                    <Card.Body>
                                        <Link to={`/artists/${artist.id}/`} className="text-decoration-none">
                                            <Card.Title>{artist.username}</Card.Title>
                                        </Link>
                                    </Card.Body>
                                </Col>
                            </Row>
                        </Card>
                    )
                }
            ))}
            <h3>
                Альбомы
            </h3>
            {data.albums?.length > 0 && (
                data.albums.map(
                    (album) => {
                        return (
                        <Card className="mb-3 w-50">
                            <Row className="g-0">
                                <Col md={4} className="d-flex">
                                    <Card.Img
                                        src={album.cover}
                                    />
                                </Col>
                                <Col md={8}>
                                    <Card.Body>
                                        <Link to={`/albums/${album.id}/`} className="text-decoration-none">
                                            <Card.Title>{album.name}</Card.Title>
                                        </Link>
                                    </Card.Body>
                                </Col>
                            </Row>
                        </Card>
                        )
                    }
                )
            )}
            <h3>
                Песни
            </h3>
            {data.songs?.length > 0 && (
                data.songs.map(
                    (song) => {
                        return (
                        <Card className="mb-3 w-50">
                            <Row className="g-0">
                                <Col md={8}>
                                    <Card.Body>
                                        <Link to={`/songs/${song.id}/`} className="text-decoration-none">
                                            <Card.Title>{song.name}</Card.Title>
                                        </Link>
                                    </Card.Body>
                                </Col>
                            </Row>
                        </Card>
                        )
                    }
                )
            )}
            <h3>
                Плейлисты
            </h3>
            {data.playlists?.length > 0 && (
                data.playlists.map(
                    (playlist) => {
                        return (
                        <Card className="mb-3 w-50">
                            <Row className="g-0">
                                <Col md={4} className="d-flex">
                                    <Card.Img
                                        src={playlist.cover}
                                    />
                                </Col>
                                <Col md={8}>
                                    <Card.Body>
                                        <Link to={`/albums/${playlist.id}/`} className="text-decoration-none">
                                            <Card.Title>{playlist.name}</Card.Title>
                                        </Link>
                                    </Card.Body>
                                </Col>
                            </Row>
                        </Card>
                        )
                    }
                )
            )}
        </Container>
    )
}

export default SearchResults;