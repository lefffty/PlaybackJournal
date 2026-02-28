import AxiosInstance from "../components/AxiosInstance";


class UserService {
    profile(){
        return AxiosInstance.get("/api/users/me/");
    }

    login(data){
        return AxiosInstance.post("/api/auth/token/login/", data);
    }

    logout(){
        return AxiosInstance.post("/api/auth/token/logout/");
    }

    signup(data){
        return AxiosInstance.post("/api/users/", data);
    }

    setPassword(data){
        return AxiosInstance.post("/api/users/set_password/", data);
    }

    setAvatar(data){
        return AxiosInstance.put("/api/users/me/avatar/", data);
    }
}

export default new UserService();