// src/components/LoginDialog.tsx
import { Dialog } from "@chakra-ui/react"
import { useNavigate } from "react-router-dom"
import useUser from "@/lib/useUser"
import SocialLogin from "./SoicalLogin"

interface LoginDialogProps {
    isOpen: boolean
    onClose: () => void
}

export default function LoginDialog({ isOpen, onClose }: LoginDialogProps) {
    const navigate = useNavigate()
    const { refetchUser } = useUser()
    return (
        <Dialog.Root
            key="center"
            placement={"center"}
            motionPreset={"slide-in-bottom"}
            open={isOpen}
            onOpenChange={(v) => !v && onClose()}
        >
            <Dialog.Backdrop />
            <Dialog.Positioner
                display={"flex"}
                justifyContent={"center"}
                alignItems={"center"}
                minH="100vh"
            >
                <Dialog.Content maxW={"md"} width="100%">
                    <Dialog.Header>
                        <Dialog.Title textAlign={"center"} width={"100%"}>
                            Login
                        </Dialog.Title>
                    </Dialog.Header>
                    <Dialog.Body>
                        <SocialLogin
                            onCancel={onClose}
                            onLoginSuccess={async () => {
                                const { data: user } = await refetchUser()

                                if (user?.role === "MANAGER") {
                                    navigate("/manager-dashboard")
                                } else {
                                    navigate("/")
                                }

                                onClose()
                            }}
                        />
                    </Dialog.Body>
                </Dialog.Content>
            </Dialog.Positioner>
        </Dialog.Root>
    )
}
