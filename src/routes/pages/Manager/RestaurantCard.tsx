// src/pages/Manager/RestaurantCard.tsx

import {
    Box,
    Heading,
    Text,
    Badge,
    Button,
    VStack,
    HStack,
} from "@chakra-ui/react"
import type { Restaurant } from "@/types/restaurantsdto"

interface RestaurantCardProps {
    restaurant: Restaurant
    onEdit: () => void
}

export default function RestaurantCard({
    restaurant,
    onEdit,
}: RestaurantCardProps) {
    return (
        <Box p={5} borderWidth={1} borderRadius="md" shadow="sm">
            <VStack align="start" gap={3}>
                <Heading size="md">{restaurant.name}</Heading>

                <Text fontSize="sm" color="gray.500">
                    {restaurant.address}
                </Text>

                <HStack>
                    <Badge colorPalette="green">{restaurant.status}</Badge>
                    <Badge colorPalette="blue">{restaurant.city}</Badge>
                </HStack>

                <Button onClick={onEdit} size="sm" colorPalette="blue" mt={2}>
                    Edit
                </Button>
            </VStack>
        </Box>
    )
}
