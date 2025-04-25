// src/pages/Manager/MyRestaurants.tsx

import { useState } from "react"
import { Box, SimpleGrid, Text, Button, VStack } from "@chakra-ui/react"

import RestaurantCard from "./RestaurantCard"
import RestaurantAddDialog from "./RestaurantAddDialog"
import type { Restaurant } from "@/types/restaurantsdto"

interface MyRestaurantsProps {
    restaurants: Restaurant[]
}

export default function MyRestaurants({ restaurants }: MyRestaurantsProps) {
    const [selectedRestaurant, setSelectedRestaurant] =
        useState<Restaurant | null>(null)
    const [isDialogOpen, setIsDialogOpen] = useState(false)

    const handleEdit = (restaurant: Restaurant | null) => {
        setSelectedRestaurant(restaurant)
        setIsDialogOpen(true)
    }

    const openAddNew = () => {
        setSelectedRestaurant(null)
        setIsDialogOpen(true)
    }

    return (
        <Box>
            {restaurants.length > 0 ? (
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} gap={8}>
                    {restaurants.map((restaurant) => (
                        <RestaurantCard
                            key={restaurant.id}
                            restaurant={restaurant}
                            onEdit={() => handleEdit(restaurant)}
                        />
                    ))}

                    {/* Add New Card */}
                    <Box
                        p={5}
                        borderWidth={2}
                        borderRadius="md"
                        borderColor="gray.300"
                        cursor="pointer"
                        display="flex"
                        alignItems="center"
                        justifyContent="center"
                        minH="200px"
                        onClick={openAddNew}
                    >
                        Add New Restaurant
                    </Box>
                </SimpleGrid>
            ) : (
                <VStack gap={4} align="center" mt={8}>
                    <Text>No restaurants yet.</Text>
                    <Button colorScheme="blue" onClick={openAddNew}>
                        Add Your First Restaurant
                    </Button>
                </VStack>
            )}

            {/* Dialog */}
            {isDialogOpen && (
                <RestaurantAddDialog
                    isOpen={isDialogOpen}
                    onClose={() => setIsDialogOpen(false)}
                    restaurant={selectedRestaurant}
                />
            )}
        </Box>
    )
}
