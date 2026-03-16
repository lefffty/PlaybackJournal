import AxiosInstance from "../components/AxiosInstance";

class SongService{
    fetchSongs(){
        return AxiosInstance.get('/api/songs/');
    }

    fetchSong(id){
        return AxiosInstance.get(`/api/songs/${id}/`);
    }

    rateSong(id, data){
        return AxiosInstance.post(`/api/songs/${id}/rated/`, data);
    }
}

export default new SongService();