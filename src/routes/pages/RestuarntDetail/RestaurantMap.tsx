import { useEffect, useRef, useState } from "react"
import { Box, Heading, Spinner } from "@chakra-ui/react"
import { Restaurant } from "@/types/restaurantsdto"

export default function RestaurantMap({
    restaurant,
}: {
    restaurant: Restaurant
}) {
    const [isInView, setIsInView] = useState(false)
    const containerRef = useRef<HTMLDivElement>(null)

    const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
    const url = new URL(restaurant.map_url || "")
    const destination = url.searchParams.get("destination") || ""
    const embedUrl = `https://www.google.com/maps/embed/v1/place?key=${apiKey}&q=${encodeURIComponent(
        destination
    )}`

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsInView(true)
                    observer.disconnect()
                }
            },
            { threshold: 0.1 }
        )

        if (containerRef.current) {
            observer.observe(containerRef.current)
        }

        return () => observer.disconnect()
    }, [])

    return (
        <Box mt={10}>
            <Heading size="sm" mb={2}>
                Restaurant Location
            </Heading>
            <Box
                ref={containerRef}
                borderRadius="xl"
                overflow="hidden"
                bg="gray.100"
                width="100%"
                height="300px"
                position="relative"
            >
                {isInView ? (
                    <iframe
                        width="100%"
                        height="100%"
                        loading="lazy"
                        style={{ border: 0 }}
                        allowFullScreen
                        referrerPolicy="no-referrer-when-downgrade"
                        src={embedUrl}
                    />
                ) : (
                    <Box
                        position="absolute"
                        top="50%"
                        left="50%"
                        transform="translate(-50%, -50%)"
                    >
                        <Spinner size="lg" />
                    </Box>
                )}
            </Box>
        </Box>
    )
}
