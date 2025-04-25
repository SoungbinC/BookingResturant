import { useForm } from "react-hook-form"
import {
    Box,
    Button,
    Input,
    Textarea,
    VStack,
    Heading,
    SimpleGrid,
    HStack,
} from "@chakra-ui/react"
import type { Restaurant } from "@/types/restaurantsdto"

interface Props {
    initialValues?: Partial<Restaurant>
    onSubmit: (values: Partial<Restaurant>) => void
    onCancel?: () => void // ✅ New optional cancel handler
}

export default function RestaurantForm({
    initialValues,
    onSubmit,
    onCancel,
}: Props) {
    const {
        register,
        handleSubmit,
        formState: { isSubmitting },
    } = useForm<Partial<Restaurant>>({
        defaultValues: initialValues,
    })

    return (
        <Box as="form" onSubmit={handleSubmit(onSubmit)} px={6} py={4}>
            <VStack gap={4} align="stretch">
                <Heading size="md">Restaurant Details</Heading>

                <Input
                    placeholder="Restaurant Name"
                    {...register("name", { required: true })}
                />
                <Textarea
                    placeholder="Description"
                    {...register("description")}
                />
                <Input placeholder="Address" {...register("address")} />
                <Input placeholder="City" {...register("city")} />
                <Input placeholder="State" {...register("state")} />
                <Input placeholder="Zipcode" {...register("zipcode")} />
                <Input placeholder="Cuisine" {...register("cuisine")} />
                <Input
                    placeholder="Price Range (e.g. $$, $$$)"
                    {...register("price_range")}
                />
                <Input placeholder="Map URL" {...register("map_url")} />

                <Heading size="sm" mt={4}>
                    Opening Hours
                </Heading>

                <SimpleGrid columns={2} gap={3}>
                    <Input
                        placeholder="Monday (e.g. 10:00 AM - 9:00 PM)"
                        {...register("open_mon")}
                    />
                    <Input placeholder="Tuesday" {...register("open_tue")} />
                    <Input placeholder="Wednesday" {...register("open_wed")} />
                    <Input placeholder="Thursday" {...register("open_thu")} />
                    <Input placeholder="Friday" {...register("open_fri")} />
                    <Input placeholder="Saturday" {...register("open_sat")} />
                    <Input placeholder="Sunday" {...register("open_sun")} />
                </SimpleGrid>

                {/* Buttons */}
                <HStack justify="flex-end" mt={6}>
                    {onCancel && (
                        <Button variant="outline" onClick={onCancel}>
                            Cancel
                        </Button>
                    )}
                    <Button
                        type="submit"
                        colorScheme="blue"
                        isLoading={isSubmitting}
                    >
                        Save
                    </Button>
                </HStack>
            </VStack>
        </Box>
    )
}
