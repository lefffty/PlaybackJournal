import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {Card, Row, Col} from "react-bootstrap";
import Container from "react-bootstrap/Container";
import { Link } from "react-router-dom";
import moment from "moment";

import ArtistService from "../../services/ArtistService";

import './ArtistList.css';

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

    const alignText = dataType === 'similar' ? 'center' : 'left';
    const showArtists = dataType === 'similar' ? false : true;

    var border_radius = '';
    if (dataType === 'similar'){
        border_radius = '50%';
    } else{
        border_radius = '5%';
    }

    return (
        <div>
            <Container>
                <Card className="mb-3">
                    <Card.Body>
                        <Card.Title className="fs-1 ms-2 mt-3">
                            {dataType === 'similar' ? 'Похожие исполнители' : 'Дискография'}
                        </Card.Title>
                        <Row className="g-0 ms-2" style={{rowGap: "10px",  gap: '90px'}}>
                            {data.map(
                                (item) => {
                                    return (
                                        <Col
                                            className="p-0 flex-shrink-0 flex-grow-0"
                                        >
                                            <div
                                                style={{position: "relative", width: '240px', height: '240px'}}
                                            >
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
                                                            borderRadius: border_radius,
                                                            width: '240px',
                                                            height: '240px',
                                                            objectFit: 'cover'
                                                        }}
                                                        className="album-cover"
                                                    />
                                                </Link>
                                            </div>
                                            <Link
                                                to={dataType === 'similar'
                                                    ? `/artists/${item.id}/`
                                                    : `/albums/${item.id}/`
                                                }
                                                className="text-decoration-none fs-4 d-block"
                                                style={{color: "black", width: "240px"}}
                                            >
                                                <Card.Text
                                                    className="album-title"
                                                    style={{
                                                        textAlign: alignText
                                                    }}
                                                >
                                                    {dataType === 'similar'
                                                        ? item.username
                                                        : item.name
                                                    }
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
                                            {dataType === 'similar'
                                                ? <>
                                                </>
                                                :
                                                <>
                                                    <div>
                                                        {moment(item.publication_date).year()}
                                                    </div>
                                                </>
                                            }
                                        </Col>
                                    )
                                }
                            )}
                        </Row>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    );
}

export default ArtistList;