import React, { useEffect, useState } from "react";
import { Card, Row, Col } from "react-bootstrap";
import Container from "react-bootstrap/Container";

import AlbumService from '../services/AlbumService';
import { useLocation } from "react-router-dom";
import moment from 'moment';

const Albums = (props) => {
    const [albums, setAlbums] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(
        () => {
            AlbumService.readAlbums()
            .then(
                (response) => {
                    setAlbums(response.data.results);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
            .finally(
                () => {
                    setLoading(false);
                }
            )
        },
        []
    )

    if (loading){
        return (
            <div>
                Loading...
            </div>
        )
    };

    if (error){
        return (
            <div>
                Error: {error}
            </div>
        )
    };

    return (
        <Container>
            {albums.map(
                (album) => {
                    return (
                        <Card>
                            <Row className="g-0">
                                <Col md={4}>
                                <Card.Img
                                    src={album.album_cover}
                                />
                                </Col>
                                <Col md={8}>
                                <Card.Body>
                                    <Card.Title>
                                        {album.album_name}
                                    </Card.Title>
                                    <Card.Text>
                                        Авторы: {album.album_artists.reduce((accumulator, currentValue) => {
                                            return accumulator.concat(currentValue.artist_username);
                                        }, []).join(', ')}
                                    </Card.Text>
                                    <Card.Text>
                                        Выпущен: {moment(album.album_publication_date).format('Do MMMM YYYY')}
                                    </Card.Text>
                                    <Card.Text>
                                        Жанры: {album.album_genres.reduce((accumulator, currentValue) => {
                                            return accumulator.concat(currentValue.genre_name);
                                        }, []
                                        ).join(', ')}
                                    </Card.Text>
                                    <Card.Text>
                                        Песни: {album.album_songs.map(
                                            (album_song) => {
                                                return (
                                                    <Card.Text>
                                                        {`${album_song.song_name} - ${album_song.song_duration}`}
                                                    </Card.Text>
                                                )
                                            }
                                        )}
                                    </Card.Text>
                                </Card.Body>
                                </Col>
                            </Row>
                        </Card>
                    );
                }
            )}
        </Container>
    )
};


export default Albums;