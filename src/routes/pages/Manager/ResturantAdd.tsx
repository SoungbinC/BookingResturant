// src/pages/Manager/RestaurantAdd.tsx

import { useMutation, useQueryClient } from "@tanstack/react-query"
import { createRestaurant } from "@/api/managerapi"
import { toaster } from "@/components/ui/toaster"
import RestaurantForm from "./RestuarantForm"
import type { Restaurant } from "@/types/restaurantsdto"

interface Props {
    onSuccess: () => void
}

export default function RestaurantAdd({ onSuccess }: Props) {
    const queryClient = useQueryClient()

    const createMutation = useMutation({
        mutationFn: createRestaurant,
        onSuccess: () => {
            toaster.create({
                title: "Restaurant created!",
                type: "success",
                duration: 3000,
            })
            queryClient.invalidateQueries(["myRestaurants"])
            onSuccess()
        },
        onError: () => {
            toaster.create({
                title: "Failed to create restaurant.",
                type: "error",
                duration: 3000,
            })
        },
    })

    const handleCreateSubmit = async (values: Partial<Restaurant>) => {
        await createMutation.mutateAsync(values)
    }

    return <RestaurantForm onSubmit={handleCreateSubmit} />
}
