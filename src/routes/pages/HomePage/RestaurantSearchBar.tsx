import {
    Box,
    Button,
    Input,
    Stack,
    HStack,
    Select,
    Field,
    createListCollection,
    Portal,
} from "@chakra-ui/react"
import { useForm, Controller } from "react-hook-form"
import { getSearchRestaurants } from "@/api/restauratnsApi"
import { useState } from "react"
import type { ValidSearchParams } from "@/api/restauratnsApi"
import type { Restaurant } from "@/types/restaurantsdto"

interface Props {
    onSearchResults: (data: Restaurant[]) => void
}

const costRatingOptions = createListCollection({
    items: [
        { label: "$30 and under", value: "$30 and under" },
        { label: "$31 to $50", value: "$31 to $50" },
        { label: "$50 and over", value: "$50 and over" },
    ],
})

export default function RestaurantSearchBar({ onSearchResults }: Props) {
    const { register, handleSubmit, control } = useForm<ValidSearchParams>()
    const [isSearching, setIsSearching] = useState(false)

    const onSubmit = async (formData: ValidSearchParams) => {
        setIsSearching(true)
        try {
            const results = await getSearchRestaurants(formData)
            onSearchResults(results)
        } catch (err) {
            console.error("Search failed:", err)
        } finally {
            setIsSearching(false)
        }
    }

    return (
        <Box width="100%" maxW="4xl" px={4}>
            <form onSubmit={handleSubmit(onSubmit)}>
                <Stack gap={4}>
                    <HStack gap={4}>
                        <Field.Root>
                            <Field.Label>Name</Field.Label>
                            <Input
                                placeholder="Sushi Garden"
                                {...register("name")}
                            />
                        </Field.Root>

                        <Field.Root>
                            <Field.Label>City</Field.Label>
                            <Input
                                placeholder="San Jose"
                                {...register("city")}
                            />
                        </Field.Root>
                    </HStack>

                    <HStack gap={4}>
                        <Field.Root>
                            <Field.Label>Cuisine</Field.Label>
                            <Input
                                placeholder="Japanese"
                                {...register("cuisine")}
                            />
                        </Field.Root>

                        <Field.Root>
                            <Field.Label>Zipcode</Field.Label>
                            <Input
                                placeholder="95112"
                                {...register("zipcode")}
                            />
                        </Field.Root>
                    </HStack>

                    <HStack gap={4}>
                        <Field.Root>
                            <Field.Label>Date</Field.Label>
                            <Input type="date" {...register("date")} />
                        </Field.Root>

                        <Field.Root>
                            <Field.Label>Time</Field.Label>
                            <Input type="time" {...register("time")} />
                        </Field.Root>
                    </HStack>

                    <HStack gap={4}>
                        <Field.Root>
                            <Field.Label>Cost Rating</Field.Label>
                            <Controller
                                name="cost_rating"
                                control={control}
                                render={({ field }) => (
                                    <Select.Root
                                        value={field.value}
                                        onValueChange={(val) =>
                                            field.onChange(val)
                                        }
                                        collection={costRatingOptions}
                                        size="md"
                                    >
                                        <Select.HiddenSelect />
                                        <Select.Control>
                                            <Select.Trigger>
                                                <Select.ValueText placeholder="Select price range" />
                                            </Select.Trigger>
                                            <Select.IndicatorGroup>
                                                <Select.Indicator />
                                            </Select.IndicatorGroup>
                                        </Select.Control>
                                        <Portal>
                                            <Select.Positioner>
                                                <Select.Content>
                                                    {costRatingOptions.items.map(
                                                        (item) => (
                                                            <Select.Item
                                                                item={item}
                                                                key={item.value}
                                                            >
                                                                {item.label}
                                                                <Select.ItemIndicator />
                                                            </Select.Item>
                                                        )
                                                    )}
                                                </Select.Content>
                                            </Select.Positioner>
                                        </Portal>
                                    </Select.Root>
                                )}
                            />
                        </Field.Root>
                    </HStack>

                    <HStack justify="flex-end">
                        <Button
                            type="submit"
                            colorScheme="blue"
                            loading={isSearching}
                        >
                            Search
                        </Button>
                    </HStack>
                </Stack>
            </form>
        </Box>
    )
}
