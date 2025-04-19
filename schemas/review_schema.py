# schemas/review_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    restaurant_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewRead(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
