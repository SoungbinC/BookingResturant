// src/pages/RestaurantsHome.tsx
import { Grid, Box, Heading, Text, useBreakpointValue } from "@chakra-ui/react"
import { Restaurant } from "@/types/restaurants"

interface RestaurantsHomeProps {
    restaurants: Restaurant[]
}

export default function RestaurantsHome({ restaurants }: RestaurantsHomeProps) {
    const columns = useBreakpointValue({ base: 1, sm: 2, md: 3 })

    return (
        <Grid templateColumns={`repeat(${columns}, 1fr)`} gap={6}>
            {restaurants.map((r: Restaurant) => (
                <Box
                    key={r.id}
                    p={5}
                    borderWidth="1px"
                    borderRadius="xl"
                    shadow="md"
                    transition="all 0.2s"
                    _hover={{ shadow: "lg", transform: "scale(1.02)" }}
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
    )
}
