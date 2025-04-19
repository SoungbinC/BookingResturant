import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { Provider } from "@/components/ui/provider"
import { RouterProvider } from "react-router-dom"
import router from "./router"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <QueryClientProvider client={new QueryClient()}>
            <Provider>
                <RouterProvider router={router} />
            </Provider>
        </QueryClientProvider>
    </StrictMode>
)
