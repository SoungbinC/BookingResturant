import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import {
    getMyReservations,
    approveReservation,
    cancelReservationByManager,
} from "@/api/managerapi"
import {
    Box,
    Heading,
    VStack,
    HStack,
    Text,
    Spinner,
    Badge,
    Select,
    Portal,
    createListCollection,
} from "@chakra-ui/react"
import { toaster } from "@/components/ui/toaster"
import ReservationCard from "./ReservationCard"

export default function ManagerReservations() {
    const queryClient = useQueryClient()
    const [filterStatus, setFilterStatus] = useState<string[]>([
        "PENDING",
        "CONFIRMED",
        "CANCELED",
        "ALL",
    ])

    const reservationFilters = createListCollection({
        items: [
            { label: "All Reservations", value: "ALL" },
            { label: "Pending Only", value: "PENDING" },
            { label: "Confirmed Only", value: "CONFIRMED" },
            { label: "Canceled Only", value: "CANCELED" },
        ],
    })

    const { data: reservations, isLoading } = useQuery({
        queryKey: ["managerReservations"],
        queryFn: getMyReservations,
    })

    const approveMutation = useMutation({
        mutationFn: (id: number) => approveReservation(id),
        onSuccess: () => {
            toaster.create({ title: "Reservation approved!", type: "success" })
            queryClient.invalidateQueries(["managerReservations"])
        },
        onError: () => {
            toaster.create({
                title: "Failed to approve reservation.",
                type: "error",
            })
        },
    })

    const cancelMutation = useMutation({
        mutationFn: (id: number) => cancelReservationByManager(id),
        onSuccess: () => {
            toaster.create({ title: "Reservation canceled!", type: "success" })
            queryClient.invalidateQueries(["managerReservations"])
        },
        onError: () => {
            toaster.create({
                title: "Failed to cancel reservation.",
                type: "error",
            })
        },
    })

    if (isLoading) {
        return (
            <Box p={10}>
                <Spinner size="xl" />
            </Box>
        )
    }

    const filteredReservations = reservations?.filter((r) => {
        if (filterStatus.includes("ALL")) return true
        return filterStatus.includes(r.status)
    })

    return (
        <Box p={10}>
            <Heading size="lg" mb={6}>
                Manage Reservations
            </Heading>

            {/* Filter dropdown */}
            <HStack mb={4} justify="flex-end">
                <Select.Root
                    value={filterStatus}
                    onValueChange={(e) => setFilterStatus(e.value)}
                    collection={reservationFilters}
                    size="md"
                >
                    <Select.HiddenSelect />
                    <Select.Control>
                        <Select.Trigger>
                            <Select.ValueText placeholder="Select reservation status" />
                        </Select.Trigger>
                        <Select.IndicatorGroup>
                            <Select.Indicator />
                        </Select.IndicatorGroup>
                    </Select.Control>

                    <Portal>
                        <Select.Positioner>
                            <Select.Content>
                                {reservationFilters.items.map((filter) => (
                                    <Select.Item
                                        key={filter.value}
                                        item={filter}
                                    >
                                        {filter.label}
                                        <Select.ItemIndicator />
                                    </Select.Item>
                                ))}
                            </Select.Content>
                        </Select.Positioner>
                    </Portal>
                </Select.Root>
            </HStack>

            {/* Selected Filters Badges */}
            {filterStatus.length > 0 && (
                <HStack flexWrap="wrap" gap={2} mb={8}>
                    {filterStatus.includes("ALL") ? (
                        <Badge colorPalette="blue" variant="solid">
                            All
                        </Badge>
                    ) : (
                        filterStatus.map((status) => (
                            <Badge
                                key={status}
                                colorPalette={
                                    status === "PENDING"
                                        ? "yellow"
                                        : status === "CONFIRMED"
                                        ? "green"
                                        : status === "CANCELED"
                                        ? "red"
                                        : "gray"
                                }
                                variant="solid"
                            >
                                {status}
                            </Badge>
                        ))
                    )}
                </HStack>
            )}

            {/* Reservation list */}
            <VStack gap={5} align="stretch">
                {filteredReservations && filteredReservations.length > 0 ? (
                    filteredReservations.map((reservation) => (
                        <ReservationCard
                            key={reservation.id}
                            reservation={reservation}
                            onApprove={
                                reservation.status === "PENDING"
                                    ? () =>
                                          approveMutation.mutate(reservation.id)
                                    : undefined
                            }
                            onCancel={
                                reservation.status === "PENDING"
                                    ? () =>
                                          cancelMutation.mutate(reservation.id)
                                    : undefined
                            }
                        />
                    ))
                ) : (
                    <Text>No reservations found for this filter.</Text>
                )}
            </VStack>
        </Box>
    )
}
