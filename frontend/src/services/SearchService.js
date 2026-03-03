import AxiosInstance from "../components/AxiosInstance";

class SearchService {
    search(data){
        return AxiosInstance.get(`/api/search/`, {params: data });
    }
}

export default new SearchService();