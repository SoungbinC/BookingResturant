import { useQuery } from "@tanstack/react-query"
import { getMyRestaurants } from "@/api/managerapi"
import { Spinner, Box, Heading, Separator as Divider } from "@chakra-ui/react"

import MyRestaurants from "./MyRestaurants"
import ManagerReservations from "./ManagerReservations"

export default function ManagerDashboard() {
    const { data: restaurants, isLoading } = useQuery({
        queryKey: ["myRestaurants"],
        queryFn: getMyRestaurants,
    })

    if (isLoading) {
        return (
            <Box p={10}>
                <Spinner size="xl" />
            </Box>
        )
    }

    return (
        <Box p={10}>
            <Heading size="lg" mb={6}>
                Manager Dashboard
            </Heading>

            {/* Section 1: My Restaurants */}
            <Heading size="md" mb={4}>
                My Restaurants
            </Heading>

            <MyRestaurants restaurants={restaurants || []} />

            {/* Add New Restaurant Button */}
            {/* Divider */}
            <Divider my={10} />

            {/* Section 2: Manage Reservations */}
            <Heading size="md" mb={4}>
                Manage Reservations
            </Heading>

            <ManagerReservations />
        </Box>
    )
}
