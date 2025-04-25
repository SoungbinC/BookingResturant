import { Button, Field, Input, Stack, HStack } from "@chakra-ui/react"
import { useForm } from "react-hook-form"
import { signup, SignupData } from "@/api/authapi"

interface Props {
    onCancel: () => void
}

export default function SignupForm({ onCancel }: Props) {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<SignupData>()

    const onSubmit = async (data: SignupData) => {
        try {
            const result = await signup(data)
            console.log("✅ Account created:", result)
            alert("Account created successfully!")
            onCancel()
        } catch (err) {
            if (err instanceof Error) {
                console.error("❌ Signup failed:", err.message)
                alert("Signup failed. Please try again.")
            } else {
                console.error("❌ Unknown error:", err)
                alert("An unexpected error occurred. Please try again.")
            }
        }
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} style={{ width: "100%" }}>
            <Stack gap={4} maxW="sm" width="100%">
                <Field.Root invalid={!!errors.username}>
                    <Field.Label>Username</Field.Label>
                    <Input {...register("username", { required: true })} />
                </Field.Root>

                <Field.Root invalid={!!errors.email}>
                    <Field.Label>Email</Field.Label>
                    <Input
                        type="email"
                        {...register("email", { required: true })}
                    />
                </Field.Root>

                <Field.Root invalid={!!errors.password}>
                    <Field.Label>Password</Field.Label>
                    <Input
                        type="password"
                        {...register("password", { required: true })}
                    />
                </Field.Root>

                <HStack justify="flex-end" pt={2}>
                    <Button onClick={onCancel} variant="outline">
                        Cancel
                    </Button>
                    <Button colorPalette="red" type="submit">
                        Sign Up
                    </Button>
                </HStack>
            </Stack>
        </form>
    )
}
