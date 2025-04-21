import { Input, InputGroup, Kbd, Box } from "@chakra-ui/react"
import { LuSearch } from "react-icons/lu"
import { useForm } from "react-hook-form"

interface SearchFormValues {
    query: string
}

export default function RestaurantSearchBar() {
    const { register, handleSubmit } = useForm<SearchFormValues>()

    const onSubmit = (data: SearchFormValues) => {
        console.log("Searching for:", data.query)
        // Navigate or call API
    }

    return (
        <Box as="form" onSubmit={handleSubmit(onSubmit)} width="100%" maxW="m">
            <InputGroup
                startElement={<LuSearch color="gray" />}
                endElement={<Kbd bg="transparent">⌘K</Kbd>}
            >
                <Input
                    placeholder="Search restaurants"
                    variant="outline"
                    {...register("query", { required: true })}
                />
            </InputGroup>
        </Box>
    )
}
