import React, { useEffect, useState } from "react";
import {Card, Row, Col, ButtonGroup, Button} from 'react-bootstrap';
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";

import ArtistService from "../../services/ArtistService";

const Artists = (props) => {
    const [error, setError] = useState('');
    const [artists, setArtists] = useState([]);
    const token = localStorage.getItem('auth_token');
    const [previousPage, setPreviousPage] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [nextPage, setNextPage] = useState(null);

    useEffect(
        () => {
            ArtistService.readArtists(currentPage)
            .then(
                (response) => {
                    setArtists(response.data.results);
                    setPreviousPage(response.data.previous);
                    setNextPage(response.data.next);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        },
        [currentPage]
    )

    const onNextPageClick = () => {
        setCurrentPage(currentPage + 1);
    }

    const onPreviousPageClick = () => {
        setCurrentPage(currentPage - 1);
    }

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
        <Container>
            <div className="justify-content-center d-flex mb-3">
                <ButtonGroup>
                    {previousPage !== null ? (
                        <>
                        <Button variant="primary" onClick={onPreviousPageClick}>
                            {currentPage - 1}
                        </Button>
                        </>
                    ) : (
                        <>
                        </>
                    )}
                    <Button variant="light">
                        {currentPage}
                    </Button>
                    {nextPage !== null ? (
                        <>
                        <Button variant="primary" onClick={onNextPageClick}>
                            {currentPage + 1}
                        </Button>
                        </>
                    ) : (
                        <>
                        </>
                    )}
                </ButtonGroup>
            </div>
            <Row>
                {artists.map(
                    (artist) => (
                        <Col key={artist.id} xs={12} className="mb-3">
                            <Card style={{maxWidth: "50%", maxHeight: "100%"}} className="mx-auto">
                                <Link to={`/artists/${artist.id}/`}>
                                    <Card.Img
                                        src={artist.avatar}
                                        className="img-fluid"
                                        style={{
                                            maxHeight: '50%',
                                            maxWidth: '100%',
                                        }}
                                        />
                                </Link>
                                <Card.Body>
                                    <Card.Title className="text-center">
                                        <Link to={`/artists/${artist.id}/`} className="text-decoration-none">
                                            {artist.username}
                                        </Link>
                                    </Card.Title>
                                </Card.Body>
                            </Card>
                        </Col>
                ))}
            </Row>
            <div className="justify-content-center d-flex mb-3">
                <ButtonGroup>
                    {previousPage !== null ? (
                        <>
                        <Button variant="primary" onClick={onPreviousPageClick}>
                            {currentPage - 1}
                        </Button>
                        </>
                    ) : (
                        <>
                        </>
                    )}
                    <Button variant="light">
                        {currentPage}
                    </Button>
                    {nextPage !== null ? (
                        <>
                        <Button variant="primary" onClick={onNextPageClick}>
                            {currentPage + 1}
                        </Button>
                        </>
                    ) : (
                        <>
                        </>
                    )}
                </ButtonGroup>
            </div>
        </Container>
    )
}

export default Artists;