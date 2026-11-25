import {Card, Col, Row} from "react-bootstrap";
import {Link} from "react-router-dom";
import React from "react";
import moment from "moment/moment";
import ScaleRating from "../Common/ScaleRating/ScaleRating";
import AlbumActions from "./AlbumActions";


const AlbumHeader = ({isAuthenticated, album, userAlbumData, onWishlistClick, onFavouriteClick, onListenedClick, onRatingChange}) => {
    return (
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
                                            <React.Fragment key={artist.id}>
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
                                                        <React.Fragment key={genre.id}>
                                                            <Link to={`/genres/${genre.id}/`}
                                                                  className="text-decoration-none">
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
                            <AlbumActions
                                isAuthenticated={isAuthenticated}
                                onListenedClick={onListenedClick}
                                onFavouriteClick={onFavouriteClick}
                                onWishlistClick={onWishlistClick}
                                userAlbumData={userAlbumData}
                            />
                        </Row>
                        {isAuthenticated && (
                            <>
                                <ScaleRating initialValue={userAlbumData.rating} totalStars={10}
                                             onRatingChange={onRatingChange}/>
                            </>
                        )}
                    </Card.Body>
                </Col>
            </Row>
        </Card>
    )
}

export default AlbumHeader;