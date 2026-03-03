import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import {useParams} from 'react-router-dom';
import {Card, Row, Col, ListGroup} from 'react-bootstrap';

import PlaylistService from "../../services/PlaylistService";

const Playlist = (props) => {
    const params = useParams();
    const id = params.id;
    const [playlist, setPlaylist] = useState(null);
    const [error, setError] = useState('');

    useEffect(
        () => {
            PlaylistService.fetchPlaylist(id)
            .then(
                (response) => {
                    setPlaylist(response.data);
                }
            )
        },
        [id]
    )

    if (!playlist){
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
            <Container className="w-75">
                <Card className="mb-3">
                    <Row className="g-0">
                        <Col md={4} className="d-flex">
                            <Card.Img
                                src={playlist.cover}
                            >
                            </Card.Img>
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Row>
                                    <Col md={8}>
                                        <Card.Title className="fs-1">
                                            {playlist.name}
                                        </Card.Title>
                                        <Card.Text className="fs-3">
                                            <span className="text-muted fs-3">Автор: </span>
                                            <span className="fs-3">
                                                <b>@{playlist.author.username}</b>
                                            </span>
                                        </Card.Text>
                                        <Card.Text className="fs-3">
                                            {playlist.description}
                                        </Card.Text>
                                    </Col>
                                </Row>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
                <Card>
                    <Card.Body>
                        <ListGroup variant="flush">
                            <Card.Title>
                                Список песен:
                            </Card.Title>
                            {playlist.songs.map(
                                (song, index) => (
                                    <ListGroup.Item key={song.id} className="px-0">
                                        <Row>
                                            <Col xs={1} className="text-muted fs-5">
                                                {index + 1}
                                            </Col>
                                            <Col xs={8} className="fs-5">
                                                {song.name}
                                            </Col>
                                            <Col xs={3} className="text-end fs-5">
                                                {song.duration}
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>
                                )
                            )}
                        </ListGroup>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
}

export default Playlist;