import httpx
from typing import List, Optional, Dict, Any
from models import Item, ItemCreate, ItemUpdate
import os
from dotenv import load_dotenv

load_dotenv()

# API base URL from environment or default to localhost:8000
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")


class APIClient:
    """Client for interacting with the FastAPI backend."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=BASE_URL, timeout=30.0)
    
    async def close(self):
        await self.client.aclose()
    
    async def get_items(self, is_active: Optional[bool] = None) -> List[Item]:
        """Get all items with optional filter for active status."""
        params = {}
        if is_active is not None:
            params["is_active"] = str(is_active).lower()
        
        response = await self.client.get("/items/", params=params)
        response.raise_for_status()
        items_data = response.json()
        return [Item(**item) for item in items_data]
    
    async def get_item(self, item_id: int) -> Item:
        """Get a single item by ID."""
        response = await self.client.get(f"/items/{item_id}")
        response.raise_for_status()
        return Item(**response.json())
    
    async def create_item(self, item: ItemCreate) -> Item:
        """Create a new item."""
        response = await self.client.post("/items/", json=item.dict())
        response.raise_for_status()
        return Item(**response.json())
    
    async def update_item(self, item_id: int, item_update: ItemUpdate) -> Item:
        """Update an existing item."""
        # Remove None values from the update payload
        update_data = {k: v for k, v in item_update.dict().items() if v is not None}
        response = await self.client.put(f"/items/{item_id}", json=update_data)
        response.raise_for_status()
        return Item(**response.json())
    
    async def delete_item(self, item_id: int) -> bool:
        """Delete an item by ID."""
        response = await self.client.delete(f"/items/{item_id}")
        response.raise_for_status()
        return True
    
    async def find_item_by_title(self, title: str) -> Optional[Item]:
        """Find an item by its title (case-insensitive partial match)."""
        items = await self.get_items()
        
        # Find first item with matching title (case-insensitive)
        for item in items:
            if title.lower() in item.title.lower():
                return item
        
        return None