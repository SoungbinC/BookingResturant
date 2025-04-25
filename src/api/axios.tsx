import axios from "axios"

// 🔧 Axios instance with cookies enabled
export const instance = axios.create({
    baseURL: "http://127.0.0.1:8000",
    withCredentials: true,
})
