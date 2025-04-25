import { Box, Button, HStack, Avatar, Menu, Portal } from "@chakra-ui/react"
import { Link, Outlet } from "react-router-dom"
import { useState } from "react"
import { MdDinnerDining } from "react-icons/md"

import toast from "react-hot-toast"
import { logout } from "@/api/authapi"

import LoginDialog from "./pages/auth_components/LoginDialog"
import SignupDialog from "./pages/auth_components/SignUpDialog"
import useUser from "@/lib/useUser"

export default function Root() {
    const [isLoginOpen, setLoginOpen] = useState(false)
    const [isSignupOpen, setSignupOpen] = useState(false)

    const { user, isLoggedIn, userLoading } = useUser()

    const handleLogout = async () => {
        try {
            await logout()
            toast.success("👋 Logged out successfully!")
            localStorage.clear()
            window.location.reload()
        } catch (err: unknown) {
            console.error("❌ Logout failed:", err)
            toast.error("Failed to log out. Please try again.")
        }
    }

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

                <HStack gap={4}>
                    {!userLoading ? (
                        isLoggedIn && user ? (
                            <Menu.Root>
                                <Menu.Trigger>
                                    <Avatar.Root variant="solid" size="md">
                                        <Avatar.Fallback name={user.username} />
                                    </Avatar.Root>
                                </Menu.Trigger>
                                <Portal>
                                    <Menu.Positioner>
                                        <Menu.Content>
                                            <Menu.Item value="profile">
                                                <Link to="/profile">
                                                    Profile
                                                </Link>
                                            </Menu.Item>
                                            <Menu.Item
                                                value="logout"
                                                onSelect={handleLogout}
                                            >
                                                Logout
                                            </Menu.Item>
                                        </Menu.Content>
                                    </Menu.Positioner>
                                </Portal>
                            </Menu.Root>
                        ) : (
                            <>
                                <Button onClick={() => setLoginOpen(true)}>
                                    Login
                                </Button>
                                <Button
                                    colorPalette={"red"}
                                    onClick={() => setSignupOpen(true)}
                                >
                                    Sign Up
                                </Button>
                            </>
                        )
                    ) : null}
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
