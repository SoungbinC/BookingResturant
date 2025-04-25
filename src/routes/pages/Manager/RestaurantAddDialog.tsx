// src/pages/Manager/RestaurantAdd.tsx

import { useMutation, useQueryClient } from "@tanstack/react-query"
import { createRestaurant, updateRestaurant } from "@/api/managerapi"
import { toaster } from "@/components/ui/toaster"
import RestaurantForm from "./RestuarantForm"
import type { Restaurant } from "@/types/restaurantsdto"

interface Props {
    onSuccess: () => void
    restaurant?: Restaurant | null
}

export default function RestaurantAdd({ onSuccess, restaurant }: Props) {
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
            })
        },
    })

    const updateMutation = useMutation({
        mutationFn: (params: { id: number; payload: Partial<Restaurant> }) =>
            updateRestaurant(params.id, params.payload),
        onSuccess: () => {
            toaster.create({
                title: "Restaurant updated!",
                type: "success",
                duration: 3000,
            })
            queryClient.invalidateQueries(["myRestaurants"])
            onSuccess()
        },
        onError: () => {
            toaster.create({
                title: "Failed to update restaurant.",
                type: "error",
            })
        },
    })

    const handleSubmit = async (values: Partial<Restaurant>) => {
        if (restaurant) {
            await updateMutation.mutateAsync({
                id: restaurant.id,
                payload: values,
            })
        } else {
            await createMutation.mutateAsync(values)
        }
    }

    return (
        <RestaurantForm
            initialValues={restaurant || undefined}
            onSubmit={handleSubmit}
            onCancel={onSuccess} // ✅ Allow Cancel button to close
        />
    )
}
