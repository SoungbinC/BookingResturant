// src/api/restaurantApi.ts
import axios from "axios"

const instance = axios.create({
    baseURL: "http://127.0.0.1:8000",
})

// Fetch all restaurants
export const getRestaurants = () =>
    instance.get("/restaurants/").then((res) => res.data)

// Fetch one restaurant by ID
export const getRestaurant = (id: number) =>
    instance.get(`/restaurants/${id}`).then((res) => res.data)

export const getRestaurantBookingAvailability = (id: number) =>
    instance.get(`/restaurants/${id}/available-slots`).then((res) => res.data)

export const getRestaurantReviews = (id: number) =>
    instance.get(`/restaurants/${id}/reviews`).then((res) => res.data)

export type ValidSearchParams = {
    name?: string
    cuisine?: string
    city?: string
    zipcode?: string
    date?: string
    time?: string
    cost_rating?: string[]
    page?: number
    limit?: number
}

export const getSearchRestaurants = (params: ValidSearchParams) => {
    const searchParams = new URLSearchParams()

    for (const [key, value] of Object.entries(params)) {
        if (value !== undefined && value !== "") {
            searchParams.append(key, value.toString())
        }
    }

    return instance
        .get(`/restaurants/search?${searchParams.toString()}`)
        .then((res) => res.data)
}
