import AxiosInstance from "../components/AxiosInstance";


class AlbumService{
    readAlbums(){
        return AxiosInstance.get("/api/albums/");
    }

    readAlbum(id){
        return AxiosInstance.get(`/api/albums/${id}/`);
    }

    rateAlbum(id, data){
        return AxiosInstance.post(`/api/albums/${id}/rated/`, data);
    }
}

export default new AlbumService();