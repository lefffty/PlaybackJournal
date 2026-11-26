import {Col, Row} from "react-bootstrap";
import {Link} from "react-router-dom";
import ScaleRating from "../Common/ScaleRating/ScaleRating";


const AlbumSongsListEntry = ({index, token, song, onSongRatingChange, songRating}) => {
    return (
        <Row>
            <Col xs={1} className="text-muted fs-5" data-testid="song-index">
                {index + 1}
            </Col>
            <Col xs={5} className="fs-5">
                <Link to={`/songs/${song.id}/`} className="text-decoration-none" data-testid="song-name">
                    {song.name}
                </Link>
            </Col>
            <Col xs={5}>
                {token ? (
                        <ScaleRating
                            initialValue={songRating}
                            onRatingChange={(value) => onSongRatingChange(song.id, value)}
                        />
                    ) :
                    (
                        <>
                        </>
                    )}
            </Col>
            <Col xs={1} className="text-end fs-5" data-testid="song-duration">
                {song.duration}
            </Col>
        </Row>
    )
}

export default AlbumSongsListEntry;