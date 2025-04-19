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
