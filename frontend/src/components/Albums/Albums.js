import React, { useEffect, useState } from "react";
import { Card, Row, Col } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import { Link } from "react-router-dom";
import moment from 'moment';

import Pagination from "../Common/Pagination/Pagination";
import AlbumService from '../../services/AlbumService';

const Albums = (props) => {
    const [albums, setAlbums] = useState([]);
    const [loading, setLoading] = useState(true);
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
            AlbumService.readAlbums(currentPage)
            .then(
                (response) => {
                    setAlbums(response.data.results);
                    setNextPage(response.data.next);
                    setPreviousPage(response.data.previous);
                    if (!totalItems){
                        setTotalItems(response.data.count);
                        const divisionResult = response.data.count / itemsPerPage;
                        if (response.data.count % itemsPerPage === 0){
                            setMaxPage(divisionResult)
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
                Loading...
            </div>
        )
    };

    if (error){
        return (
            <div>
                Error: {error}
            </div>
        )
    };

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
            {albums.map(
                (album) => {
                    return (
                        <Card
                            className="w-75 mb-3 mx-auto border-0 album-card"
                            style={{
                                backgroundColor: '#f0f0f0b7'
                            }}
                        >
                            <Row className="g-0">
                                <Col md={4}>
                                <Card.Img
                                    src={album.cover}
                                />
                                </Col>
                                <Col md={8}>
                                    <Card.Body>
                                        <Card.Title className="fs-2">
                                            <Link to={`/albums/${album.id}/`} className="text-decoration-none">
                                                {album.name}
                                            </Link>

                                        </Card.Title>
                                        <Card.Text className="fs-4">
                                            <span className="text-muted fs-6">Авторы: </span>
                                            <span>
                                                {album.artists.map(
                                                    (artist, index) => (
                                                        <React.Fragment>
                                                            <Link to={`/artists/${artist.id}/`} className="text-decoration-none">
                                                                {artist.username}
                                                            </Link>
                                                            {index < album.artists.length - 1 && ', '}
                                                        </React.Fragment>
                                                    )
                                                )}
                                            </span>
                                        </Card.Text>
                                        <Card.Text className="fs-4">
                                            <span className="text-muted fs-6">Выпущен: </span>
                                            <span>
                                                {moment(album.publication_date).format('Do MMMM YYYY')}
                                            </span>
                                        </Card.Text>
                                        <Card.Text className="fs-4">
                                            <span className="text-muted fs-6">Жанры: </span>
                                            <span>
                                                {album.genres.map(
                                                    (genre, index) => (
                                                        <React.Fragment>
                                                            <Link to={`/genres/${genre.id}/`} className="text-decoration-none">
                                                                {genre.name}
                                                            </Link>
                                                            {index < album.genres.length - 1 && ', '}
                                                        </React.Fragment>
                                                    )
                                                )}
                                            </span>
                                        </Card.Text>
                                    </Card.Body>
                                </Col>
                            </Row>
                        </Card>
                    );
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
    )
};


export default Albums;