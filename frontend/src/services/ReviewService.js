import AxiosInstance from "../components/AxiosInstance";

class ReviewsService {
    fetchReview(id){
        return AxiosInstance.get(`http://localhost:8000/api/reviews/${id}/`);
    }

    createComment(data){
        return AxiosInstance.post(`http://localhost:8000/api/comments/`, data);
    }
}

export default new ReviewsService();