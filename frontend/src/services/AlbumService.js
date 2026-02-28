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

    listenAlbum(id){
        return AxiosInstance.post(`/api/albums/${id}/listened/`);
    }

    favouriteAlbum(id){
        return AxiosInstance.post(`/api/albums/${id}/favourite/`);
    }

    userAlbum(id){
        return AxiosInstance.get(`/api/albums/${id}/user_album/`)
    }
}

export default new AlbumService();