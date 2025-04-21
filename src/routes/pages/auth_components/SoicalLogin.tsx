import { Button, Field, Input, Stack, HStack } from "@chakra-ui/react"
import { PasswordInput } from "@/components/ui/password-input"
import { useForm } from "react-hook-form"

interface FormValues {
    username: string
    password: string
}

interface SocialLoginProps {
    onCancel: () => void
}

export default function SocialLogin({ onCancel }: SocialLoginProps) {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<FormValues>()

    const onSubmit = (data: FormValues) => {
        console.log("Login Submitted:", data)
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} style={{ width: "100%" }}>
            <Stack gap={4} align="flex-start" maxW="sm" width="100%">
                <Field.Root invalid={!!errors.username} width="100%">
                    <Field.Label>Username</Field.Label>
                    <Input
                        {...register("username", {
                            required: "Username is required",
                        })}
                        placeholder="Enter username"
                    />
                    <Field.ErrorText>
                        {errors.username?.message}
                    </Field.ErrorText>
                </Field.Root>

                <Field.Root invalid={!!errors.password} width="100%">
                    <Field.Label>Password</Field.Label>
                    <PasswordInput
                        {...register("password", {
                            required: "Password is required",
                        })}
                        placeholder="Enter password"
                    />
                    <Field.ErrorText>
                        {errors.password?.message}
                    </Field.ErrorText>
                </Field.Root>

                <HStack width="100%" justify="flex-end" pt={2}>
                    <Button variant="outline" type="button" onClick={onCancel}>
                        Cancel
                    </Button>
                    <Button colorScheme="blue" type="submit">
                        Login
                    </Button>
                </HStack>
            </Stack>
        </form>
    )
}
