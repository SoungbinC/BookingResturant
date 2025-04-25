import { instance } from "./axios"
import type { Reservation } from "@/types/reservationdto"

export interface CustomerProfile {
    id: number
    username: string
    email: string
    role: string
}

// 🔍 GET /customers/profile
export const getCustomerProfile = async (): Promise<CustomerProfile> => {
    const res = await instance.get("/customers/profile", {
        headers: { "x-requires-auth": "true" },
        withCredentials: true,
    })
    return res.data
}

// 📅 GET /customers/reservations/me
export const getCustomerReservations = async (): Promise<Reservation[]> => {
    const res = await instance.get("/customers/reservations/me", {
        headers: { "x-requires-auth": "true" },
        withCredentials: true,
    })
    return res.data
}
