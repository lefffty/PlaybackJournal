import UserService from "../../../../services/UserService";

function UserListFunction(listType){
    let func = null;
    switch (listType) {
        case "favouriteAlbums":
            func = UserService.fetchFavouriteAlbums
            break;
        case "listenedAlbums":
            func = UserService.fetchListenedAlbums            
            break;
        case "ratedAlbums":
            func = UserService.fetchRatedAlbums
            break;
        case "favouritePlaylists":
            func = UserService.fetchFavouritePlaylists
            break;
        case "ratedPlaylists":
            func = UserService.fetchRatedPlaylists
            break;
        case "favouriteArtists":
            func = UserService.fetchFavouriteArtists
            break;
        case "wishlistAlbums":
            func = UserService.fetchWishlistAlbums
            break;
        case "reviews":
            func = UserService.fetchReviews
            break;
        default:
            break;
    }

    return func;
}

export default UserListFunction;