import React, { useEffect, useState } from "react";
import { Card, Col, Container, Row, Badge } from "react-bootstrap";
import { Link } from "react-router-dom";
import moment from "moment";

import UserService from "../../../services/UserService";
import './AlbumsList.css';

const RatedList = (props) => {
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');

    useEffect(
        () => {
            UserService.fetchRated()
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
                        Оценки
                    </Card.Title>
                    <Card.Body>
                        <Row className="g-0">
                            {data.map(
                                (item) => (
                                    (
                                        <Col className="p-0" key={item.album.id}>
                                            <div style={{position: "relative"}}>
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
                                                <div
                                                    style={{
                                                        position: 'absolute',
                                                        top: '10px',
                                                        right: '185px',
                                                        width: '40px',
                                                        height: '40px',
                                                        borderRadius: '50%',
                                                        backgroundColor: '#f5efe0',
                                                        color: '#000',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                        fontWeight: 'bold',
                                                        fontSize: '1.2rem',
                                                        boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
                                                        zIndex: 10
                                                    }}
                                                >
                                                    {item.rating}
                                                </div>
                                                <Link
                                                    to={`/albums/${item.album.id}/`}
                                                    className="text-decoration-none fs-4 d-block"
                                                    style={{color: "black"}}
                                                >
                                                        {item.album.name}
                                                </Link>
                                                </div>
                                            <div>
                                                {moment(item.album.publication_date).year()}
                                            </div>
                                        </Col>
                                    )
                                )
                            )}
                        </Row>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
};

export default RatedList;