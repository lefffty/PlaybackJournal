import AxiosInstance from "../components/AxiosInstance";

class ArtistService{
    readArtists(){
        return AxiosInstance.get("/api/artists/");
    }

    readArtist(id){
        return AxiosInstance.get(`/api/artists/${id}/`)
    }
}

export default new ArtistService();