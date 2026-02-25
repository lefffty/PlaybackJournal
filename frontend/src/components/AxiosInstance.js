import axios from "axios";

const AxiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
});

AxiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('auth_token');
        if (token){
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    }
)

export default AxiosInstance;