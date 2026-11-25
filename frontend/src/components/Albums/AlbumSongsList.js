import {Card, Col, ListGroup, Row} from "react-bootstrap";
import {Link} from "react-router-dom";
import ScaleRating from "../Common/ScaleRating/ScaleRating";

const AlbumSongsList = ({token, album, songsRatings, onSongRatingChange}) => {
    return (
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
                                                    initialValue={songsRatings[song.id]}
                                                    onRatingChange={(value) => onSongRatingChange(song.id, value)}
                                                />
                                            ) :
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
    )
};

export default AlbumSongsList;