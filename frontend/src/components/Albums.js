import React, { useEffect, useState } from "react";
import { Card, Row, Col, Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import { Link, useLocation } from "react-router-dom";
import moment from 'moment';

import AlbumService from '../services/AlbumService';

const Albums = (props) => {
    const [albums, setAlbums] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(
        () => {
            AlbumService.readAlbums()
            .then(
                (response) => {
                    setAlbums(response.data.results);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
            .finally(
                () => {
                    setLoading(false);
                }
            )
        },
        []
    )

    if (loading){
        return (
            <div>
                Loading...
            </div>
        )
    };

    if (error){
        return (
            <div>
                Error: {error}
            </div>
        )
    };

    return (
        <Container>
            {albums.map(
                (album) => {
                    return (
                        <Card className="w-55 mb-3">
                            <Row className="g-0">
                                <Col md={4}>
                                <Card.Img
                                    src={album.cover}
                                />
                                </Col>
                                <Col md={8}>
                                <Card.Body>
                                    <Card.Title>
                                        {album.name}
                                    </Card.Title>
                                    <Card.Text>
                                        Авторы: {album.artists.reduce((accumulator, currentValue) => {
                                            return accumulator.concat(currentValue.username);
                                        }, []).join(', ')}
                                    </Card.Text>
                                    <Card.Text>
                                        Выпущен: {moment(album.publication_date).format('Do MMMM YYYY')}
                                    </Card.Text>
                                    <Card.Text>
                                        Жанры: {album.genres.reduce((accumulator, currentValue) => {
                                            return accumulator.concat(currentValue.name);
                                        }, []
                                        ).join(', ')}
                                    </Card.Text>
                                    <Link to={`/albums/${album.id}/`} state={{album}}>
                                        <Button>
                                            К альбому
                                        </Button>
                                    </Link>
                                </Card.Body>
                                </Col>
                            </Row>
                        </Card>
                    );
                }
            )}
        </Container>
    )
};


export default Albums;