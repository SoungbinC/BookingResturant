import { Review as ReviewType } from "@/types/reviewdto"
import { Box, Text } from "@chakra-ui/react"
import { useState } from "react"

export default function Review({ review }: { review: ReviewType }) {
    const [isExpanded, setIsExpanded] = useState(false)
    const content = review.comment ?? ""
    const shouldTruncate = content.length > 200
    const displayText =
        !shouldTruncate || isExpanded ? content : content.slice(0, 200) + "..."

    return (
        <Box p={4} borderWidth="1px" borderRadius="md" bg="gray.50" shadow="sm">
            <Box display="flex" flexDirection={{ base: "column", md: "row" }}>
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
                        {new Date(review.created_at).toLocaleDateString()}
                    </Text>
                    <Text>Rating: ⭐ {review.rating}</Text>
                </Box>

                {/* Comment Block */}
                <Box flex="1">
                    <Text whiteSpace="pre-wrap">{displayText}</Text>
                    {shouldTruncate && (
                        <Text
                            mt={2}
                            color="blue.500"
                            cursor="pointer"
                            fontSize="sm"
                            onClick={() => setIsExpanded((prev) => !prev)}
                        >
                            {isExpanded ? "Show less" : "Read more"}
                        </Text>
                    )}
                </Box>
            </Box>
        </Box>
    )
}
