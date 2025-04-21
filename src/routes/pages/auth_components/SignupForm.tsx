import { Button, Field, Input, Stack, HStack } from "@chakra-ui/react"
import { PasswordInput } from "@/components/ui/password-input"
import { useForm } from "react-hook-form"

interface FormValues {
    username: string
    email: string
    password: string
}

interface SignupFormProps {
    onCancel: () => void
}

export default function SignupForm({ onCancel }: SignupFormProps) {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<FormValues>()

    const onSubmit = (data: FormValues) => {
        console.log("Signup Submitted:", data)
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

                <Field.Root invalid={!!errors.email} width="100%">
                    <Field.Label>Email</Field.Label>
                    <Input
                        type="email"
                        {...register("email", {
                            required: "Email is required",
                            pattern: {
                                value: /^\S+@\S+$/i,
                                message: "Invalid email address",
                            },
                        })}
                        placeholder="Enter email"
                    />
                    <Field.ErrorText>{errors.email?.message}</Field.ErrorText>
                </Field.Root>

                <Field.Root invalid={!!errors.password} width="100%">
                    <Field.Label>Password</Field.Label>
                    <PasswordInput
                        {...register("password", {
                            required: "Password is required",
                            minLength: {
                                value: 6,
                                message:
                                    "Password must be at least 6 characters",
                            },
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
                    <Button colorScheme="red" type="submit">
                        Sign Up
                    </Button>
                </HStack>
            </Stack>
        </form>
    )
}
