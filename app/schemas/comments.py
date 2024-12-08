from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserCommentSchema(BaseModel):
    first_name: str
    last_name: str
    model_config = ConfigDict(from_attributes=True)


class VerifiedCommentsSchema(BaseModel):
    comment: str
    date_added: datetime
    user: UserCommentSchema
    model_config = ConfigDict(from_attributes=True)


class CommentsSchema(VerifiedCommentsSchema):
    id: int
    is_verified: bool
