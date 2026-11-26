import React, { useEffect, useState } from "react";
import {Link, useParams} from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import {Card, Col, Row} from 'react-bootstrap';
import {Spinner, Alert} from "react-bootstrap";

import ScaleRating from "../Common/ScaleRating/ScaleRating";
import SongService from "../../services/Song";

const Song = (props) => {
    const params = useParams();
    const id = params.id;
    const token = localStorage.getItem('auth_token');
    const [song, setSong] = useState(null);
    const [songRating, setSongRating] = useState(null);
    const [error, setError] = useState('');

    useEffect(
        () => {
            SongService.fetchSong(id)
            .then(
                (response) => {
                    setSong(response.data);
                    setSongRating(response.data.rating);
                }
            )
            .catch(
                (e) => setError(e.toString())
            )
        },
        [id]
    );

    if (error){
        return (
            <Alert data-testid="song-error">
                <Alert.Heading>
                    Error: {error}
                </Alert.Heading>
            </Alert>
        )
    }

    if (!song){
        return (
            <Spinner data-testid="song-spinner" animation={"grow"} variant={"primary"}/>
        )
    }

    return (
        <Container className="w-75 ms-0">
            <Card className="mb-3">
                <Row className="g-0">
                    <Col md={4} className="d-flex">
                        <Card.Img
                            src={song.cover}
                            data-testid="song-cover"
                        >
                        </Card.Img>
                    </Col>
                    <Col md={8}>
                        <Card.Body>
                            <Card.Title data-testid="song-title">
                                {song.name}
                            </Card.Title>
                            <Card.Text className="text-muted" data-testid="song-duration">
                                {song.duration}
                            </Card.Text>
                            {song.album != null
                                ? (
                                    <>
                                        <Card.Text>
                                            <span>From </span>
                                            <span>
                                                <Link to={`/albums/${song.album.id}`} data-testid={"song-album"} className="text-decoration-none">
                                                    {song.album.name}
                                                </Link>
                                            </span>
                                        </Card.Text>
                                    </>
                                )
                                : (
                                    <>
                                    </>
                                )
                            }
                            {token && (
                                <ScaleRating
                                    initialValue={songRating}
                                    frozen={true}
                                />
                            )}
                        </Card.Body>
                    </Col>
                </Row>
            </Card>
        </Container>
    )
}

export default Song;