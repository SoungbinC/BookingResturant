import { instance } from "./axios"

// 🔁 Automatically refresh access token on 401 errors
instance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        // Only attempt refresh if explicitly required
        const requiresAuth = originalRequest.headers?.["x-requires-auth"]

        if (error.response?.status === 401 && requiresAuth) {
            try {
                await instance.post("/auth/refresh")
                return instance(originalRequest)
            } catch (refreshError) {
                console.error("❌ Token refresh failed:", refreshError)
                return Promise.reject(refreshError)
            }
        }

        return Promise.reject(error)
    }
)

export const getMe = () =>
    instance
        .get("/auth/me", {
            headers: { "x-requires-auth": "true" },
        })
        .then((res) => res.data)

export const login = async (email: string, password: string): Promise<void> => {
    const formData = new URLSearchParams()
    formData.append("username", email)
    formData.append("password", password)

    try {
        await instance.post("/auth/login", formData, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        })
    } catch (err) {
        console.error("❌ Login failed:", err)
        throw new Error("Login failed. Please check your credentials.")
    }
}

export const logout = async (): Promise<void> => {
    try {
        await instance.post("/auth/logout", null, {
            headers: { "x-requires-auth": "true" },
        })
    } catch (err) {
        console.error("❌ Logout failed:", err)
        throw new Error("Logout failed. Please try again.")
    }
}

export interface SignupData {
    username: string
    email: string
    password: string
}

export const signup = async (data: SignupData) =>
    instance.post("/auth/register", data).then((res) => res.data)
