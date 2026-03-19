import AxiosInstance from "../components/AxiosInstance";

class ReviewsService {
    fetchReview(id){
        return AxiosInstance.get(`http://localhost:8000/api/reviews/${id}/`);
    }
}

export default new ReviewsService();