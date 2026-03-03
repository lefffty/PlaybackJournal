import React, { useEffect, useState } from "react";
import Container from 'react-bootstrap/Container';
import Alert from "react-bootstrap/Alert";
import { Link, useNavigate } from "react-router-dom";
import { Form, Card, ListGroup, ListGroupItem, Button } from "react-bootstrap";

import SongService from '../../services/SongService';
import PlaylistService from '../../services/PlaylistService';


const CreatePlaylist = (props) => {
    const token = localStorage.getItem('auth_token');
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        cover: '',
        songs: [],
    })
    const navigate = useNavigate();
    const [coverFile, setCoverFile] = useState(null);
    const [error, setError] = useState('');
    const [songs, setSongs] = useState([]);
    const [query, setQuery] = useState('');
    const [filteredSongs, setFilteredSongs] = useState([]);
    const [showDropDown, setShowDropDown] = useState(false);

    useEffect(
        () => {
            SongService.fetchSongs()
            .then(
                (response) => {
                    setSongs(response.data);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        },
        []
    );

    useEffect(
        () => {
            console.log(formData);
        },
        [formData]
    )

    const handleChange = (e) => {
        const value = e.target.value;
        setQuery(value);

        if (value.trim()){
            const filtered = songs.filter(
                (song) => song.name.toLowerCase().includes(value.toLowerCase())
            );
            setFilteredSongs(filtered);
            setShowDropDown(true);
        }
        else{
            setFilteredSongs([]);
            setShowDropDown(false);
        }
    }

    const handleSelect = (song) => {
        if (!formData.songs.some(s => s.id === song.id)){
            setFormData({
                ...formData,
                songs: [...formData.songs, {
                    id: song.id,
                    name: song.name,
                }]
            });
        }
        setQuery('');
        setShowDropDown(false);
    }

    const removeSong = (songId) => {
        setFormData({
            ...formData,
            songs: formData.songs.filter(s => s.id !== songId),
        });
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        const data = {
            name: formData.name,
            description: formData.description,
            cover: formData.cover,
            songs: formData.songs.map((s) => ({id: s.id}))
        }
        PlaylistService.createPlaylist(formData)
        .then(
            (_) => {
                navigate('/playlists/')
            }
        )
    }

    const onCoverFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setCoverFile(file);

        const reader = new FileReader();
        reader.onload = () => {
            setFormData({...formData, cover: reader.result});
        }

        reader.readAsDataURL(file);
    }

    return (
        <Container>
        {token == null || token === ''
            ? (
                <Alert variant="warning">
                    You are not logged in. Please <Link to={"/login/"}>login</Link>.
                </Alert>
            )
            : (
                <Card>
                    <Card.Header><b>Создать плейлист</b></Card.Header>
                    <Card.Body>
                        <Form>
                            <Form.Group className="mb-3">
                                <Form.Label>
                                    Название плейлиста
                                </Form.Label>
                                <Form.Control
                                    type="text"
                                    value={formData.name}
                                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>
                                    Описание плейлиста
                                </Form.Label>
                                <Form.Control
                                    as={"textarea"}
                                    value={formData.description}
                                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>
                                    Обложка
                                </Form.Label>
                                <Form.Control
                                    type="file"
                                    accept=".png, .jpg"
                                    onChange={onCoverFileChange}
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>
                                    Песни
                                </Form.Label>
                                <Form.Control
                                    type="text"
                                    value={query}
                                    onChange={handleChange}
                                    placeholder="Поиск песен..."
                                />
                                {showDropDown && filteredSongs.length > 0 && (
                                    <ListGroup
                                        style={{
                                            position: 'absolute',
                                            width: '100%',
                                            maxHeight: '200px',
                                            overflowY: 'auto',
                                            zIndex: 1000
                                        }}
                                    >
                                        {filteredSongs.map(
                                            (song) => (
                                                <ListGroupItem
                                                    key={song.id}
                                                    action
                                                    onClick={() => handleSelect(song)}
                                                >
                                                    {song.name}
                                                </ListGroupItem>
                                            )
                                        )}
                                    </ListGroup>
                                )}

                                {formData.songs.length > 0 && (
                                    <ListGroup className="mt-2">
                                        {formData.songs.map(
                                            (song) => (
                                                <ListGroup.Item key={song.id} className="d-flex justify-content-between align-items-center">
                                                    {song.name}
                                                    <Button variant="outline-danger" size="sm" onClick={() => removeSong(song.id)}>
                                                        ✕
                                                    </Button>
                                                </ListGroup.Item>
                                            )
                                        )}
                                    </ListGroup>
                                )}
                            </Form.Group>
                            <Button type="submit" onClick={handleSubmit}>
                                Создать
                            </Button>
                        </Form>
                    </Card.Body>
                </Card>
            )
        }
        </Container>
    )
};

export default CreatePlaylist;