import AxiosInstance from "../components/AxiosInstance";


class GenreService {
    readGenres(){
        return AxiosInstance.get("api/genres/");
    }
}

export default new GenreService();