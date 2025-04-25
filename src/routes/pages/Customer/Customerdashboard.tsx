import {
    Box,
    Card,
    CardHeader,
    CardBody,
    Heading,
    Text,
    VStack,
    Spinner,
    Separator as Divider,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { getCustomerProfile, getCustomerReservations } from "@/api/customerapi"

import { format } from "date-fns"

export default function CustomerDashboard() {
    const { data: profile, isLoading: loadingProfile } = useQuery({
        queryKey: ["customerProfile"],
        queryFn: getCustomerProfile,
    })

    const { data: reservations, isLoading: loadingReservations } = useQuery({
        queryKey: ["customerReservations"],
        queryFn: getCustomerReservations,
    })

    if (loadingProfile || loadingReservations) {
        return (
            <Box px={10} py={6}>
                <Spinner size="xl" />
            </Box>
        )
    }

    return (
        <Box px={10} py={6}>
            <Heading size="xl" mb={6}>
                Welcome,{" "}
                <Text as="span" color="red.500">
                    {profile?.username}
                </Text>
            </Heading>

            <Heading size="lg" mt={10} mb={4}>
                Your Reservations
            </Heading>

            <VStack gap={4} align="stretch">
                {reservations && reservations.length > 0 ? (
                    reservations.map((res) => (
                        <Card.Root key={res.id} shadow="sm" borderRadius="2xl">
                            <CardHeader>
                                <Heading size="md">
                                    📍 Restaurant #{res.restaurant_id}
                                </Heading>
                            </CardHeader>
                            <CardBody>
                                <Text>
                                    Date:{" "}
                                    {new Date(
                                        res.reservation_time
                                    ).toLocaleString()}
                                </Text>
                                <Text>People: {res.number_of_people}</Text>
                                <Text>
                                    Status:{" "}
                                    <Text as="span" color="blue.500">
                                        {res.status}
                                    </Text>
                                </Text>
                                <Divider my={3} />
                                <Text fontSize="sm" color="gray.500">
                                    Slot:{" "}
                                    {format(
                                        new Date(res.booking_slot.start_time),
                                        "MMM d, h:mm a"
                                    )}{" "}
                                    —{" "}
                                    {format(
                                        new Date(res.booking_slot.end_time),
                                        "h:mm a"
                                    )}
                                </Text>
                            </CardBody>
                        </Card.Root>
                    ))
                ) : (
                    <Text>No reservations yet.</Text>
                )}
            </VStack>
        </Box>
    )
}
