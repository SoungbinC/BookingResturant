// src/pages/RestaurantsHomeSkeleton.tsx
import {
    Grid,
    Box,
    Skeleton,
    SkeletonText,
    useBreakpointValue,
} from "@chakra-ui/react"

export default function RestaurantsHomeSkeleton() {
    const columns = useBreakpointValue({ base: 1, sm: 2, md: 3 })

    return (
        <Grid templateColumns={`repeat(${columns}, 1fr)`} gap={6}>
            {Array.from({ length: 6 }).map((_, idx) => (
                <Box
                    key={idx}
                    p={5}
                    borderWidth="1px"
                    borderRadius="xl"
                    shadow="md"
                >
                    <Skeleton height="20px" mb={3} />
                    <SkeletonText noOfLines={2} gap="2" />
                </Box>
            ))}
        </Grid>
    )
}
