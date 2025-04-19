import { Box, Button, HStack } from "@chakra-ui/react"
import { Link, Outlet } from "react-router-dom"
import { useState } from "react"
import { MdDinnerDining } from "react-icons/md"

import LoginDialog from "./components/auth_components/LoginDialog"
import SignupDialog from "./components/auth_components/SignUpDialog"

export default function Root() {
    const [isLoginOpen, setLoginOpen] = useState(false)
    const [isSignupOpen, setSignupOpen] = useState(false)
    return (
        <Box>
            <HStack
                justifyContent={"space-between"}
                py={5}
                px={10}
                borderBottomWidth={1}
            >
                <Box color="red.500">
                    <Link to={"/"}>
                        <MdDinnerDining size={"48"} />
                    </Link>
                </Box>
                <HStack h="2">
                    <Button onClick={() => setLoginOpen(true)}>Login</Button>
                    <Button
                        colorPalette={"red"}
                        onClick={() => setSignupOpen(true)}
                    >
                        Sign Up
                    </Button>
                </HStack>
            </HStack>
            <LoginDialog
                isOpen={isLoginOpen}
                onClose={() => setLoginOpen(false)}
            />
            <SignupDialog
                isOpen={isSignupOpen}
                onClose={() => setSignupOpen(false)}
            />
            <Outlet />
        </Box>
    )
}
