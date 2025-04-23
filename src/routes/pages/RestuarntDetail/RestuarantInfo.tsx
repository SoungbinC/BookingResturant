// src/components/RestaurantInfo.tsx
import {
    Box,
    Heading,
    Text,
    Stack,
    Badge,
    Image,
    Button,
} from "@chakra-ui/react"
import { useState } from "react"
import { Restaurant } from "@/types/restaurantsdto"
export default function RestaurantInfo({
    restaurant,
}: {
    restaurant: Restaurant
}) {
    const [showFullDescription, setShowFullDescription] = useState(false)
    const fullDescription =
        restaurant.description ?? "No description available."
    const shortDescription =
        fullDescription.slice(0, 200) +
        (fullDescription.length > 200 ? "..." : "")

    return (
        <Box>
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
                        {showFullDescription
                            ? fullDescription
                            : shortDescription}
                    </Text>
                </Text>
                {fullDescription.length > 200 && (
                    <Button
                        variant="subtle"
                        size="sm"
                        onClick={() => setShowFullDescription((prev) => !prev)}
                    >
                        {showFullDescription ? "Show less" : "Read more"}
                    </Button>
                )}
            </Stack>
        </Box>
    )
}
