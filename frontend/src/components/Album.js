import React, { useEffect, useState } from "react";

import { Link, useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import {ListGroup, Card, Row, Col} from "react-bootstrap";
import moment from "moment";

import ScaleRating from "./ScaleRating";
import HeartIcon from "./HeartIcon";
import Headphones from "./Headphones";

import AlbumService from "../services/AlbumService";

const Album = (props) => {
    const params = useParams();
    const id = params.id;
    const [album, setAlbum] = useState(null);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');
    const [userAlbumData, setUserAlbumData] = useState({
        liked: false,
        listened: false,
        rating: 0,
    });

    useEffect(
        () => {
            AlbumService.readAlbum(id)
            .then(
                (response) => {
                    setAlbum(response.data);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        }, []
    )

    useEffect(
        () => {
            if (token){
                AlbumService.userAlbum(id)
                .then(
                    (response) => {
                        setUserAlbumData(response.data);
                    }
                )
            }
        }, [token, id]
    )

    const onRatingChange = (value) => {
        setUserAlbumData(
            prevstate => ({
                ...prevstate,
                rating: value
            })
        );
        const data = {
            rating: value,
        }
        AlbumService.rateAlbum(id, data)
        .catch(
            (e) => {
                console.log(e.toString());
            }
        )
    }

    const onListenedClick = (_) => {
        setUserAlbumData(
            prevstate => ({
                ...prevstate,
                listened: !prevstate.listened,
            })
        )
        AlbumService.listenAlbum(album.id)
        .catch(
            (e) => {
                console.log(e.toString());
            }
        )
    }

    const onLikedClick = (_) => {
        setUserAlbumData(
            prevstate => ({
                ...prevstate,
                liked: !prevstate.liked,
            })
        )
        AlbumService.favouriteAlbum(album.id)
        .catch(
            (e) => {
                console.log(e.toString());
            }
        )
    }

    if (!album){
        return (
            <div>
                Loading
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
                    <Row className="g-0">
                        <Col md={4} className="d-flex">
                            <Card.Img
                                src={album.cover}
                            >
                            </Card.Img>
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Row>
                                <Col md={8}>
                                    <Card.Title className="fs-1">
                                        {album.name}
                                    </Card.Title>
                                    <Card.Text className="fs-3">
                                        <span className="text-muted fs-5">Исполнители: </span>
                                        <span>{album.artists.map(art => art.username).join(', ')}</span>
                                    </Card.Text>
                                    <Card.Text className="fs-3">
                                        <span className="text-muted fs-5">Жанры: </span>
                                        <span>
                                            {album.genres.map(
                                                (genre, index) => (
                                                    <React.Fragment>
                                                        <Link to={`/genres/${genre.id}/`} className="text-decoration-none">
                                                            {genre.name}
                                                        </Link>
                                                        {index < album.genres.length - 1 && ', '}
                                                    </React.Fragment>
                                                )
                                            )}
                                        </span>
                                    </Card.Text>
                                    <Card.Text className="fs-3">
                                        <span className="text-muted fs-5">Выпущен: </span>
                                        <span>{moment(album.publication_date).format('Do MMMM YYYY')}</span>
                                    </Card.Text>
                                    <Card.Text className="fs-3">
                                        <span className="text-muted fs-5">Средняя оценка: </span>
                                        <span>
                                            {album.average_rating !== "-" ? (
                                                Intl.NumberFormat("en", {maximumFractionDigits: 2}).format(album.average_rating))
                                                : (
                                                    "-"
                                                )
                                            } / 10.0
                                        </span>
                                    </Card.Text>
                                </Col>
                                <Col md={3}>
                                    <Row md={3}>
                                        {token == null || token === '' ? (                                            
                                            <>
                                            </>
                                        ) : (
                                            <>
                                                <HeartIcon initialValue={userAlbumData.liked} onClick={onLikedClick}/>
                                                <Headphones initialValue={userAlbumData.listened} onClick={onListenedClick}/>
                                            </>
                                        )}
                                    </Row>
                                </Col>
                                </Row>
                                {token == null || token === '' ? (
                                    <>
                                    </>
                                ) : (
                                    <>
                                        <ScaleRating initialValue={userAlbumData.rating} totalStars={10} onRatingChange={onRatingChange}/>
                                    </>
                                )}
                            </Card.Body>
                        </Col>
                    </Row>
                </Card>
                <Card>
                    <Card.Body>
                        <ListGroup variant="flush">
                            <Card.Title>
                                Список песен:
                            </Card.Title>
                            {album.songs.map(
                                (song, index) => (
                                    <ListGroup.Item key={song.id} className="px-0">
                                        <Row>
                                            <Col xs={1} className="text-muted fs-5">
                                                {index}
                                            </Col>
                                            <Col xs={8} className="fs-5">
                                                {song.name}
                                            </Col>
                                            <Col xs={3} className="text-end fs-5">
                                                {song.duration}
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>
                                )
                            )}
                        </ListGroup>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
};

export default Album;