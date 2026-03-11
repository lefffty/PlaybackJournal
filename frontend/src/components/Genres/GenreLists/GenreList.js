import React, { useEffect, useState } from "react";
import { Card, Row, Col, Container } from "react-bootstrap";
import {useParams, Link} from 'react-router-dom';
import moment from "moment";

import './GenreList.css';
import GenreListFunction from './Utils/GenreListFunction';

const GenreList = ({listType, cardTitle}) => {
    const params = useParams();
    const id = params.id;
    const [data, setData] = useState([]);
    const [error, setError] = useState('');

    const fetchFunction = GenreListFunction(listType);

    useEffect(
        () => {
            fetchFunction(id)
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

    const path = listType.includes('Albums') ? 'album' : 'artist';
    const nameKey = listType.includes('Albums') ? 'name' : 'username';
    const imageKey = listType.includes('Albums') ? 'cover' : 'avatar';
    const imageBorderRadius = listType.includes('Albums') ? '5%' : '50%';
    const textAlignment = listType.includes('Albums') ? 'left' : 'center';
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
                                    return (
                                        <Col
                                            style={{textAlign: textAlignment}}
                                            className="p-0 flex-shrink-0 flex-grow-0"
                                            key={item.id}
                                        >
                                            <Link to={`/${path}s/${item.id}/`}>
                                                <Card.Img
                                                    src={`http://localhost:8000/${item[imageKey]}`}
                                                    style={{
                                                        borderRadius: imageBorderRadius,
                                                        width: '240px',
                                                        height: '240px',
                                                        objectFit: 'cover'
                                                    }}
                                                    className="album-cover"
                                                    />
                                            </Link>
                                            <Link
                                                to={`/${path}s/${item.id}/`}
                                                className="text-decoration-none fs-5"
                                                style={{color: "black"}}
                                            >
                                                <Col>
                                                    {item[nameKey]}
                                                </Col>
                                            </Link>
                                            {showYear && (
                                                <div>
                                                    {moment(item.publication_date).year()}
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
}


export default GenreList;