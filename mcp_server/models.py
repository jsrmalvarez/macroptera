from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None