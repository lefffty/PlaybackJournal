import AxiosInstance from '../components/AxiosInstance';

class PlaylistService{
    fetchPlaylists(page = 1){
        return AxiosInstance.get(`api/playlists/?page=${page}`);
    }

    fetchPlaylist(id){
        return AxiosInstance.get(`api/playlists/${id}/`);
    }

    createPlaylist(data){
        return AxiosInstance.post('api/playlists/', data);
    }

    deletePlaylist(id){
        return AxiosInstance.delete(`api/playlists/${id}/`);
    }

    userPlaylist(id){
        return AxiosInstance.get(`api/playlists/${id}/user_playlist/`);
    }

    favouritePlaylist(id){
        return AxiosInstance.post(`api/playlists/${id}/favourite/`);
    }

    ratePlaylist(id, data){
        return AxiosInstance.post(`api/playlists/${id}/rated/`, data);
    }

    updatePlaylist(id, data){
        return AxiosInstance.patch(`api/playlists/${id}/`, data);
    }
}

export default new PlaylistService();