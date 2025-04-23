// src/components/RestaurantHours.tsx
import { Heading, Text, SimpleGrid, Box, Separator } from "@chakra-ui/react"
import { Restaurant } from "@/types/restaurantsdto"
export default function RestaurantHours({
    restaurant,
}: {
    restaurant: Restaurant
}) {
    return (
        <Box my={6}>
            <Separator mb={6} />
            <Heading size="md" mb={4}>
                Weekly Hours
            </Heading>
            <SimpleGrid columns={[1, 2]} gap={3}>
                <Text>Monday: {restaurant.open_mon ?? "Closed"}</Text>
                <Text>Tuesday: {restaurant.open_tue ?? "Closed"}</Text>
                <Text>Wednesday: {restaurant.open_wed ?? "Closed"}</Text>
                <Text>Thursday: {restaurant.open_thu ?? "Closed"}</Text>
                <Text>Friday: {restaurant.open_fri ?? "Closed"}</Text>
                <Text>Saturday: {restaurant.open_sat ?? "Closed"}</Text>
                <Text>Sunday: {restaurant.open_sun ?? "Closed"}</Text>
            </SimpleGrid>
        </Box>
    )
}
