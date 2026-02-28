import AxiosInstance from "../components/AxiosInstance";


class GenreService {
    readGenres(){
        return AxiosInstance.get("api/genres/");
    }

    readGenre(id){
        return AxiosInstance.get(`api/genres/${id}/`);
    }
}

export default new GenreService();