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

    userArtist(id){
        return AxiosInstance.get(`/api/artists/${id}/user_artist/`);
    }

    favouriteArtist(id){
        return AxiosInstance.post(`/api/artists/${id}/favourite/`);
    }
}

export default new ArtistService();