import { useForm } from "react-hook-form"
import { login } from "@/api/authapi"
import { Button, Input, Field, Stack, HStack } from "@chakra-ui/react"

interface FormValues {
    username: string
    password: string
}

interface Props {
    onCancel: () => void
    onLoginSuccess: () => void
}

export default function SocialLogin({ onCancel, onLoginSuccess }: Props) {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<FormValues>()

    const onSubmit = async (data: FormValues) => {
        try {
            await login(data.username, data.password)
            console.log("✅ Login successful")
            onLoginSuccess()
        } catch (err: unknown) {
            console.error("❌ Login failed:", err)
            alert("❌ Login failed. Please check your credentials.")
        }
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} style={{ width: "100%" }}>
            <Stack gap={4}>
                <Field.Root invalid={!!errors.username}>
                    <Field.Label>username</Field.Label>
                    <Input
                        {...register("username", {
                            required: "username is required",
                        })}
                    />
                    <Field.ErrorText>
                        {errors.username?.message}
                    </Field.ErrorText>
                </Field.Root>
                <Field.Root invalid={!!errors.password}>
                    <Field.Label>Password</Field.Label>
                    <Input
                        type="password"
                        {...register("password", {
                            required: "Password is required",
                        })}
                    />
                    <Field.ErrorText>
                        {errors.password?.message}
                    </Field.ErrorText>
                </Field.Root>
                <HStack justify="flex-end">
                    <Button type="button" onClick={onCancel}>
                        Cancel
                    </Button>
                    <Button type="submit" colorScheme="blue">
                        Login
                    </Button>
                </HStack>
            </Stack>
        </form>
    )
}
