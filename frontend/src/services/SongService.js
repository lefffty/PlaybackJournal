import AxiosInstance from "../components/AxiosInstance";

class SongService{
    fetchSongs(){
        return AxiosInstance.get('/api/songs/');
    }

    fetchSong(id){
        return AxiosInstance.get(`/api/songs/${id}/`);
    }
}

export default new SongService();