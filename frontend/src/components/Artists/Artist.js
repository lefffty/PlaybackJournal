import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Card, Col, Row, Container } from "react-bootstrap";

import '../Albums/Album.css';
import './Lists/ArtistList.css';

import HeartIcon from "../Common/HeartIcon/HeartIcon";

import ItemGrid from "../Common/ItemGrids/ItemGrid";
import ArtistService from '../../services/ArtistService';

const Artist = (props) => {
    const [artist, setArtist] = useState(null);
    const params = useParams();
    const id = params.id;
    const token = localStorage.getItem('auth_token');
    const [error, setError] = useState('');
    const [userArtistData, setUserArtistData] = useState({
        favourite: false,
    });

    useEffect(
        () => {
            setArtist(null);
            ArtistService.readArtist(id)
            .then(
                (response) => {
                    setArtist(response.data);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        },
        [id]
    );

    useEffect(
        () => {
            if (token){
                ArtistService.userArtist(id)
                .then(
                    (response) => {
                        setUserArtistData(response.data);
                    }
                )
            }
        },
        [id]
    )

    const onFavouriteClick = (_) => {
        setUserArtistData(
            prevstate => ({
                ...prevstate,
                favourite: !prevstate.favourite
            })
        );
        ArtistService.favouriteArtist(id)
        .catch(
            (e) => setError(e.toString())
        )
    }

    if (!artist){
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
                <Card className="mb-3 border-0">
                    <Row className="g-0">
                        <Col md={4}>
                            <Card.Img
                                src={artist.avatar}
                            />
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Row>
                                    <Col md={11} className="mb-3">
                                        <Card.Title className="fs-1">
                                            {artist.username}
                                        </Card.Title>
                                        <Card.Text>
                                            {artist.description}
                                        </Card.Text>
                                        <Card.Text className="fs-4">
                                            <span><b>Жанры</b>: </span>
                                            <span>
                                                {artist.genres.map(
                                                    (genre, index) => (
                                                        <React.Fragment>
                                                            <Link to={`/genres/${genre.id}/`} className="text-decoration-none">
                                                                {genre.name}
                                                            </Link>
                                                            {index < artist.genres.length - 1 && ', '}
                                                        </React.Fragment>
                                                    )
                                                )}
                                            </span>
                                        </Card.Text>
                                    </Col>
                                    <Col md={1}>
                                        <Row>
                                            {token == null || token === '' ? (                                            
                                                <>
                                                </>
                                            ) : (
                                                <>
                                                    <HeartIcon initialValue={userArtistData.favourite} onClick={onFavouriteClick}/>
                                                </>
                                            )}
                                        </Row>
                                    </Col>
                                </Row>
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
                <ItemGrid
                    itemId={artist.id}
                    items={artist.albums}
                    itemsName={"Альбомы"}
                    urlPath={"albums"}
                    urlPathName={"artists"}
                    kind={"discography"}
                />
                <ItemGrid
                    itemId={artist.id}
                    items={artist.similar}
                    itemsName={"Похожие исполнители"}
                    urlPathName={"artists"}
                    urlPath={"artists"}
                    kind={"similar"}
                />
            </Container>
        </div>
    )
};

export default Artist;