// src/pages/RestaurantDetail.tsx
import { useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import {
    getRestaurant,
    getRestaurantBookingAvailability,
} from "@/api/restauratnsApi"

import { Box, Spinner, Center, Alert } from "@chakra-ui/react"
import RestaurantInfo from "./RestuarantInfo"
import RestaurantHours from "./ResturantHours"
import BookingSlots from "./RestaurantBookingSlots"
import RestaurantReviews from "./RestaurantReviews"

export default function RestaurantDetail() {
    const { id } = useParams<{ id: string }>()
    const restaurantId = parseInt(id!)

    const {
        data: restaurant,
        isLoading,
        isError,
    } = useQuery({
        queryKey: ["restaurant", restaurantId],
        queryFn: () => getRestaurant(restaurantId),
        enabled: !!id,
    })

    const {
        data: availability,
        isLoading: isAvailabilityLoading,
        isError: isAvailabilityError,
    } = useQuery({
        queryKey: ["bookingslot", restaurantId],
        queryFn: () => getRestaurantBookingAvailability(restaurantId),
        enabled: !!restaurantId,
    })

    if (isLoading) {
        return (
            <Center py={20}>
                <Spinner size="xl" />
            </Center>
        )
    }

    if (isError || !restaurant) {
        return (
            <Alert.Root status="error" mt={6}>
                <Alert.Title>Failed to load restaurant details.</Alert.Title>
            </Alert.Root>
        )
    }

    return (
        <Box px={6} py={10} maxW={"4xl"} mx="auto">
            <RestaurantInfo restaurant={restaurant} />
            <RestaurantHours restaurant={restaurant} />
            <BookingSlots
                availability={availability}
                isLoading={isAvailabilityLoading}
                isError={isAvailabilityError}
            />
            <RestaurantReviews restaurantId={restaurantId} />
        </Box>
    )
}
