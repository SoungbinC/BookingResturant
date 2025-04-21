// src/pages/RestaurantsHome.tsx
import {
    Grid,
    Box,
    Text,
    useBreakpointValue,
    Image,
    Badge,
    Stack,
    AspectRatio,
    GridItem,
    Wrap,
} from "@chakra-ui/react"
import { Restaurant } from "@/types/restaurants"
import { Link } from "react-router-dom"

interface RestaurantsHomeProps {
    restaurants: Restaurant[]
}

export default function RestaurantsHome({ restaurants }: RestaurantsHomeProps) {
    const columns = useBreakpointValue({ base: 1, sm: 2, md: 3 })

    return (
        <Grid
            templateColumns={`repeat(${columns}, 1fr)`}
            gap={6}
            alignItems="stretch"
        >
            {restaurants.map((r: Restaurant) => (
                <Link
                    to={`/restaurants/${r.id}`}
                    key={r.id}
                    style={{ height: "100%" }}
                >
                    <GridItem
                        p={4}
                        borderWidth="1px"
                        borderRadius="xl"
                        shadow="sm"
                        transition="all 0.2s"
                        _hover={{ shadow: "lg", transform: "scale(1.02)" }}
                        bg="white"
                        height="100%"
                        display="flex"
                        flexDirection="column"
                        justifyContent="space-between"
                    >
                        <Stack gap={4} flex="1">
                            <AspectRatio ratio={16 / 9} mb={2}>
                                <Image
                                    src={
                                        !r.photo_url ||
                                        r.photo_url
                                            .toLowerCase()
                                            .includes("no photo")
                                            ? "/fallback.svg"
                                            : r.photo_url
                                    }
                                    alt={r.name}
                                    objectFit="cover"
                                    borderRadius="md"
                                />
                            </AspectRatio>

                            <Wrap flex="1">
                                <Box mb={2}>
                                    <Text
                                        fontSize="xl"
                                        fontWeight="bold"
                                        color="gray.500"
                                    >
                                        {r.name}
                                    </Text>
                                </Box>

                                <Box mb={2}>
                                    <Text
                                        fontSize="xs"
                                        fontWeight="bold"
                                        color="gray.500"
                                    >
                                        Address:
                                    </Text>
                                    <Text fontSize="sm" color="gray.600">
                                        {r.address}, {r.city}, {r.state}{" "}
                                        {r.zipcode}
                                    </Text>
                                </Box>

                                <Box>
                                    <Text
                                        fontSize="xs"
                                        fontWeight="bold"
                                        color="gray.500"
                                        mb={1}
                                    >
                                        Open Status:
                                    </Text>
                                    <Badge
                                        colorScheme={
                                            r.is_approved ? "green" : "yellow"
                                        }
                                    >
                                        {r.status}
                                    </Badge>
                                </Box>
                            </Wrap>
                        </Stack>

                        <Box mt={4}>
                            <Text fontSize="sm" color="gray.500">
                                Rating:{" "}
                                {r.rating
                                    ? `⭐ ${r.rating.toFixed(1)}`
                                    : "Not rated"}
                            </Text>
                        </Box>
                    </GridItem>
                </Link>
            ))}
        </Grid>
    )
}
