import AxiosInstance from '../components/AxiosInstance';

class PlaylistService{
    fetchPlaylists(page = 1){
        return AxiosInstance.get(`api/playlists/?page=${page}`);
    }

    fetchPlaylist(id){
        return AxiosInstance.get(`api/playlists/${id}/`);
    }
}

export default new PlaylistService();