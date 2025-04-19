# models/common.py
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime


class Base(DeclarativeBase):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
