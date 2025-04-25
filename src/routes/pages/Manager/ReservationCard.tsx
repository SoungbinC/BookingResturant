// src/components/Manager/ReservationCard.tsx

import { Box, HStack, VStack, Text, Badge, Button } from "@chakra-ui/react"
import type { Reservation } from "@/types/reservationdto"

interface ReservationCardProps {
    reservation: Reservation
    onApprove?: () => void
    onCancel?: () => void
}

export default function ReservationCard({
    reservation,
    onApprove,
    onCancel,
}: ReservationCardProps) {
    return (
        <Box p={5} borderWidth={1} borderRadius="md">
            <HStack justifyContent="space-between" mb={3}>
                <Text fontWeight="bold">Reservation #{reservation.id}</Text>
                <Badge
                    colorScheme={
                        reservation.status === "PENDING"
                            ? "yellow"
                            : reservation.status === "CONFIRMED"
                            ? "green"
                            : reservation.status === "CANCELED"
                            ? "red"
                            : "gray"
                    }
                >
                    {reservation.status}
                </Badge>
            </HStack>

            <VStack align="start" gap={1}>
                <Text>
                    <strong>Slot:</strong>{" "}
                    {formatTimeRange(
                        reservation.booking_slot.start_time,
                        reservation.booking_slot.end_time
                    )}
                </Text>
                <Text>
                    <strong>People:</strong> {reservation.number_of_people}
                </Text>
                <Text>
                    <strong>Reserved At:</strong>{" "}
                    {new Date(reservation.reservation_time).toLocaleString()}
                </Text>
            </VStack>

            {onApprove && onCancel && (
                <HStack gap={4} mt={4}>
                    <Button colorScheme="green" onClick={onApprove}>
                        Approve
                    </Button>
                    <Button colorScheme="red" onClick={onCancel}>
                        Cancel
                    </Button>
                </HStack>
            )}
        </Box>
    )
}

// 🧩 Small helper function for formatting time
function formatTimeRange(start: string, end: string) {
    const startTime = new Date(start).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
    })
    const endTime = new Date(end).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
    })
    return `${startTime} - ${endTime}`
}
