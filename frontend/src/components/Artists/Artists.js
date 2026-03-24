import React, { useEffect, useState } from "react";
import {Card, Row, Col } from 'react-bootstrap';
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";

import Pagination from '../Common/Pagination/Pagination';
import './Artist.css';

import ArtistService from "../../services/ArtistService";

const Artists = (props) => {
    const [error, setError] = useState('');
    const [artists, setArtists] = useState([]);
    const token = localStorage.getItem('auth_token');
    const [previousPage, setPreviousPage] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [nextPage, setNextPage] = useState(null);
    const [totalItems, setTotalItems] = useState(null);
    const [maxPage, setMaxPage] = useState(null);
    const [minPage] = useState(1);
    const [itemsPerPage] = useState(10);

    useEffect(
        () => {
            ArtistService.readArtists(currentPage)
            .then(
                (response) => {
                    setArtists(response.data.results);
                    setPreviousPage(response.data.previous);
                    setNextPage(response.data.next);
                    if (!totalItems){
                        setTotalItems(response.data.count);
                        const divisionResult = response.data.count / itemsPerPage;
                        if (response.data.count % itemsPerPage === 0){
                            setMaxPage(divisionResult);
                        } else{
                            setMaxPage(Math.trunc(divisionResult) + 1);
                        }
                    }
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

    const onFirstPageClick = () => {
        setCurrentPage(minPage);
    }

    const onLastPageClick = () => {
        setCurrentPage(maxPage);
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
            <Pagination
                minPage={minPage}
                maxPage={maxPage}
                currentPage={currentPage}
                previousPage={previousPage}
                nextPage={nextPage}
                onFirstPageClick={onFirstPageClick}
                onPreviousPageClick={onPreviousPageClick}
                onNextPageClick={onNextPageClick}
                onLastPageClick={onLastPageClick}
            />
            <Row>
                {artists.map(
                    (artist) => (
                        <Col key={artist.id} xs={12} className="mb-3">
                            <Card style={{maxWidth: "50%", maxHeight: "100%"}} className="mx-auto border-0 artist-card">
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
            <Pagination
                minPage={minPage}
                maxPage={maxPage}
                currentPage={currentPage}
                previousPage={previousPage}
                nextPage={nextPage}
                onFirstPageClick={onFirstPageClick}
                onPreviousPageClick={onPreviousPageClick}
                onNextPageClick={onNextPageClick}
                onLastPageClick={onLastPageClick}
            />
        </Container>
    )
}

export default Artists;