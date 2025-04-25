export interface BookingSlot {
    id: number
    restaurant_id: number
    start_time: string
    end_time: string
    table_size: number
    is_booked: boolean
}
