// src/types/restaurant.ts

export interface Restaurant {
    id: number
    name: string
    address: string
    city: string
    state: string
    zipcode: string
    cuisine: string
    cost_rating: number
    created_at: string
    updated_at: string
    available_time_slots: string[]
    status: "OPEN" | "CLOSED" | "RENOVATING"
    is_approved: boolean
    description?: string
    photo_url?: string
}
export interface RestaurantSearchParams {
    query: string
    cuisine?: string
    cost_rating?: number
    page?: number
    limit?: number
}
