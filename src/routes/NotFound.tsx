import { Button, Heading, Text, VStack } from "@chakra-ui/react"
import { Link } from "react-router-dom"
import useUser from "@/lib/useUser"

export default function NotFound() {
    const { user } = useUser() // ✅ get logged-in user info

    const redirectPath = user?.role === "MANAGER" ? "/manager-dashboard" : "/"

    return (
        <VStack bg="gray.900" justifyContent={"center"} minH="100vh">
            <Heading>Page not found.</Heading>
            <Text>It seems that you're lost.</Text>
            <Link to={redirectPath}>
                <Button colorPalette={"red"} variant={"solid"}>
                    Go {user?.role === "MANAGER" ? "Dashboard" : "Home"} &rarr;
                </Button>
            </Link>
        </VStack>
    )
}
