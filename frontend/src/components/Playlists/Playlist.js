import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import {Link, useNavigate, useParams} from 'react-router-dom';
import {Card, Row, Col, ListGroup, Button, Modal} from 'react-bootstrap';

import PlaylistService from "../../services/PlaylistService";
import UserService from "../../services/UserService";

const Playlist = (props) => {
    const params = useParams();
    const [show, setShow] = useState(false);
    const id = params.id;
    const token = localStorage.getItem('auth_token');
    const [userId, setUserId] = useState(null);
    const [playlist, setPlaylist] = useState(null);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(
        () => {
            PlaylistService.fetchPlaylist(id)
            .then(
                (response) => {
                    setPlaylist(response.data);
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

    useEffect(
        () => {
            if (token){
                UserService.profile()
                .then(
                    (response) => {
                        setUserId(response.data.id);
                    }
                )
                .catch(
                    (e) => {
                        setError(e.toString());
                    }
                )
            }
        },
        [id]
    )

    const onDeleteBtnClick = () => {
        PlaylistService.deletePlaylist(id)
        .then(
            (_) => {
                navigate('/playlists/');
            }
        )
    }

    const onCloseHandle = () => setShow(false);
    const onOpenHandle = () => setShow(true);

    if (!playlist){
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
            <Container className="w-75">
                <Card className="mb-3">
                    <Row className="g-0">
                        <Col md={4} className="d-flex">
                            <Card.Img
                                src={playlist.cover}
                            >
                            </Card.Img>
                        </Col>
                        <Col md={8}>
                            <Card.Body>
                                <Row>
                                    <Col md={8}>
                                        <Card.Title className="fs-1">
                                            {playlist.name}
                                        </Card.Title>
                                        <Card.Text className="fs-3">
                                            <span className="text-muted fs-4">Автор: </span>
                                            <span className="fs-3">
                                                <b>@{playlist.author.username}</b>
                                            </span>
                                        </Card.Text>
                                        <Card.Text className="fs-3">
                                            <span className="text-muted fs-4">Описание: </span>
                                            <span>{playlist.description}</span>
                                            
                                        </Card.Text>
                                        {userId === playlist.author.id
                                            ? (
                                                <>
                                                    <Button className="me-2" onClick={onOpenHandle}>
                                                        Удалить плейлист
                                                    </Button>

                                                    <Modal show={show} onHide={onCloseHandle}>
                                                        <Modal.Header closeButton>
                                                            <Modal.Title>Подтверждение</Modal.Title>
                                                        </Modal.Header>
                                                        <Modal.Body>Вы уверены, что хотите удалить плейлист?</Modal.Body>
                                                        <Modal.Footer>
                                                            <Button variant="primary" onClick={onDeleteBtnClick}>
                                                                Да
                                                            </Button>
                                                            <Button variant="secondary" onClick={onCloseHandle}>
                                                                Нет
                                                            </Button>
                                                        </Modal.Footer>
                                                    </Modal>
                                                </>
                                            )
                                            : (
                                                <>
                                                </>
                                            )
                                        }
                                    </Col>
                                </Row>
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
                            {playlist.songs.map(
                                (song, index) => (
                                    <ListGroup.Item key={song.id} className="px-0">
                                        <Row>
                                            <Col xs={1} className="text-muted fs-5">
                                                {index + 1}
                                            </Col>
                                            <Col xs={8} className="fs-5">
                                                <Link to={`/songs/${song.id}/`} className="text-decoration-none">
                                                    {song.name}
                                                </Link>
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
}

export default Playlist;