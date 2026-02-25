import axios from "axios";


class AlbumService{
    readAlbums(){
        return axios.get("http://localhost:8000/api/albums/");
    }

    readAlbum(id){
        return axios.get(`htt://localhost:8000/api/albums/${id}/`);
    }
}

export default new AlbumService();