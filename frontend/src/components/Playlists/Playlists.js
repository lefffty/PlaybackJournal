import React, { useEffect, useState } from "react";
import Container from 'react-bootstrap/Container';
import { FaPlus } from "react-icons/fa";
import { Card, Col, Row } from 'react-bootstrap';

import './Playlist.css';

import Pagination from "../Common/Pagination/Pagination";
import PlaylistService from '../../services/PlaylistService';
import { Link } from "react-router-dom";

const Playlists = (props) => {
    const [data, setData] = useState([]);
    const token = localStorage.getItem('auth_token');
    const isAuthenticated = token && token !== '';
    const [error, setError] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [nextPage, setNextPage] = useState(null);
    const [previousPage, setPreviousPage] = useState(null);
    const [totalItems, setTotalItems] = useState(null);
    const [maxPage, setMaxPage] = useState(null);
    const [minPage] = useState(1);
    const [itemsPerPage] = useState(10);

    useEffect(
        () => {
            PlaylistService.fetchPlaylists(currentPage)
            .then(
                (response) => {
                    setData(response.data.results);
                    setNextPage(response.data.next);
                    setPreviousPage(response.data.previous);
                    if (!totalItems){
                        setTotalItems(response.data.count);
                        setMaxPage(Math.trunc(response.data.count / itemsPerPage) + 1);
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

    if (!data){
        return (
            <Container>
                Loading...
            </Container>
        )
    }

    if (error){
        return (
            <Container>
                {error}
            </Container>
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
            {isAuthenticated && (
                <div className="d-flex justify-content-end">
                    <Link to={"/playlists/create/"}>
                        <FaPlus size={30} title="Создать плейлист"/>
                    </Link>
                </div>
            )}
            <div className="mb-3">
                {data.map(
                    (playlist) => {
                        return (
                            <Card className="w-75 mb-3 mx-auto playlist-card border-0">
                                <Row className="g-0">
                                    <Col md={4}>
                                        <Card.Img
                                            src={playlist.cover}
                                            style={{
                                                aspectRatio: '1 / 1',
                                                objectFit: 'cover',
                                            }}
                                        />
                                    </Col>
                                    <Col md={8}>
                                        <Card.Body>
                                            <Link to={`/playlists/${playlist.id}/`} className="text-decoration-none">
                                                <Card.Title className="fs-2">
                                                    {playlist.name}
                                                </Card.Title>
                                            </Link>
                                            <Card.Text>
                                                <span className="text-muted fs-4">Автор: </span>
                                                <span className="fs-4">
                                                    <b>@{playlist.author.username}</b>
                                                </span>
                                            </Card.Text>
                                            <Card.Text>
                                                <span className="text-muted fs-4">Описание: </span>
                                                <span className="fs-4">{playlist.description}</span>
                                            </Card.Text>
                                        </Card.Body>
                                    </Col>
                                </Row>
                            </Card>
                        )
                    }
                )}
            </div>
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

export default Playlists;