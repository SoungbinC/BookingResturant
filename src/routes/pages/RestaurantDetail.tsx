// src/pages/RestaurantDetail.tsx
import { useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { getRestaurant } from "@/api/restauratnsApi"
import {
    Box,
    Heading,
    Text,
    Spinner,
    Stack,
    Center,
    Alert,
    Image,
    Badge,
    SimpleGrid,
    Separator,
} from "@chakra-ui/react"

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
        <Box px={6} py={10} maxW="4xl" mx="auto">
            {restaurant.photo_url && (
                <Image
                    src={
                        !restaurant.photo_url ||
                        restaurant.photo_url.toLowerCase().includes("no photo")
                            ? "/fallback.svg"
                            : restaurant.photo_url
                    }
                    alt={restaurant.name}
                    borderRadius="xl"
                    mb={6}
                />
            )}

            <Heading mb={2}>{restaurant.name}</Heading>
            <Badge
                colorScheme={restaurant.is_approved ? "green" : "yellow"}
                mb={4}
            >
                {restaurant.status}
            </Badge>

            <Stack gap={3}>
                <Text fontWeight="medium">
                    Cuisine:{" "}
                    <Text as="span" fontWeight="normal">
                        {restaurant.cuisine}
                    </Text>
                </Text>
                <Text fontWeight="medium">
                    Address:{" "}
                    <Text as="span" fontWeight="normal">
                        {restaurant.address}
                    </Text>
                </Text>
                <Text fontWeight="medium">
                    Location:{" "}
                    <Text as="span" fontWeight="normal">
                        {restaurant.city}, {restaurant.state}{" "}
                        {restaurant.zipcode}
                    </Text>
                </Text>
                <Text fontWeight="medium">
                    Price Range:{" "}
                    <Text as="span" fontWeight="normal">
                        {restaurant.price_range ?? "N/A"}
                    </Text>
                </Text>
                <Text fontWeight="medium">
                    Rating:{" "}
                    <Text as="span" fontWeight="normal">
                        {restaurant.rating ?? "Not rated yet"}
                    </Text>
                </Text>
                <Text fontWeight="medium">
                    Description:{" "}
                    <Text as="span" fontWeight="normal">
                        {restaurant.description ?? "No description available."}
                    </Text>
                </Text>
            </Stack>

            <Separator my={6} />

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
