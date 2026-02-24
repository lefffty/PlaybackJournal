import axios from 'axios';


class UserService {
    profile(token){
        axios.defaults.headers['Authorization'] = 'Token ' + token;
        return axios.get("http://localhost:8000/api/users/me/");
    }

    login(data){
        return axios.post("http://localhost:8000/api/auth/token/login/", data);
    }

    logout(token){
        axios.defaults.headers['Authorization'] = 'Token ' + token;
        return axios.post("http://localhost:8000/api/auth/token/logout/");
    }

    signup(data){
        return axios.post("http://localhost:8000/api/users/", data);
    }
}

export default new UserService();