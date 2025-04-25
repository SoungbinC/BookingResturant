import type { Restaurant } from "@/types/restaurantsdto"
import type { Reservation } from "@/types/reservationsdto"
import { instance } from "./axios"

// 🧩 Get My Restaurant(s)
export async function getMyRestaurants(): Promise<Restaurant[]> {
    const response = await instance.get("/manager/my-restaurants")
    return response.data
}

// 🧩 Create Restaurant
export async function createRestaurant(
    payload: Partial<Restaurant>
): Promise<Restaurant> {
    const response = await instance.post("/manager/restaurants", payload)
    return response.data
}

// 🧩 Update Restaurant
export async function updateRestaurant(
    restaurantId: number,
    payload: Partial<Restaurant>
): Promise<Restaurant> {
    const response = await instance.put(
        `/manager/restaurants/${restaurantId}`,
        payload
    )
    return response.data
}

// 🧩 Get My Reservations (all reservations under my restaurants)
export async function getMyReservations(): Promise<Reservation[]> {
    const response = await instance.get("/manager/reservations")
    return response.data
}

// 🧩 Approve a Reservation
export async function approveReservation(
    reservationId: number
): Promise<Reservation> {
    const response = await instance.post(
        `/manager/reservations/${reservationId}/approve`
    )
    return response.data
}

// 🧩 Cancel a Reservation by Manager
export async function cancelReservationByManager(
    reservationId: number
): Promise<Reservation> {
    const response = await instance.post(
        `/manager/reservations/${reservationId}/cancel`
    )
    return response.data
}
