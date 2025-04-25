// src/api/reservationapi.ts
import { instance } from "./axios"

export interface BookSlotPayload {
    restaurant_id: number
    booking_slot_id: number
    number_of_people: number
    reservation_time: string
}

export const bookSlot = async (payload: BookSlotPayload) => {
    const res = await instance.post("/customers/reservations", payload, {
        headers: { "x-requires-auth": "true" },
        withCredentials: true,
    })
    return res.data
}
