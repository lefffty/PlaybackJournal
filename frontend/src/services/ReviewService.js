import AxiosInstance from "../components/AxiosInstance";

class ReviewsService {
    fetchReview(id){
        return AxiosInstance.get(`http://localhost:8000/api/reviews/${id}/`);
    }

    fetchComments(id){
        return AxiosInstance.get(`http://localhost:8000/api/reviews/${id}/comments/`);
    }

    createReview(data){
        return AxiosInstance.post(`http://localhost:8000/api/reviews/`, data);
    }

    createComment(data){
        return AxiosInstance.post(`http://localhost:8000/api/comments/`, data);
    }
}

export default new ReviewsService();