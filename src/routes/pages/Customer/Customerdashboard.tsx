import {
    Box,
    Card,
    CardHeader,
    CardBody,
    Heading,
    Text,
    VStack,
    Spinner,
    Button,
    Separator as Divider,
    HStack,
} from "@chakra-ui/react"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { getCustomerProfile, getCustomerReservations } from "@/api/customerapi"
import { cancelReservation } from "@/api/reservationapi"
import { format } from "date-fns"
import { useState } from "react"
import { toast } from "react-hot-toast"

export default function CustomerDashboard() {
    const { data: profile, isLoading: loadingProfile } = useQuery({
        queryKey: ["customerProfile"],
        queryFn: getCustomerProfile,
    })

    const { data: reservations, isLoading: loadingReservations } = useQuery({
        queryKey: ["customerReservations"],
        queryFn: getCustomerReservations,
    })

    const queryClient = useQueryClient()
    const [visibleCount, setVisibleCount] = useState(3)

    const handleSeeMore = () => {
        setVisibleCount((prev) => prev + 3)
    }

    const handleCancel = async (
        restaurant_id: number,
        booking_slot_id: number
    ) => {
        try {
            await cancelReservation({ restaurant_id, booking_slot_id })
            toast.success("✅ Reservation canceled")
            queryClient.invalidateQueries(["customerReservations"]) // refetch updated reservations
        } catch (err) {
            console.error(err)
            toast.error("❌ Failed to cancel reservation")
        }
    }

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
                    <>
                        {reservations.slice(0, visibleCount).map((res) => (
                            <Card.Root
                                key={res.id}
                                shadow="sm"
                                borderRadius="2xl"
                            >
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
                                            new Date(
                                                res.booking_slot.start_time
                                            ),
                                            "MMM d, h:mm a"
                                        )}{" "}
                                        —{" "}
                                        {format(
                                            new Date(res.booking_slot.end_time),
                                            "h:mm a"
                                        )}
                                    </Text>

                                    <HStack mt={4}>
                                        <Button
                                            size="sm"
                                            colorPalette="red"
                                            onClick={() =>
                                                handleCancel(
                                                    res.restaurant_id,
                                                    res.booking_slot.id
                                                )
                                            }
                                        >
                                            Cancel Reservation
                                        </Button>
                                    </HStack>
                                </CardBody>
                            </Card.Root>
                        ))}

                        {visibleCount < reservations.length && (
                            <Button
                                mt={4}
                                width="fit-content"
                                mx="auto"
                                variant="outline"
                                colorPalette="blue"
                                onClick={handleSeeMore}
                            >
                                See More Reservations
                            </Button>
                        )}
                    </>
                ) : (
                    <Text>No reservations yet.</Text>
                )}
            </VStack>
        </Box>
    )
}
