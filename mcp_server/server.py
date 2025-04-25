from fastmcp import FastMCP, Context
from typing import Optional, List
from models import Item, ItemCreate, ItemUpdate
from client import APIClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP and API client
mcp = FastMCP(name="Items Manager")
api_client = APIClient()

@mcp.tool()
async def list_items(ctx: Context, is_active: Optional[bool] = None) -> str:
    """List all items in the database, optionally filtered by active status."""
    items = await api_client.get_items(is_active)
    
    if not items:
        return "No items found."
    
    items_text = "\n".join([
        f"ID: {item.id}\n"
        f"Title: {item.title}\n"
        f"Description: {item.description or 'N/A'}\n"
        f"Status: {'Active' if item.is_active else 'Inactive'}\n"
        f"Created: {item.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        for item in items
    ])
    
    return f"Here are the items ({len(items)}):\n\n{items_text}"

@mcp.tool()
async def get_item_details(ctx: Context, item_id: int) -> str:
    """Get details about a specific item."""
    try:
        item = await api_client.get_item(item_id)
        return (
            f"Here are the details for item {item_id}:\n\n"
            f"Title: {item.title}\n"
            f"Description: {item.description or 'N/A'}\n"
            f"Status: {'Active' if item.is_active else 'Inactive'}\n"
            f"Created: {item.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Last Updated: {item.updated_at.strftime('%Y-%m-%d %H:%M:%S') if item.updated_at else 'Never'}"
        )
    except Exception as e:
        return f"Error: Could not find item with ID {item_id}"

@mcp.tool()
async def create_item(ctx: Context, title: str, description: Optional[str] = None, is_active: bool = True) -> str:
    """Create a new item in the database."""
    try:
        new_item = ItemCreate(
            title=title,
            description=description,
            is_active=is_active
        )
        created_item = await api_client.create_item(new_item)
        
        return (
            f"Successfully created new item:\n\n"
            f"ID: {created_item.id}\n"
            f"Title: {created_item.title}\n"
            f"Description: {created_item.description or 'N/A'}\n"
            f"Status: {'Active' if created_item.is_active else 'Inactive'}"
        )
    except Exception as e:
        return f"Error: Could not create item. {str(e)}"

@mcp.tool()
async def update_item(ctx: Context, item_id: int, title: Optional[str] = None, 
                     description: Optional[str] = None, is_active: Optional[bool] = None) -> str:
    """Update an existing item."""
    try:
        # First check if item exists
        await api_client.get_item(item_id)
        
        # Create update object
        item_update = ItemUpdate(
            title=title,
            description=description,
            is_active=is_active
        )
        
        # Update the item
        updated_item = await api_client.update_item(item_id, item_update)
        return (
            f"Successfully updated item {item_id}:\n\n"
            f"Title: {updated_item.title}\n"
            f"Description: {updated_item.description or 'N/A'}\n"
            f"Status: {'Active' if updated_item.is_active else 'Inactive'}\n"
            f"Last Updated: {updated_item.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    except Exception as e:
        return f"Error: Could not update item {item_id}. {str(e)}"

@mcp.tool()
async def delete_item(ctx: Context, item_id: int) -> str:
    """Delete an item from the database."""
    try:
        # Get item details before deletion
        item = await api_client.get_item(item_id)
        await api_client.delete_item(item_id)
        return f"Successfully deleted item '{item.title}' (ID: {item_id})"
    except Exception as e:
        return f"Error: Could not delete item {item_id}. {str(e)}"

@mcp.tool()
async def find_item(ctx: Context, title: str) -> str:
    """Find an item by its title."""
    try:
        item = await api_client.find_item_by_title(title)
        if not item:
            return f"No items found with title containing '{title}'"
        
        return (
            f"Found item matching '{title}':\n\n"
            f"ID: {item.id}\n"
            f"Title: {item.title}\n"
            f"Description: {item.description or 'N/A'}\n"
            f"Status: {'Active' if item.is_active else 'Inactive'}\n"
            f"Created: {item.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    except Exception as e:
        return f"Error searching for items: {str(e)}"

if __name__ == "__main__":
    port = int(os.getenv("MCP_PORT", "5000"))
    host = os.getenv("MCP_HOST", "0.0.0.0")
    
    # Print startup message
    print(f"MCP Server starting up on {host}:{port}...")
    
    try:
        mcp.run("sse")
    finally:
        # Close the API client when the server shuts down
        import asyncio
        asyncio.run(api_client.close())