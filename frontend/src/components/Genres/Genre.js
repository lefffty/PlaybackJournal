import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import { useParams, } from "react-router-dom";
import { Card, Row, Col } from "react-bootstrap";

import GenreService from "../../services/GenreService";
import './Genre.css';

import ItemGrid from "../Common/ItemGrids/ItemGrid";
import HeartIcon from "../Common/HeartIcon/HeartIcon";

const Genre = (props) => {
    const {id} = useParams();
    const token = localStorage.getItem('auth_token');
    const isAuthenticated = token && token !== '';

    const [genre, setGenre] = useState(null);
    const [userGenreData, setUserGenreData] = useState({
        favourite: false,
    });
    const [error, setError] = useState('');

    useEffect(
        () => {
            GenreService.readGenre(id)
                .then((response) => { setGenre(response.data)} )
                .catch((e) => { setError(e.toString()) });
        },
        [id]
    )

    useEffect(
        () => {
            if (isAuthenticated){
                GenreService.userGenre(id)
                .then(
                    (response) => {
                        setUserGenreData(response.data);
                    }
                )
                .catch(
                    (e) => {
                        setError(e.toString());
                    }
                )
            }
        },
        [id, isAuthenticated]
    )

    const onFavouriteClick = (_) => {
        setUserGenreData(
            (prevstate) => ({
                ...prevstate,
                favourite: !prevstate.favourite,
            })
        )
        GenreService.favouriteGenre(id)
        .catch(
            e => setError(e.toString())
        )
    }

    if (!genre){
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
                    <Card.Body>
                        <Row md={2}>
                            <Col md={9}>
                                <Card.Title className="fs-2">
                                    {genre.name}
                                </Card.Title>
                                <Card.Text className="fs-4">
                                    {genre.description != null && genre.description !== ''
                                        ? (
                                            <>
                                                {genre.description}
                                            </>
                                        )
                                        : (
                                            <>
                                                <div className="ms-3">
                                                    Описания пока нет
                                                </div>
                                            </>
                                        )
                                    }
                                </Card.Text>
                            </Col>
                            <Col md={2}>
                                {isAuthenticated && (
                                        <>
                                            <HeartIcon initialValue={userGenreData.favourite} onClick={onFavouriteClick}/>
                                        </>
                                    )
                                }
                            </Col>
                        </Row>
                        <ItemGrid
                            itemId={genre.id}
                            urlPathName={"genre"}
                            items={genre.artists}
                            itemsName={"Исполнители"}
                            urlPath={"artists"}
                            kind={"artists"}
                        />
                        <ItemGrid
                            itemId={genre.id}
                            urlPathName={"genre"}
                            items={genre.albums}
                            itemsName={"Альбомы"}
                            urlPath={"albums"}
                            kind={"albums"}
                        />
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
}

export default Genre;
