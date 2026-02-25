import React, { useState } from "react";

import { useLocation, useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import {ListGroup, Card, Row, Col} from "react-bootstrap";
import moment from "moment";

const Album = (props) => {
    const location = useLocation();
    const params = useParams();
    const album = location.state.album;

    return (
        <div>
            <Container>
                <Card className="mb-3">
                    <Row className="g-0">
                        <Col md={4} className="d-flex">
                            <Card.Img
                                src={album.album_cover}
                            >
                            </Card.Img>
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Card.Title className="fs-1">
                                    {album.album_name}
                                </Card.Title>
                                <Card.Text className="fs-3">
                                    Исполнители: {album.album_artists.map(art => art.artist_username).join(', ')}
                                </Card.Text>
                                <Card.Text className="fs-3">                                
                                    Жанры: {album.album_genres.map(genre => genre.genre_name).join(', ')}
                                </Card.Text>
                                <Card.Text className="fs-3">
                                    Выпущен: {moment(album.album_publication_date).format('Do MMMM YYYY')} 
                                </Card.Text>
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
                            {album.album_songs.map(
                                (song, index) => (
                                    <ListGroup.Item key={song.song_id} className="px-0">
                                        <Row>
                                            <Col xs={1} className="text-muted fs-5">
                                                {index}
                                            </Col>
                                            <Col xs={8} className="fs-5">
                                                {song.song_name}
                                            </Col>
                                            <Col xs={3} className="text-end fs-5">
                                                {song.song_duration}
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
};

export default Album;