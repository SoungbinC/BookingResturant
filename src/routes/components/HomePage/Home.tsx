// src/pages/Home.tsx
import { Box, Heading, Stack, Text } from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { getRestaurants } from "@/api/restauratnsApi"
import RestaurantSearchBar from "./RestaurantSearchBar"
import RestaurantsHome from "./RestaurantsHome"
import RestaurantsHomeSkeleton from "./RestaurantsHomeSkeleton"
export default function Home() {
    const {
        data: restaurants,
        isLoading,
        isError,
    } = useQuery({
        queryKey: ["restaurants"],
        queryFn: getRestaurants,
        staleTime: 1000 * 60 * 5,
    })

    return (
        <Box px={6} py={10}>
            <Stack align="center" gap={6} mb={10}>
                <Heading size="lg">Restaurants</Heading>
                <RestaurantSearchBar />
            </Stack>

            {isError && (
                <Text color="red.500" textAlign="center">
                    Failed to load restaurants. Please try again later.
                </Text>
            )}

            {isLoading ? (
                <RestaurantsHomeSkeleton />
            ) : (
                <RestaurantsHome restaurants={restaurants} />
            )}
        </Box>
    )
}
