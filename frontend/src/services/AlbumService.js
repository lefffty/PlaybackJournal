import axios from "axios";


class AlbumService{
    readAlbums(){
        return axios.get("http://localhost:8000/api/albums/");
    }
}

export default new AlbumService();