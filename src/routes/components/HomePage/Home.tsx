// src/pages/Home.tsx
import {
    Box,
    Grid,
    Heading,
    Stack,
    Text,
    useBreakpointValue,
} from "@chakra-ui/react"
import RestaurantSearchBar from "./RestaurantSearchBar"

const mockRestaurants = [
    { id: 1, name: "Sushi Paradise", cuisine: "Japanese" },
    { id: 2, name: "Pizza Central", cuisine: "Italian" },
    { id: 3, name: "Curry Kingdom", cuisine: "Indian" },
    { id: 4, name: "Burger Barn", cuisine: "American" },
    { id: 5, name: "Taco Time", cuisine: "Mexican" },
]

export default function Home() {
    const columns = useBreakpointValue({ base: 1, sm: 2, md: 3 })

    return (
        <Box px={6} py={10}>
            <Stack align="center" gap={6} mb={10}>
                <Heading size="lg">Find a Restaurant</Heading>
                <RestaurantSearchBar />
            </Stack>

            <Grid templateColumns={`repeat(${columns}, 1fr)`} gap={6}>
                {mockRestaurants.map((r) => (
                    <Box
                        key={r.id}
                        p={5}
                        borderWidth="1px"
                        borderRadius="xl"
                        shadow="md"
                        _hover={{ shadow: "lg", transform: "scale(1.02)" }}
                        transition="all 0.2s"
                    >
                        <Heading size="md" mb={2}>
                            {r.name}
                        </Heading>
                        <Text fontSize="sm" color="gray.500">
                            {r.cuisine}
                        </Text>
                    </Box>
                ))}
            </Grid>
        </Box>
    )
}
