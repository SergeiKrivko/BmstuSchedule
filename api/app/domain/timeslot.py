from datetime import datetime

from pydantic import BaseModel


class TimeSlot(BaseModel):
    start_time: datetime
    end_time: datetime
