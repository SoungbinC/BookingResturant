import { createBrowserRouter } from "react-router-dom"
import NotFound from "./routes/NotFound"
import Root from "./routes/root"

import Home from "./routes/pages/HomePage/Home"
import RestaurantDetail from "./routes/pages/RestuarntDetail/RestaurantDetail"
import CustomerDashboard from "./routes/pages/Customer/Customerdashboard"
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
            {
                path: "profile",
                element: <CustomerDashboard />,
            },
        ],
    },
])

export default router
