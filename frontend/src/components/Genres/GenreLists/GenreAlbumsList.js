import React, { useEffect, useState } from "react";
import {useParams} from 'react-router-dom';
import Container from "react-bootstrap/Container";
import {Card, Row, Col} from "react-bootstrap";
import { Link } from "react-router-dom";

import GenreService from '../../../services/GenreService';

import './GenreAlbumsList.css';

const GenreAlbumsList = (props) => {
    const params = useParams();
    const id = params.id;
    const [data, setData] = useState([]);
    const [error, setError] = useState('');

    useEffect(
        () => {
            GenreService.fetchGenreAlbums(id)
            .then(
                (response) => {
                    setData(response.data);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        },
        [id]
    )

    if (!data){
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
        <div>
            <Container>
                <Card>
                    <Card.Body>
                        <Card.Title className="fs-1">
                            Альбомы
                        </Card.Title>
                        <Row className="g-0">
                            {data.map(
                                (item) => {
                                    return (
                                        <Col style={{textAlign: "center"}}>
                                            <Link to={`/albums/${item.id}/`}>
                                                <Card.Img
                                                    src={`http://localhost:8000/${item.cover}`}
                                                    style={{
                                                        borderRadius: '5%',
                                                        width: '200px',
                                                        height: '200px',
                                                        objectFit: 'cover'
                                                    }}
                                                    className="album-cover"
                                                    />
                                            </Link>
                                            <Link
                                                to={`/albums/${item.id}/`}
                                                className="text-decoration-none fs-5"
                                                style={{color: "black"}}
                                            >
                                                <Col>
                                                    {item.name}
                                                </Col>
                                            </Link>
                                        </Col>
                                    )
                                }
                            )}
                        </Row>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
}

export default GenreAlbumsList;