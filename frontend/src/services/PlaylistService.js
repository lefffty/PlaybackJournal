import AxiosInstance from '../components/AxiosInstance';

class PlaylistService{
    fetchPlaylists(page = 1){
        return AxiosInstance.get(`http://localhost:8000/api/playlists/?page=${page}`);
    }
}

export default new PlaylistService();