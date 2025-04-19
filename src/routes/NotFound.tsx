import { Button, Heading, Text, VStack } from "@chakra-ui/react"
import { Link } from "react-router-dom"

export default function NotFound() {
    return (
        <VStack bg="gray.900" justifyContent={"center"} minH="100vh">
            <Heading>Page not found.</Heading>
            <Text>It seems that you're lost.</Text>
            <Link to="/">
                <Button colorPalette={"red"} variant={"solid"}>
                    Go home &rarr;
                </Button>
            </Link>
        </VStack>
    )
}
