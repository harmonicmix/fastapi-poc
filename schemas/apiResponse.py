from pydantic import BaseModel
from typing import Any, List, Union
from datetime import datetime

class APIResponseBase(BaseModel):
    timeStamp: datetime
    status: str
    data: Any
    