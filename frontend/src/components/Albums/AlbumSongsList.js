import {Card, ListGroup} from "react-bootstrap";

import AlbumSongsListEntry from "./AlbumSongsListEntry";

const AlbumSongsList = ({token, album, songsRatings, onSongRatingChange}) => {
    return (
        <Card className="mb-3 border-0">
            <Card.Body>
                <ListGroup variant="flush">
                    <Card.Title data-testid="album-songs-list-title">
                        Список песен:
                    </Card.Title>
                    {album.songs.map(
                        (song, index) => (
                            <ListGroup.Item key={song.id} className="px-0">
                                <AlbumSongsListEntry
                                    index={index}
                                    songRating={songsRatings[song.id]}
                                    song={song}
                                    token={token}
                                    onSongRatingChange={onSongRatingChange}
                                />
                            </ListGroup.Item>
                        )
                    )}
                </ListGroup>
            </Card.Body>
        </Card>
    )
};

export default AlbumSongsList;