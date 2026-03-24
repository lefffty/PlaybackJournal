import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import { Card } from 'react-bootstrap';

import './Genre.css';

import Pagination from "../Common/Pagination/Pagination";
import GenreService from "../../services/GenreService";
import { Link } from "react-router-dom";

const Genres = (props) => {
    const [genres, setGenres] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState('');
    const [previousPage, setPreviousPage] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [nextPage, setNextPage] = useState(null);
    const [totalItems, setTotalItems] = useState(null);
    const [maxPage, setMaxPage] = useState(null);
    const [minPage] = useState(1);
    const [itemsPerPage] = useState(10);

    useEffect(
        () => {
            GenreService.readGenres(currentPage)
            .then(
                (response) => {
                    setGenres(response.data.results);
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

    const onFirstPageClick = () => {
        setCurrentPage(minPage);
    }

    const onLastPageClick = () => {
        setCurrentPage(maxPage);
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
            {genres.map(
                (genre) => {
                    return (
                        <Card className="w-75 mb-3 mx-auto border-0 genre-card">
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
    );
};

export default Genres;