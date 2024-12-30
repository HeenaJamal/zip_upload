from pydantic import BaseModel
from typing import Any, Dict

class CSVDataSchema(BaseModel):
    data: Dict[str, Any]
    
    class Config:
        from_attributes = True  # Use for compatibility with Pydantic V2