import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import {Card, ButtonGroup, Button} from 'react-bootstrap';

import GenreService from "../../services/GenreService";
import { Link } from "react-router-dom";

const Genres = (props) => {
    const [genres, setGenres] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState('');
    const [previousPage, setPreviousPage] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [nextPage, setNextPage] = useState(null);

    useEffect(
        () => {
            GenreService.readGenres(currentPage)
            .then(
                (response) => {
                    setGenres(response.data.results);
                    setPreviousPage(response.data.previous);
                    setNextPage(response.data.next);
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
        [currentPage]
    )

    const onNextPageClick = () => {
        setCurrentPage(currentPage + 1);
    }

    const onPreviousPageClick = () => {
        setCurrentPage(currentPage - 1);
    }

    if (loading){
        return (
            <div>
                Loading
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
            {genres.map(
                (genre) => {
                    return (
                        <Card className="w-75 mb-3 mx-auto">
                            <Card.Body>
                                <Card.Title>
                                    <Link to={`/genres/${genre.id}/`} className="text-decoration-none">
                                        {genre.name}
                                    </Link>
                                </Card.Title>
                                <Card.Text>
                                    {genre.description}
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    )
                }
            )}
            <div className="justify-content-center d-flex">
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
    );
};

export default Genres;