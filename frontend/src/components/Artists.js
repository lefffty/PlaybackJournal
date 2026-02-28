import React, { useEffect, useState } from "react";
import {Card, Row, Col} from 'react-bootstrap';
import { Link } from "react-router-dom";

import ArtistService from "../services/ArtistService";

const Artists = (props) => {
    const [error, setError] = useState('');
    const [artists, setArtists] = useState([]);
    const token = localStorage.getItem('auth_token');

    useEffect(
        () => {
            ArtistService.readArtists()
            .then(
                (response) => {
                    setArtists(response.data.results);
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

    if (!artists){
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
        <Row>
            {artists.map(
                (artist) => (
                    <Col key={artist.id} xs={12} className="mb-3">
                        <Card>
                            <Link to={`/artist/${artist.id}/`}>
                                <Card.Img
                                    variant="top"
                                    src={artist.avatar}
                                />
                            </Link>
                            <Card.Body>
                                <Card.Title className="text-center">
                                    <Link to={`/artist/${artist.id}/`} className="text-decoration-none">
                                        {artist.username}
                                    </Link>
                                </Card.Title>
                            </Card.Body>
                        </Card>
                    </Col>
            ))}
        </Row>
    )
}

export default Artists;