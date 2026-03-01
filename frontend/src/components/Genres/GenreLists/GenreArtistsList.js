import React, { useEffect, useState } from "react";
import {useParams} from 'react-router-dom';
import Container from "react-bootstrap/Container";
import {Card, Row, Col} from "react-bootstrap";
import { Link } from "react-router-dom";

import GenreService from '../../../services/GenreService';

const GenreArtistsList = (props) => {
    const params = useParams();
    const id = params.id;
    const [data, setData] = useState([]);
    const [error, setError] = useState('');

    useEffect(
        () => {
            GenreService.fetchGenreArtists(id)
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
                            Исполнители
                        </Card.Title>
                        <Row className="g-0">
                            {data.map(
                                (item) => {
                                    return (
                                        <Col style={{textAlign: "center"}}>
                                            <Link to={`/artists/${item.id}/`}>
                                                <Card.Img
                                                    src={`http://localhost:8000/${item.avatar}`}
                                                    style={{
                                                        borderRadius: '50%',
                                                        width: '240px',
                                                        height: '240px',
                                                        objectFit: 'cover'
                                                    }}
                                                    />
                                            </Link>
                                            <Link
                                                to={`/artists/${item.id}/`}
                                                className="text-decoration-none fs-5"
                                                style={{color: "black"}}
                                            >
                                                <Col>
                                                    {item.username}
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

export default GenreArtistsList;