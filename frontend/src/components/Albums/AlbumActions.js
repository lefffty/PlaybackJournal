import {Row, Col} from "react-bootstrap"

import WishlistIcon from "../Common/WishlistIcon/WishlistIcon";
import HeartIcon from "../Common/HeartIcon/HeartIcon";
import Headphones from "../Common/Headphones/Headphones";

const AlbumActions = ({isAuthenticated, userAlbumData, onWishlistClick, onFavouriteClick, onListenedClick}) => {
    return (
        <Col md={3}>
            <Row md={3} data-testid="album-actions">
                {isAuthenticated && (
                    <>
                        <WishlistIcon initialValue={userAlbumData.wishlist}
                                      onClick={onWishlistClick}/>
                        <HeartIcon initialValue={userAlbumData.favourite}
                                   onClick={onFavouriteClick}/>
                        <Headphones initialValue={userAlbumData.listened}
                                    onClick={onListenedClick}/>
                    </>
                )}
            </Row>
        </Col>
    )
}

export default AlbumActions;