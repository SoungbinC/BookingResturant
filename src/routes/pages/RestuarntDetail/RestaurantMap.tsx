import { Box, Heading } from "@chakra-ui/react"
import { Restaurant } from "@/types/restaurantsdto"

export default function RestaurantMap({
    restaurant,
}: {
    restaurant: Restaurant
}) {
    const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
    console.log(restaurant.map_url)
    const url = new URL(restaurant.map_url || "")
    const destination = url.searchParams.get("destination") || ""
    const embedUrl = `https://www.google.com/maps/embed/v1/place?key=${apiKey}&q=${encodeURIComponent(
        destination
    )}`

    return (
        <Box mt={10}>
            <Heading size="sm" mb={2}>
                Restaurant Location
            </Heading>
            <div style={{ borderRadius: "8px", overflow: "hidden" }}>
                <iframe
                    width="100%"
                    height="300"
                    loading="lazy"
                    style={{ border: 0 }}
                    allowFullScreen
                    referrerPolicy="no-referrer-when-downgrade"
                    src={embedUrl}
                />
            </div>
        </Box>
    )
}
