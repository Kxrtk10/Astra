from pydantic import BaseModel
from datetime import datetime


class ContextItem(BaseModel):

    text: str
    type: str
    timestamp: str = datetime.now().isoformat()