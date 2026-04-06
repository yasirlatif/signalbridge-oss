from pydantic import BaseModel

class TimeSeriesRecord(BaseModel):
    tag: str
    timestamp: str
    value: float
