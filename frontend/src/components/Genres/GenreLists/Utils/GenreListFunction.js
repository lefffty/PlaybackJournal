import GenreService from "../../../../services/GenreService";

function GenreListFunction(listType){
    let func = null;
    switch (listType) {
        case "genreAlbums":
            func = GenreService.fetchGenreAlbums
            break;
        case "genreArtists":
            func = GenreService.fetchGenreArtists
            break;
        default:
            break;
    }
    return func;
}

export default GenreListFunction;