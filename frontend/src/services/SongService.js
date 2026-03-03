import AxiosInstance from "../components/AxiosInstance";

class SongService{
    fetchSongs(){
        return AxiosInstance.get('api/songs/');
    }
}

export default new SongService();