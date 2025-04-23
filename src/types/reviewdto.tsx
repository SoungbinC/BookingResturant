// src/types/review.ts
import { User } from "./userdto"
export interface Review {
    id: number
    user: User
    comment: string
    rating: number
    created_at: string
}
