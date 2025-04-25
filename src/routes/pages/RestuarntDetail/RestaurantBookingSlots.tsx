import { useState } from "react"
import { useNavigate } from "react-router-dom"
import {
    Box,
    Heading,
    Text,
    Button,
    ButtonGroup,
    SimpleGrid,
} from "@chakra-ui/react"
import { toast } from "react-hot-toast"

import { BookingSlot } from "@/types/Bookingslotdto"
import { bookSlot } from "@/api/reservationapi"
import useUser from "@/lib/useUser"
import { useEffect } from "react"

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
    const [bookingSlotId, setBookingSlotId] = useState<number | null>(null)
    const [availabilityState, setAvailabilityState] =
        useState<BookingSlot[]>(availability)

    const { isLoggedIn } = useUser()
    const navigate = useNavigate()

    const days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    useEffect(() => {
        if (availability && availability.length > 0) {
            setAvailabilityState(availability)
        }
    }, [availability])

    const filteredSlots = selectedDay
        ? availabilityState.filter(
              (slot) =>
                  getDayOfWeek(slot.start_time) === selectedDay &&
                  !slot.is_booked
          )
        : []

    const handleBookSlot = async (slot: BookingSlot) => {
        if (!isLoggedIn) {
            toast("⚠️ Please login as a customer to book a slot.")
            navigate("/login")
            return
        }

        try {
            setBookingSlotId(slot.id)

            await bookSlot({
                restaurant_id: slot.restaurant_id,
                booking_slot_id: slot.id,
                number_of_people: 2,
                reservation_time: slot.start_time,
            })

            toast.success("✅ Slot booked successfully!")

            // 🧠 Mark this slot as booked in state to hide it from UI
            setAvailabilityState((prev) =>
                prev.map((s) =>
                    s.id === slot.id ? { ...s, is_booked: true } : s
                )
            )
        } catch (err) {
            console.error("Booking failed:", err)
            toast.error("❌ Could not complete your reservation.")
        } finally {
            setBookingSlotId(null)
        }
    }

    return (
        <Box my={6}>
            <Heading size="md" mb={4}>
                Available Booking Slots
            </Heading>

            <ButtonGroup size="sm" mb={6} flexWrap="wrap" gap={2}>
                {days.map((day) => (
                    <Button
                        key={day}
                        onClick={() =>
                            setSelectedDay(day === selectedDay ? null : day)
                        }
                        colorPalette={selectedDay === day ? "blue" : "gray"}
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
                <SimpleGrid columns={{ base: 1, sm: 2, md: 3, lg: 4 }} gap={4}>
                    {filteredSlots.map((slot) => (
                        <Box
                            key={slot.id}
                            p={4}
                            borderWidth="1px"
                            borderRadius="xl"
                            bg="gray.50"
                            shadow="sm"
                        >
                            <Text color="gray.600" fontWeight="bold" mb={2}>
                                {formatSlotTime(slot.start_time, slot.end_time)}
                            </Text>
                            <Text fontSize="sm" color="gray.500" mb={4}>
                                Table for {slot.table_size}
                            </Text>

                            <Button
                                size="sm"
                                colorPalette="blue"
                                width="full"
                                loading={bookingSlotId === slot.id}
                                onClick={() => handleBookSlot(slot)}
                            >
                                Book Now
                            </Button>
                        </Box>
                    ))}
                </SimpleGrid>
            ) : (
                <Text textAlign="center" color="gray.500">
                    {selectedDay
                        ? `No available slots for ${selectedDay}.`
                        : "Please select a day to see availability."}
                </Text>
            )}
        </Box>
    )
}
