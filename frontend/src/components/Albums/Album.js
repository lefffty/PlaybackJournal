import React, {useEffect, useState} from "react";

import {useParams} from "react-router-dom";
import Container from "react-bootstrap/Container";
import {Spinner, Alert} from "react-bootstrap";

import ReviewForm from "../Reviews/Forms/ReviewForm";

import AlbumHeader from "./AlbumHeader";
import AlbumSongsList from "./AlbumSongsList";
import AlbumReviews from "./AlbumReviews";

import AlbumService from "../../services/AlbumService";
import SongService from "../../services/Song";

const Album = () => {
    const {id} = useParams();
    const [album, setAlbum] = useState(null);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');
    const isAuthenticated = token && token !== '';
    const [reviews, setReviews] = useState([]);
    const [userAlbumData, setUserAlbumData] = useState({
        favourite: false,
        listened: false,
        wishlist: false,
        rating: 0,
    });
    const [reviewsStatistics, setReviewsStatistics] = useState({
        total: 0,
        negative: 0,
        neutral: 0,
        positive: 0,
    })
    const [isStatistics, setIsStatistics] = useState(false);
    const [songsRatings, setSongsRatings] = useState({});

    const fetchAlbum = () => {
        AlbumService.readAlbum(id)
            .then(
                (response) => {
                    setAlbum(response.data);
                    const songs = response.data.songs;
                    const initialRatings = {};
                    songs.forEach(song => {
                        initialRatings[song.id] = song.rating;
                    })
                    setSongsRatings(initialRatings);
                }
            )
            .catch((e) => {
                setAlbum(s => s);
                setSongsRatings(s => s);
                setError(e.toString());
            })
    }

    const fetchUserAlbum = () => {
        AlbumService.userAlbum(id)
            .then(
                (response) => {
                    setUserAlbumData(response.data);
                }
            )
    }

    const fetchReviews = () => {
        AlbumService.fetchReviews(id)
            .then(
                (response) => {
                    const data = response.data;
                    setReviews(data);
                }
            )
            .catch(
                (e) => setError(e.toString())
            )
    }

    const fetchAlbumReviews = () => {
        AlbumService.fetchStatistics(id)
            .then(
                (response) => {
                    const data = response.data;
                    setReviewsStatistics(data);
                    if (data.total) {
                        setIsStatistics(Boolean(data.total));
                        fetchReviews();
                    }
                }
            )
            .catch(
                (e) => setError(e.toString())
            )
    }

    useEffect(
        () => {
            fetchAlbum();
            fetchAlbumReviews();
            if (isAuthenticated) fetchUserAlbum();
        },
        [id]
    )

    const handleReviewAdded = () => {
        fetchAlbumReviews();
    }

    const onSongRatingChange = (songId, value) => {
        const prevValue = songsRatings[songId];
        setSongsRatings(
            prev => ({
                ...prev,
                [songId]: value
            })
        )
        const data = {
            rating: value
        }
        SongService.rateSong(songId, data)
            .catch((e) => {
                setSongsRatings(prevState => ({...prevState, [songId]: prevValue}))
            })
    }

    const onRatingChange = (value) => {
        const prev = userAlbumData.rating;
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
            .catch((e) => {
                setUserAlbumData(s => ({...s, rating: prev}));
                setError(e.toString());
            })
    }

    const onListenedClick = () => {
        const prev = userAlbumData.listened;
        setUserAlbumData(
            prevstate => ({
                ...prevstate,
                listened: !prevstate.listened,
            })
        )
        AlbumService.listenAlbum(id)
            .catch((e) => {
                setUserAlbumData(s => ({...s, listened: prev}))
                setError(e.toString());
            })
    }

    const onWishlistClick = () => {
        const prev = userAlbumData.wishlist;
        setUserAlbumData(
            prevstate => ({
                ...prevstate,
                wishlist: !prevstate.wishlist,
            })
        )
        AlbumService.wishlistAlbum(id)
            .catch((e) => {
                setUserAlbumData(s => ({...s, wishlist: prev}));
                setError(e.toString());
            })
    }

    const onFavouriteClick = () => {
        const prev = userAlbumData.favourite;
        setUserAlbumData(
            prevstate => ({
                ...prevstate,
                favourite: !prevstate.favourite,
            })
        )
        AlbumService.favouriteAlbum(id)
            .catch((e) => {
                setUserAlbumData(state => ({...state, favourite: prev}));
                setError(e.toString());
            })
    }

    if (error) {
        return (
            <Alert>
                <Alert.Heading>
                    Error: {error}
                </Alert.Heading>
            </Alert>
        )
    }

    if (!album) {
        return (
            <Spinner animation={"grow"} variant={"primary"}/>
        )
    }

    return (
        <div>
            <Container>
                <AlbumHeader
                    isAuthenticated={isAuthenticated}
                    album={album}
                    userAlbumData={userAlbumData}
                    onRatingChange={onRatingChange}
                    onFavouriteClick={onFavouriteClick}
                    onListenedClick={onListenedClick}
                    onWishlistClick={onWishlistClick}
                />
                <AlbumSongsList
                    token={token}
                    album={album}
                    onSongRatingChange={onSongRatingChange}
                    songsRatings={songsRatings}
                />
                <AlbumReviews
                    id={album.id}
                    reviews={reviews}
                    isStatistics={isStatistics}
                    reviewsStatistics={reviewsStatistics}
                />
                {isAuthenticated && (
                    <div className="mt-3 w-50">
                        <ReviewForm albumId={id} onReviewAdded={handleReviewAdded}/>
                    </div>
                )}
            </Container>
        </div>
    )
};

export default Album;