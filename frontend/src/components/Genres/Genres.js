import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import {Card} from 'react-bootstrap';

import GenreService from "../../services/GenreService";
import { Link } from "react-router-dom";

const Genres = (props) => {
    const [genres, setGenres] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState('');

    useEffect(
        () => {
            GenreService.readGenres()
            .then(
                (response) => {
                    setGenres(response.data.results);
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
        <Container>
            {genres.map(
                (genre) => {
                    return (
                        <Card className="w-75 mb-3 mx-auto">
                            <Card.Body>
                                <Card.Title>
                                    <Link to={`/genres/${genre.id}/`} className="text-decoration-none">
                                        {genre.name}
                                    </Link>
                                </Card.Title>
                                <Card.Text>
                                    {genre.description}
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    )
                }
            )}
        </Container>
    );
};

export default Genres;