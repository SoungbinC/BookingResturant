// src/components/SignupDialog.tsx
import {
    Dialog,
    DialogBackdrop,
    DialogBody,
    DialogContent,
    DialogHeader,
    DialogPositioner,
    DialogTitle,
} from "@chakra-ui/react"

import SignupForm from "./SignupForm"

interface SignupDialogProps {
    isOpen: boolean
    onClose: () => void
}

export default function SignupDialog({ isOpen, onClose }: SignupDialogProps) {
    return (
        <Dialog.Root
            key="center"
            placement={"center"}
            motionPreset={"slide-in-bottom"}
            open={isOpen}
            onOpenChange={(v) => !v && onClose()}
        >
            <DialogBackdrop />
            <DialogPositioner
                display={"flex"}
                justifyContent={"center"}
                alignItems={"center"}
                minH="100vh"
            >
                <DialogContent maxW={"md"} width="100%">
                    <DialogHeader>
                        <DialogTitle textAlign={"center"} width={"100%"}>
                            Sign Up
                        </DialogTitle>
                    </DialogHeader>
                    <DialogBody>
                        <SignupForm onCancel={onClose} />
                    </DialogBody>
                </DialogContent>
            </DialogPositioner>
        </Dialog.Root>
    )
}
