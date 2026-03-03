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
}

export default new PlaylistService();