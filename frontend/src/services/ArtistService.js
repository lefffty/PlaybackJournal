import AxiosInstance from "../components/AxiosInstance";

class ArtistService{
    readArtists(){
        return AxiosInstance.get("/api/artists/");
    }
}

export default new ArtistService();