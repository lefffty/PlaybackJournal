import React, { useEffect, useState } from "react";
import { Card, Col, Container, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
import moment from "moment";

import UserService from "../../../services/UserService";

const FavouriteList = (props) => {
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');

    useEffect(
        () => {
            UserService.fetchFavourite()
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
                    <Card.Title className="fs-1">
                        Любимые альбомы
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
                                                />
                                            </Link>
                                            <Link to={`/albums/${item.album.id}/`} className="text-decoration-none fs-4" style={{color: "black"}}>
                                                <Col>
                                                    {item.album.name}
                                                </Col>
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

export default FavouriteList;