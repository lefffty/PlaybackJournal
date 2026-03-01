import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {Card, Row, Col} from "react-bootstrap";
import Container from "react-bootstrap/Container";
import { Link } from "react-router-dom";

import ArtistService from "../../services/ArtistService";


const ArtistList = (props) => {
    const params = useParams();
    const id = params.id;
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const dataType = props.dataType;

    useEffect(
        () => {
            if (dataType === 'similar'){
                ArtistService.readSimilar(id)
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
            }
            else {
                ArtistService.readDiscography(id)
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
            }
        },
        []
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
                <Card className="mb-3">
                    <Card.Body>
                        <Card.Title className="fs-1">
                            {dataType === 'similar' ? 'Похожие исполнители' : 'Дискография'}
                        </Card.Title>
                        <Card.Body>
                            <Row className="g-0">
                                {data.map(
                                    (item) => {
                                        return (
                                            <Col style={{textAlign: "center"}}>
                                                <Link
                                                    to={dataType === 'similar'
                                                        ? `/artists/${item.id}/`
                                                        : `/albums/${item.id}/`
                                                    }
                                                >
                                                    <Card.Img
                                                        src={dataType === 'similar'
                                                            ? "http://localhost:8000" + item.avatar
                                                            : "http://localhost:8000" + item.cover
                                                        }
                                                        style={{
                                                            borderRadius: '50%',
                                                            width: '240px',
                                                            height: '240px',
                                                            objectFit: 'cover'
                                                        }}                                                        
                                                    />
                                                </Link>
                                                <Link
                                                    to={dataType === 'similar'
                                                        ? `/artists/${item.id}/`
                                                        : `/albums/${item.id}/`
                                                    }
                                                    className="text-decoration-none fs-5"
                                                    style={{color: "black"}}
                                                >
                                                    <Col>
                                                        {dataType === 'similar'
                                                            ? item.username
                                                            : item.name
                                                        }
                                                    </Col>
                                                </Link>
                                            </Col>
                                        )
                                    }
                                )}
                            </Row>
                        </Card.Body>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    );
}

export default ArtistList;