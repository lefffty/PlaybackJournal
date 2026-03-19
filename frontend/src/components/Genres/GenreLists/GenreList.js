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
    const showArtists = listType.includes('Albums');

    return (
        <div>
            <Container>
                <Card className="border-0">
                    <Card.Body>
                        <Card.Title className="fs-1 ms-3 mt-3">
                            {cardTitle}
                        </Card.Title>
                        <Row className="g-0 mt-4 ms-2" style={{rowGap: "10px",  gap: '90px'}}>
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
                                                className="text-decoration-none fs-4"
                                                style={{color: "black"}}
                                            >
                                                <Card.Text className="mb-0">
                                                    {item[nameKey]}
                                                </Card.Text>
                                            </Link>
                                            {showArtists && (
                                                <span>
                                                    {item.artists.map(
                                                        (artist, index) => (
                                                            <React.Fragment>
                                                                <Link
                                                                    to={`/artists/${artist.id}/`}
                                                                    className="text-muted text-decoration-none"
                                                                >
                                                                    {artist.username}
                                                                </Link>
                                                                {index < item.artists.length - 1 && ', '}
                                                            </React.Fragment>
                                                        )
                                                    )}
                                                </span>
                                            )}
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