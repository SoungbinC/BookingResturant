import { useQuery } from "@tanstack/react-query"
import { getMe } from "@/api/authapi"

export default function useUser() {
    const query = useQuery({
        queryKey: ["me"],
        queryFn: getMe,
        retry: false,
        staleTime: 0,
    })

    return {
        userLoading: query.isLoading,
        user: query.data,
        isLoggedIn: !!query.data,
        refetchUser: query.refetch,
    }
}
