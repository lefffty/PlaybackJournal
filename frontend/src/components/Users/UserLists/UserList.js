import React, { useEffect, useState } from "react";
import { Card, Col, Container, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
import moment from "moment";

import './UserList.css';
import UserListFunction from './Utils/UserListFunction';

const UserList = ({listType, cardTitle}) => {
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');

    const fetchFunction = UserListFunction(listType);

    useEffect(
        () => {
            fetchFunction()
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
        [token]
    )

    if (error){
        return (
            <div>
                Error: {error}
            </div>
        )
    }

    const itemKey = listType.includes('Albums') ? 'album' : 'playlist';
    const showYear = listType.includes('Albums');

    return (
        <div>
            <Container>
                <Card>
                    <Card.Body>
                        <Card.Title className="fs-1 ms-3 mt-3">
                            {cardTitle}
                        </Card.Title>
                        <Row className="g-0" style={{rowGap: "10px",  gap: '90px'}}>
                            {data.map(
                                (item) => {
                                    const entity = item[itemKey];
                                    return (
                                        <Col
                                            className="p-0 flex-shrink-0 flex-grow-0"
                                            key={entity.id}
                                        >
                                            <div
                                                style={{position: "relative", width: '240px', height: '240px'}}
                                            >
                                                <Link to={`/${itemKey}s/${entity.id}/`}>
                                                    <Card.Img
                                                        src={"http://localhost:8000" + entity.cover}
                                                        style={{
                                                            borderRadius: '5%',
                                                            width: '240px',
                                                            height: '240px',
                                                            objectFit: 'cover'
                                                        }}
                                                        className="album-cover"
                                                    />
                                                </Link>
                                                {'rating' in item
                                                    ? (
                                                        <>
                                                            <div
                                                                style={{
                                                                    position: 'absolute',
                                                                    top: '10px',
                                                                    right: '10px',
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
                                                        </>
                                                    )
                                                    : (
                                                        <>
                                                        </>
                                                    )
                                                }
                                            </div>
                                            <Link
                                                to={`/${itemKey}s/${entity.id}/`}
                                                className="text-decoration-none fs-4 d-block"
                                                style={{color: "black", width: "240px"}}
                                            >
                                                <Card.Text
                                                    className="album-title"
                                                >
                                                    {entity.name}
                                                </Card.Text>
                                            </Link>
                                            {showYear && (
                                                <div>
                                                    {moment(entity.publication_date).year()}
                                                </div>
                                            )}
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

export default UserList;