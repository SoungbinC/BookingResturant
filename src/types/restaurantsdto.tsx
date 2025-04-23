// src/types/restaurant.ts

export interface Restaurant {
    id: number
    name: string
    description: string
    address: string
    city?: string
    state?: string
    zipcode?: string
    cuisine?: string
    price_range?: string
    rating?: number
    open_mon?: string
    open_tue?: string
    open_wed?: string
    open_thu?: string
    open_fri?: string
    open_sat?: string
    open_sun?: string
    photo_url?: string
    created_at: string
    updated_at: string
    status: "OPEN" | "CLOSED" | "RENOVATING"
    is_approved: boolean
}
export interface RestaurantSearchParams {
    query: string
    cuisine?: string
    cost_rating?: number
    page?: number
    limit?: number
}
