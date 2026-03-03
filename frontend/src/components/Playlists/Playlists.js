import React, { useEffect, useState } from "react";
import Container from 'react-bootstrap/Container';
import { FaPlus } from "react-icons/fa";
import {Button, Card, Col, Row} from 'react-bootstrap';

import PlaylistService from '../../services/PlaylistService';
import { Link } from "react-router-dom";

const Playlists = (props) => {
    const [data, setData] = useState([]);
    const token = localStorage.getItem('auth_token');
    const [error, setError] = useState('');
    const [currentPage, setCurrentPage] = useState(1);

    useEffect(
        () => {
            PlaylistService.fetchPlaylists(currentPage)
            .then(
                (response) => {
                    setData(response.data.results);
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
            {token == null || token === ''
                ? (
                    <>
                    </>
                )
                : (
                    <div className="d-flex justify-content-end">
                        <Link to={"/playlists/create/"}>
                            <FaPlus size={30} title="Создать плейлист"/>
                        </Link>
                    </div>
                )
            }
            <div className="mb-3">
                {data.map(
                    (playlist) => {
                        return (
                            <Card className="w-75 mb-3 mx-auto">
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
        </Container>
    )
}

export default Playlists;