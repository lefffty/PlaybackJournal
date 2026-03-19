import React, { useEffect, useState } from "react";

import { Link, useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import {ListGroup, Card, Row, Col} from "react-bootstrap";
import moment from "moment";

import WishlistIcon from "../Common/WishlistIcon/WishlistIcon";
import ScaleRating from "../Common/ScaleRating/ScaleRating";
import HeartIcon from "../Common/HeartIcon/HeartIcon";
import Headphones from "../Common/Headphones/Headphones";

import Review from "../Reviews/Review";
import Reviews from "../Statistics/Reviews/Reviews";

import AlbumService from "../../services/AlbumService";
import SongService from "../../services/SongService";

const Album = (props) => {
    const params = useParams();
    const id = params.id;
    const [album, setAlbum] = useState(null);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');
    const [userAlbumData, setUserAlbumData] = useState({
        favourite: false,
        listened: false,
        wishlist: false,
        rating: 0,
    });
    const [reviewsStatistics, setReviewsStatistics] = useState({
        negative: 0,
        neutral: 0,
        positive: 0,  
    })
    const [isStatistics, setIsStatistics] = useState(false);
    const [userSongsData, setUserSongsData] = useState({});

    useEffect(
        () => {
            AlbumService.readAlbum(id)
            .then(
                (response) => {
                    setAlbum(response.data);
                    const songs = response.data.songs;
                    const initialRatings = {};
                    songs.forEach(song => {
                        initialRatings[song.id] = song.rating;
                    })
                    const statistics = response.data.statistics;
                    if (statistics.total !== 0){
                        setReviewsStatistics(statistics);
                        setIsStatistics(true);
                    }
                    setUserSongsData(initialRatings);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        }, [id]
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
        }, [id]
    )

    const onSongRatingChange = (songId, value) => {
        const data = {
            rating: value
        }

        setUserSongsData(
            prev => ({
                ...prev,
                [songId]: value
            })
        )

        SongService.rateSong(songId, data)
        .catch(
            e => setError(e.toString())
        )
    }

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
        AlbumService.listenAlbum(id)
        .catch(
            (e) => {
                console.log(e.toString());
            }
        )
    }

    const onWishlistClick = (_) => {
        setUserAlbumData(
            prevstate => ({
                ...prevstate,
                wishlist: !prevstate.wishlist,
            })
        )
        AlbumService.wishlistAlbum(id)
        .catch(
            e => setError(e.toString())
        )
    }

    const onFavouriteClick = (_) => {
        setUserAlbumData(
            prevstate => ({
                ...prevstate,
                favourite: !prevstate.favourite,
            })
        )
        AlbumService.favouriteAlbum(id)
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
                <Card className="mb-3 border-0">
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
                                    <Col md={8} className="mb-3">
                                        <Card.Title className="fs-1">
                                            {album.name}
                                        </Card.Title>
                                        <Card.Text className="fs-3">
                                            <span className="text-muted fs-5">Исполнители: </span>
                                            <span>{album.artists.map(
                                                (artist, index) => (
                                                    <React.Fragment>
                                                        <Link
                                                            className="text-decoration-none"
                                                            to={`/artists/${artist.id}/`}
                                                            >
                                                            {artist.username}
                                                        </Link>
                                                        {index < album.artists.length - 1 && ', '}
                                                        </React.Fragment>
                                                )
                                            )}
                                            </span>
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
                                                    <WishlistIcon initialValue={userAlbumData.wishlist} onClick={onWishlistClick}/>
                                                    <HeartIcon initialValue={userAlbumData.favourite} onClick={onFavouriteClick}/>
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
                <Card className="mb-3 border-0">
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
                                                {index + 1}
                                            </Col>
                                            <Col xs={5} className="fs-5">
                                                <Link to={`/songs/${song.id}/`} className="text-decoration-none">
                                                    {song.name}
                                                </Link>
                                            </Col>
                                            <Col xs={5}>
                                            {token ? (
                                                <ScaleRating
                                                    initialValue={userSongsData[song.id]}
                                                    onRatingChange={(value) => onSongRatingChange(song.id, value)}
                                                />
                                            ):
                                                (
                                                <>
                                                </>
                                            )}
                                            </Col>  
                                            <Col xs={1} className="text-end fs-5">
                                                {song.duration}
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>
                                )
                            )}
                        </ListGroup>
                    </Card.Body>
                </Card>
                {isStatistics === true ? (
                    <>
                        <Card.Title className="mb-3 fs-3">
                            Рецензии слушателей
                        </Card.Title>
                        <Row className="g-0">
                            <Col md={8} className="pe-3">
                                {album.reviews.map(
                                    (review) => <Review review={review} albumId={id}/>
                                )}
                            </Col>
                            <Col md={4} className="statistics-block" style={{top: '20px'}}>
                                <Reviews stats={reviewsStatistics} />
                            </Col>
                        </Row>
                    </>
                ) : (
                    <>
                    </>
                )}

            </Container>
        </div>
    )
};

export default Album;