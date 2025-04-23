import { BookingSlot } from "../../../types/Bookingslotdto"
import {
    Heading,
    Text,
    SimpleGrid,
    Box,
    Separator,
    Button,
    ButtonGroup,
} from "@chakra-ui/react"
import { useState } from "react"

const formatSlotTime = (start: string, end: string) => {
    const startDate = new Date(start)
    const endDate = new Date(end)

    const datePart = startDate.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
    })

    const startTime = startDate.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    })

    const endTime = endDate.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    })

    return `${datePart} — ${startTime} - ${endTime}`
}

const getDayOfWeek = (isoDate: string) =>
    new Date(isoDate).toLocaleDateString("en-US", { weekday: "long" })

export default function BookingSlots({
    availability,
    isLoading,
    isError,
}: {
    availability: BookingSlot[]
    isLoading: boolean
    isError: boolean
}) {
    const [selectedDay, setSelectedDay] = useState<string | null>(null)

    const days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    const filteredSlots = selectedDay
        ? availability.filter(
              (slot) =>
                  getDayOfWeek(slot.start_time) === selectedDay &&
                  slot.is_booked === false
          )
        : []

    return (
        <Box my={6}>
            <Separator my={6} />
            <Heading size="md" mb={4}>
                Available Booking Slots
            </Heading>

            <ButtonGroup size="sm" mb={4}>
                {days.map((day) => (
                    <Button
                        key={day}
                        onClick={() =>
                            setSelectedDay(day === selectedDay ? null : day)
                        }
                        colorScheme={selectedDay === day ? "blue" : "gray"}
                        variant={selectedDay === day ? "solid" : "outline"}
                    >
                        {day}
                    </Button>
                ))}
            </ButtonGroup>

            {isLoading ? (
                <Text>Loading availability...</Text>
            ) : isError ? (
                <Text color="red.500">Failed to load booking slots.</Text>
            ) : filteredSlots.length > 0 ? (
                <SimpleGrid columns={[1, 2, 4]} gap={3}>
                    {filteredSlots.map((slot: BookingSlot) => (
                        <Box
                            key={slot.id}
                            p={3}
                            borderWidth="1px"
                            borderRadius="md"
                            shadow="sm"
                            bg="gray.50"
                        >
                            <Text fontWeight="medium" color="gray.700">
                                {formatSlotTime(slot.start_time, slot.end_time)}
                            </Text>
                            <Text fontSize="sm" color="gray.500">
                                Table for {slot.table_size}
                            </Text>
                        </Box>
                    ))}
                </SimpleGrid>
            ) : (
                <Text>
                    {selectedDay
                        ? `No available slots for ${selectedDay}.`
                        : "Please select a day to see availability."}
                </Text>
            )}
        </Box>
    )
}
