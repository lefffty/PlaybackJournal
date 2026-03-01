import AxiosInstance from "../components/AxiosInstance";


class GenreService {
    readGenres(){
        return AxiosInstance.get("api/genres/");
    }

    readGenre(id){
        return AxiosInstance.get(`api/genres/${id}/`);
    }

    fetchGenreAlbums(id){
        return AxiosInstance.get(`api/genres/${id}/albums/`);
    }

    fetchGenreArtists(id){
        return AxiosInstance.get(`api/genres/${id}/artists/`);
    }
}

export default new GenreService();