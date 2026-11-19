import AxiosInstance from "../components/AxiosInstance";


class AlbumService{
    readAlbums(page = 1){
        return AxiosInstance.get(`/api/albums/?page=${page}`);
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

    wishlistAlbum(id){
        return AxiosInstance.post(`/api/albums/${id}/wishlist/`)
    }

    userAlbum(id){
        return AxiosInstance.get(`/api/albums/${id}/status/`)
    }

    fetchStatistics(id){
        return AxiosInstance.get(`/api/albums/${id}/statistics/`);
    }

    fetchReviews(id){
        return AxiosInstance.get(`/api/albums/${id}/reviews/`);
    }
}

export default new AlbumService();