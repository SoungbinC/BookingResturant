import { createBrowserRouter } from "react-router-dom"
import NotFound from "./routes/NotFound"
import Root from "./routes/root"

import Home from "./routes/pages/HomePage/Home"
import RestaurantDetail from "./routes/pages/RestaurantDetail"
const router = createBrowserRouter([
    {
        path: "/",
        element: <Root />,
        errorElement: <NotFound />,
        children: [
            {
                path: "",
                element: <Home />,
            },
            {
                path: "restaurants/:id",
                element: <RestaurantDetail />,
            },
        ],
    },
])

export default router
