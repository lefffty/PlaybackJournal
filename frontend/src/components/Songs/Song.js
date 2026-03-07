import React, { useEffect, useState } from "react";
import {Link, useParams} from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import {Card, Col, Row} from 'react-bootstrap';

import SongService from "../../services/SongService";

const Song = (props) => {
    const params = useParams();
    const id = params.id;
    const [song, setSong] = useState(null);
    const [error, setError] = useState('');

    useEffect(
        () => {
            SongService.fetchSong(id)
            .then(
                (response) => {
                    setSong(response.data);
                }
            )
            .catch(
                (e) => setError(e.toString())
            )
        },
        [id]
    );

    if (!song){
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
        <Container className="w-75 ms-0">
            <Card className="mb-3">
                <Row className="g-0">
                    <Col md={4} className="d-flex">
                        <Card.Img
                            src={song.cover}
                        >
                        </Card.Img>
                    </Col>
                    <Col md={8}>
                        <Card.Body>
                            <Card.Title>
                                {song.name}
                            </Card.Title>
                            <Card.Text className="text-muted">
                                {song.duration}
                            </Card.Text>
                            {song.album != null
                                ? (
                                    <>
                                        <Card.Text>
                                            <span>From </span>
                                            <span>
                                                <Link to={`/albums/${song.album.id}`} className="text-decoration-none">
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
                        </Card.Body>
                    </Col>
                </Row>
            </Card>
        </Container>
    )
}

export default Song;