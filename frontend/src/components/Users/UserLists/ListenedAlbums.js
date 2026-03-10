import React, { useEffect, useState } from "react";
import { Card, Container, Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import moment from "moment";

import UserService from "../../../services/UserService";
import './AlbumsList.css';

const ListenedAlbums = (props) => {
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');

    useEffect(
        () => {
            UserService.fetchListenedAlbums()
            .then(
                (response) => {
                    setData(response.data);
                }
            )
        },
        [token],
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
                    <Card.Title className="fs-1 ms-3 mt-3">
                        Прослушанные альбомы
                    </Card.Title>
                    <Card.Body>
                        <Row className="g-0">
                            {data.map(
                                (item) => {
                                    return (
                                        <Col>
                                            <Link to={`/albums/${item.album.id}/`}>
                                                <Card.Img
                                                    src={"http://localhost:8000" + item.album.cover}
                                                    style={{
                                                        borderRadius: '5%',
                                                        width: '240px',
                                                        height: '240px',
                                                        objectFit: 'cover'
                                                    }}
                                                    className="album-cover"
                                                />
                                            </Link>
                                            <Link to={`/albums/${item.album.id}/`} className="text-decoration-none fs-4" style={{color: "black"}}>
                                                    <Card.Text
                                                        className="album-title"
                                                    >
                                                        {item.album.name}
                                                    </Card.Text>
                                            </Link>
                                            <Col>
                                                {moment(item.album.publication_date).year()}
                                            </Col>
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
};

export default ListenedAlbums;