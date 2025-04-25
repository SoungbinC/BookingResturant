import { BookingSlot } from "./Bookingslotdto"

export interface Reservation {
    id: number
    restaurant_id: number
    user_id: number
    reservation_time: string // ISO datetime string
    number_of_people: number
    status: string // e.g., "pending" | "confirmed" | "cancelled"
    booking_slot: BookingSlot
}
