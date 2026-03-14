import AxiosInstance from "../components/AxiosInstance";


class GenreService {
    readGenres(page = 1){
        return AxiosInstance.get(`api/genres/?page=${page}`);
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

    userGenre(id){
        return AxiosInstance.get(`api/genres/${id}/user_genre/`);
    }

    favouriteGenre(id){
        return AxiosInstance.post(`api/genres/${id}/favourite/`);
    }
}

export default new GenreService();