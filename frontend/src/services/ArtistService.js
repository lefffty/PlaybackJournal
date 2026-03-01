import AxiosInstance from "../components/AxiosInstance";

class ArtistService{
    readArtists(page = 1){
        return AxiosInstance.get(`/api/artists/?page=${page}`);
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