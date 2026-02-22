from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class ConsultingRequestBase(BaseModel):
    project_id: UUID4
    type: str
    objective: str

class ConsultingRequestCreate(ConsultingRequestBase):
    pass

class ConsultingRequestResponse(ConsultingRequestBase):
    id: UUID4
    user_id: UUID4
    status: str
    meeting_link: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
