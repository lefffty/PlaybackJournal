import AxiosInstance from "../components/AxiosInstance";

class ReviewsService {
    fetchReview(id){
        return AxiosInstance.get(`api/reviews/${id}/`);
    }

    fetchComments(id){
        return AxiosInstance.get(`api/reviews/${id}/comments/`);
    }

    reactionReview(id, data){
        return AxiosInstance.post(`api/reviews/${id}/review_reaction/`, data);
    }

    createReview(data){
        return AxiosInstance.post(`api/reviews/`, data);
    }

    createComment(data){
        return AxiosInstance.post(`api/comments/`, data);
    }
}

export default new ReviewsService();