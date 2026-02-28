import AxiosInstance from "../components/AxiosInstance";

class ArtistService{
    readArtists(){
        return AxiosInstance.get("/api/artists/");
    }

    readArtist(id){
        return AxiosInstance.get(`/api/artists/${id}/`);
    }

    readDiscography(id){
        return AxiosInstance.get(`/api/artists/${id}/discography/`);
    }

    readSimilar(id) {
        return AxiosInstance.get(`/api/artists/${id}/similar/`);
    }
}

export default new ArtistService();