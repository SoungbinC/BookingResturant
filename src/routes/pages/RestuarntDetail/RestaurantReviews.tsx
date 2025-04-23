import { useQuery } from "@tanstack/react-query"
import { getRestaurantReviews } from "@/api/restauratnsApi"
import { LuAlarmClockPlus } from "react-icons/lu"
import { Review } from "../../../types/reviewdto"
import { Box, Heading, Stack, Text, Spinner, Alert } from "@chakra-ui/react"
import { useState } from "react"
interface Props {
    restaurantId: number
}

export default function RestaurantReviews({ restaurantId }: Props) {
    const {
        data: reviews,
        isLoading,
        isError,
    } = useQuery<Review[]>({
        queryKey: ["reviews", restaurantId],
        queryFn: () => getRestaurantReviews(restaurantId),
        enabled: !!restaurantId,
    })

    const [expandedComments, setExpandedComments] = useState<
        Record<number, boolean>
    >({})

    const isExpanded = (id: number) => expandedComments[id] ?? false

    const toggleExpanded = (id: number) => {
        setExpandedComments((prev) => ({
            ...prev,
            [id]: !prev[id],
        }))
    }

    const getCommentContent = (id: number, content: string) => {
        if (content.length <= 200) return content
        return isExpanded(id) ? content : content.slice(0, 200) + "..."
    }
    return (
        <Box mt={10}>
            <Heading size="md" mb={4}>
                Customer Reviews
            </Heading>

            {isLoading ? (
                <Spinner />
            ) : isError ? (
                <Alert.Root status="error" mt={6}>
                    <Alert.Indicator>
                        <LuAlarmClockPlus size={20} />
                    </Alert.Indicator>
                    <Alert.Title>Failed to load reviews.</Alert.Title>
                </Alert.Root>
            ) : reviews && reviews.length > 0 ? (
                <Stack gap={4}>
                    {reviews.map((review: Review) => (
                        <Box
                            key={review.id}
                            p={4}
                            borderWidth="1px"
                            borderRadius="md"
                            bg="gray.50"
                            shadow="sm"
                        >
                            <Box
                                display="flex"
                                flexDirection={{ base: "column", md: "row" }}
                            >
                                {/* Sidebar Metadata */}
                                <Box
                                    minW="150px"
                                    mb={{ base: 2, md: 0 }}
                                    mr={{ md: 4 }}
                                    color="gray.600"
                                    fontSize="sm"
                                >
                                    <Text fontWeight="bold">
                                        {review.user?.username ?? "Anonymous"}
                                    </Text>
                                    <Text>
                                        {new Date(
                                            review.created_at
                                        ).toLocaleDateString()}
                                    </Text>
                                    <Text>Rating: ⭐ {review.rating}</Text>
                                </Box>

                                {/* Comment Content */}
                                <Box flex="1">
                                    <Text
                                        color="gray.800"
                                        whiteSpace="pre-wrap"
                                    >
                                        {getCommentContent(
                                            review.id,
                                            review.comment
                                        )}
                                    </Text>
                                    {review.comment.length > 200 && (
                                        <Text
                                            mt={2}
                                            color="blue.500"
                                            cursor="pointer"
                                            fontSize="sm"
                                            onClick={() =>
                                                toggleExpanded(review.id)
                                            }
                                        >
                                            {isExpanded(review.id)
                                                ? "Show less"
                                                : "Read more"}
                                        </Text>
                                    )}
                                </Box>
                            </Box>
                        </Box>
                    ))}
                </Stack>
            ) : (
                <Text>No reviews yet.</Text>
            )}
        </Box>
    )
}
