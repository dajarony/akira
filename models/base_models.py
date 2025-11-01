from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BaseResponse(BaseModel):
    success: bool
    message: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    execution_time_ms: Optional[float] = None
